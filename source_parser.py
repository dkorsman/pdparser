import argparse
import os
import re
from typing import Optional

class DirectiveParseError(Exception):
	pass

class ParserState:
	def __init__(self):
		self.conditional_stack = []

	def get_stack_level(self) -> int:
		return len(self.conditional_stack)

	def stack_is_empty(self) -> bool:
		return self.get_stack_level() == 0

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

def get_involved_features(condition:str) -> set[str]:
	return set(re.findall('defined\s*[\(\s]([A-Za-z0-9_]+)\)?', condition))

def parse(
	path: str,
	relative_path: str,
	output_folder: str,
	arg: argparse.Namespace,
	# ref:
	features: set[str],
	feature_possible_guards: set[str],
	nesting_level_stats: dict[int,int],
	feature_interaction_stats: dict[int,int],
	pinpoint_nesting_level_stats, # : dict[int, list[
	pinpoint_feature_interaction_stats
) -> bool:
	report_line = ''
	annotated_file = ''
	stack_level_deepest = 0
	stack_level_latest = 0
	result = False
	try:
		# Interpreting UTF-8 as old-school-codepage won't matter in our case, other way around is a crash...
		with open(path, 'r', encoding="ISO-8859-1") as infile:
			state = ParserState()

			clean_continued_line = ''
			multi_lines = ''
			line_number = 0
			for full_line in infile:
				line_number += 1

				report_line = full_line.strip()
				clean_line = re.sub('\/\*.*?\*\/', '', full_line)
				clean_line = re.sub('\/\*.*$', '', clean_line)
				clean_line = re.sub('\/\/.*$', '', clean_line).strip()
				clean_line = re.sub('^#\s+', '#', clean_line)

				if full_line.endswith('\\\n') or full_line.endswith('\\\r\n'):
					clean_continued_line += clean_line + ' '
					multi_lines += full_line
					continue

				if clean_continued_line:
					clean_line = clean_continued_line + clean_line
					pass

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
					elif clean_line.startswith('#define') and arg.features:
						possible_guard = parse_define(state, clean_line)
						if possible_guard is not None:
							feature_possible_guards.add(possible_guard)
						condition_changed = False
					else:
						condition_changed = False
				elif not arg.hide_code:
					annotated_file += multi_lines + full_line
				clean_continued_line = ''
				multi_lines = ''

				if condition_changed:
					stack_level = state.get_stack_level()
					if stack_level > stack_level_deepest:
						stack_level_deepest = stack_level

					if stack_level >= stack_level_latest:
						if stack_level in nesting_level_stats:
							nesting_level_stats[stack_level] += 1
						else:
							nesting_level_stats[stack_level] = 1

						if arg.json_pinpoint:
							if stack_level not in pinpoint_nesting_level_stats:
								pinpoint_nesting_level_stats[stack_level] = []

							pinpoint_nesting_level_stats[stack_level].append(
								[relative_path, line_number]
							)

					stack_level_latest = stack_level

					condition = state.calculate_current_conditional()

					if condition == '':
						annotated_file += '// [pdparser] L{}, always\n'.format(stack_level)
					else:
						annotated_file += '// [pdparser] L{}, only if {}\n'.format(stack_level, condition)

					if arg.features:
						current_involved_features = get_involved_features(condition)

						annotated_file += '// [pdparser] Features involved: {}\n'.format(current_involved_features)

						features.update(current_involved_features)

						n_involved_features = len(current_involved_features)
						if n_involved_features in feature_interaction_stats:
							feature_interaction_stats[n_involved_features] += 1
						else:
							feature_interaction_stats[n_involved_features] = 1

						if arg.json_pinpoint:
							if n_involved_features not in pinpoint_feature_interaction_stats:
								pinpoint_feature_interaction_stats[n_involved_features] = []

							pinpoint_feature_interaction_stats[n_involved_features].append(
								[relative_path, line_number, condition]
							)

			if not state.stack_is_empty():
				raise DirectiveParseError('Unexpected EOF, too few #endif!')

		result = True
	except DirectiveParseError as e:
		print('    Error parsing file {}!'.format(path))
		print('    {}'.format(e))
		print('    {}'.format(report_line))

		annotated_file += '/* [pdparser] *CRASH*\n{}\n{}\n*/'.format(e, report_line)

		result = False

	annotated_file += '\n// [pdparser] deepest level: {}\n'.format(stack_level_deepest)

	# Write the annotated file
	if output_folder is not None:
		if path == relative_path:
			print('    Not writing output file, relative path is full path!')
		else:
			output_path = '{}/{}'.format(output_folder, relative_path)
			os.makedirs(output_path[:output_path.rindex('/')], exist_ok=True)
			try:
				with open(output_path, 'w') as outfile:
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

def parse_define(state:ParserState, line:str) -> Optional[str]:
	#define POSSIBLE_INCLUDE_GUARD
	m = re.search('^#define\s+(?P<identifier>[A-Za-z0-9_]+)\s*$', line)
	if m is None:
		# We're actually defining something here, or we can't parse it - but it's off the table
		return None

	# We're defining a bare identifier. Is that feature already involved?
	identifier = m.group('identifier')
	if identifier in get_involved_features(state.calculate_current_conditional()):
		print('    Possible include guard: {}'.format(identifier))
		return identifier

	return None
