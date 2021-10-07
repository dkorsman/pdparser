import re

class DirectiveParseError(Exception):
	pass

class ParserState:
	def __init__(self):
		self.conditional_stack = []

	def stack_is_empty(self):
		return len(self.conditional_stack) == 0

	def start_if(self) -> None:
		# Start an #if...#elif...#else...#endif block
		self.conditional_stack.append([])

	def insert_conditional(self, conditional:str) -> None:
		# Insert the conditional belonging to a block in an #if...#elif... chain
		# #else will be inserted as if it were #elif 1
		if self.stack_is_empty():
			raise DirectiveParseError('Trying to insert conditional without stack item; #elif without #if?')
		self.conditional_stack[-1].append(conditional)

	def end_if(self) -> None:
		# End a block with #endif
		if self.stack_is_empty():
			raise DirectiveParseError('Too many #endif!')
		self.conditional_stack.pop()

	def calculate_current_conditional(self) -> str:
		# Get the combined conditional at the current point
		# Example:
		#if A
			#if B
				#if C
				#elif D
					# ← (A) && (B) && !(C) && (D)
				#endif
			#endif
		#endif
		conditional = ''
		first = True
		for level in self.conditional_stack:
			for i_block in range(len(level)):
				block_cond = level[i_block]
				if i_block < len(level)-1:
					# We're already an #elif or #else beyond this, so this is false!
					if not first:
						conditional += ' && '
					conditional += '!({})'.format(block_cond)
					first = False
				elif block_cond != '1':
					# We're in this block right now
					if not first:
						conditional += ' && '
					conditional += '({})'.format(block_cond)
					first = False
				else:
					#else is actually #elif 1
					pass

		return conditional

def parse(path:str, relative_path:str, output_folder:str, hide_code:bool) -> bool:
	report_line = ''
	annotated_file = ''
	result = False
	try:
		# Interpreting UTF-8 as old-school-codepage won't matter in our case, other way around is a crash...
		with open(path, 'r', encoding="ISO-8859-1") as infile:
			state = ParserState()

			clean_continued_line = ''
			multi_lines = ''
			for full_line in infile:
				report_line = full_line.strip()
				clean_line = re.sub('\/\*.*?\*\/', '', full_line)
				clean_line = re.sub('\/\*.*$', '', clean_line)
				clean_line = re.sub('\/\/.*$', '', clean_line).strip()
				clean_line = re.sub('^#\s+', '#', clean_line)
				if clean_continued_line:
					clean_line = clean_continued_line + clean_line

				if full_line.endswith('\\\n') or full_line.endswith('\\\r\n'):
					clean_continued_line += clean_line + ' '
					multi_lines += full_line
					continue

				condition_changed = False
				if clean_line.startswith('#'):
					annotated_file += multi_lines + full_line
					condition_changed = True
					if clean_line.startswith('#ifdef') or clean_line.startswith('#ifndef'):
						parse_ifdef(state, clean_line)
					elif clean_line.startswith('#if') or clean_line.startswith('#elif'):
						parse_if(state, clean_line)
					elif clean_line.startswith('#else'):
						parse_else(state, clean_line)
					elif clean_line.startswith('#endif'):
						parse_endif(state, clean_line)
					else:
						condition_changed = False
				elif not hide_code:
					annotated_file += multi_lines + full_line
				clean_continued_line = ''
				multi_lines = ''

				if condition_changed:
					condition = state.calculate_current_conditional()
					if condition == '':
						annotated_file += '// [pdparser] Always\n'
					else:
						annotated_file += '// [pdparser] Only if {}\n'.format(condition)

			if not state.stack_is_empty():
				raise DirectiveParseError('Unexpected EOF, too few #endif!')

		result = True
	except DirectiveParseError as e:
		print('    Error parsing file {}!'.format(path))
		print('    {}'.format(e))
		print('    {}'.format(report_line))

		annotated_file += '/* [pdparser] *CRASH*\n{}\n{}\n*/'.format(e, report_line)

		result = False

	# Write the annotated file
	if output_folder is not None:
		if path == relative_path:
			print('    Not writing output file, relative path is full path!')
		else:
			try:
				with open('{}/{}'.format(output_folder, relative_path), 'w') as outfile:
					outfile.write(annotated_file)
			except Exception as e:
				print('    Writing output file failed!')
				print('    {}'.format(e))

	return result

def parse_ifdef(state:ParserState, line:str) -> None:
	#ifn?def IDENTIFIER
	m = re.search('^#if(?P<n>n?)def\s+(?P<identifier>[A-Za-z0-9_]+)$', line)
	if m is None:
		raise DirectiveParseError('Could not match #ifdef/#ifndef!')

	not_op = '!' if m.group('n') == 'n' else ''
	return parse_if(state, '#if {}defined({})'.format(not_op, m.group('identifier')))

def parse_if(state:ParserState, line:str) -> None:
	#(el)?if EXPR
	m = re.search('^#(?P<el>(el)?)if\s*(?P<expr>.*)$', line)
	if m is None:
		raise DirectiveParseError('Could not match #if/#elif!')

	# Maybe parse expression so it can be simplified

	if m.group('el') == '':
		state.start_if()
	state.insert_conditional(m.group('expr'))

def parse_else(state:ParserState, line:str) -> None:
	#else
	m = re.search('^#else$', line)
	if m is None:
		raise DirectiveParseError('Could not match #else!')

	state.insert_conditional('1')

def parse_endif(state:ParserState, line:str) -> None:
	#endif
	m = re.search('^#endif$', line)
	if m is None:
		raise DirectiveParseError('Could not match #endif!')

	state.end_if()
