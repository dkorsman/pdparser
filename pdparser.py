#!/usr/bin/python3

import argparse
import json
import os
import time

import source_parser
import util

arg_parse = argparse.ArgumentParser()
arg_parse.add_argument('source', help='the source folder to operate on')
arg_parse.add_argument('-o', '--output', type=str, help='the folder to write annotated source files to')
arg_parse.add_argument('-q', '--quiet', type=str, nargs='*', metavar='CAT', help='silence a category of messages')
arg_parse.add_argument('-d', '--hide-code', action='store_true', help='hide code from output files except preprocessor directives and annotations')
arg_parse.add_argument('-f', '--features', action='store_true', help='try to get all involved features in defined(X)')
arg_parse.add_argument('-B', '--no-blacklist', action='store_true', help='ignore pdparser-blacklist.lst file (to get all files again)')
arg_parse.add_argument('-jr', '--json-result', action='store_true', help='store a json file with general results in the output folder')
arg_parse.add_argument('-jp', '--json-pinpoint', action='store_true', help='store json files with all locations of nesting levels and feature interactions')
arg = arg_parse.parse_args()

if arg.quiet is not None:
	for q in arg.quiet:
		util.hide_cat(q)

if arg.output is None:
	util.catprint('WARN', 'Dry-running: no output folder passed (-o/--output)')
	output_folder = None
else:
	output_folder = os.path.abspath(arg.output)

source_folder = os.path.abspath(arg.source)

util.catprint('info', 'Using source folder {}'.format(source_folder))

folders = [source_folder]

n_source_files = 0
n_ignored_files = 0
n_parser_errors = 0
ignored_exts = set()
all_features = set()
all_features_possible_guards = set() # possible include guards - features #define'd conditional to themselves
all_features_not_guards = set() # not include guards - features #define'd outside of their own conditional
all_features_trimmed = set()
feature_interaction_blocks = {}
nesting_level_blocks = {}
pinpoint_feature_interaction_blocks = {}
pinpoint_nesting_level_blocks = {}
feature_interaction_lines = {}
nesting_level_lines = {}

t_start = time.perf_counter()


filename_blacklist = set()
blacklist_name = '{}/pdparser-blacklist.lst'.format(source_folder)
if arg.no_blacklist:
	util.catprint('info', 'Ignoring blacklist file at {} (-B/--no-blacklist was used)'.format(blacklist_name))
else:
	try:
		with open(blacklist_name, 'r') as infile:
			for full_line in infile:
				filename_blacklist.add(full_line.strip())
		util.catprint('info', 'Blacklist file present at {}'.format(blacklist_name))
	except FileNotFoundError:
		util.catprint('info', 'Blacklist file not present (search path: {}), accepting all paths'.format(blacklist_name))
		pass


while folders:
	folder = folders.pop(0)

	for f in os.scandir(folder):
		relative_path = f.path
		if f.path.startswith(source_folder):
			relative_path = f.path[len(source_folder)+1:]

		if filename_blacklist and any(relative_path.startswith(bl) for bl in filename_blacklist):
			util.catprint('debug', 'Ignoring blacklisted file {}'.format(relative_path))
			continue
		if f.is_symlink():
			util.catprint('debug', 'Ignoring symlink {}'.format(relative_path))
			continue
		if f.is_dir():
			if f.name != '.git':
				folders.append(os.path.abspath(f.path))
			continue
		if not f.is_file():
			util.catprint('WARN', '{} is not a file or folder or symlink'.format(relative_path))
			continue

		name_ext = os.path.splitext(f.path)

		if name_ext[1].lower() in ('.c', '.cpp', '.h', '.hpp', '.cxx', '.m', '.cc'):
			util.catprint('debug', 'Found {}'.format(relative_path))
			n_source_files += 1

			result = source_parser.parse(
				f.path,
				relative_path,
				output_folder,
				arg,
				# ref:
				all_features,
				all_features_possible_guards,
				all_features_not_guards,
				nesting_level_blocks,
				feature_interaction_blocks,
				pinpoint_nesting_level_blocks,
				pinpoint_feature_interaction_blocks,
				nesting_level_lines,
				feature_interaction_lines
			)

			if not result:
				n_parser_errors += 1
		else:
			util.catprint('debug', 'Ignoring non-C/C++ file {}'.format(relative_path))
			n_ignored_files += 1
			if name_ext[1] != '':
				ignored_exts.add(name_ext[1])

t_end = time.perf_counter()
t_taken = t_end - t_start

util.catprint('info', '{} source files, {} ignored files, {} parser errors'.format(
		n_source_files, n_ignored_files, n_parser_errors
	)
)
util.catprint('info', 'Ignored file extensions: {}'.format(ignored_exts))

if arg.features:
	# First subtract the "not guards" from the "possible guards"...
	all_features_possible_guards = all_features_possible_guards.difference(all_features_not_guards)

	util.catprint('feat', '{} possible guards: {}'.format(
			len(all_features_possible_guards), all_features_possible_guards
		)
	)

	all_features_trimmed = all_features.difference(all_features_possible_guards)
	util.catprint('feat', '{} features without guards: {}'.format(
			len(all_features_trimmed), all_features_trimmed
		)
	)

	util.catprint('info', 'Feature interaction blocks (#features occurring in conditional): {}'.format(
			feature_interaction_blocks
		)
	)

	util.catprint('info', 'Feature interaction lines (line numbers conditional to X features): {}'.format(
			feature_interaction_lines
		)
	)

util.catprint('info', 'Nesting level blocks: {}'.format(nesting_level_blocks))
util.catprint('info', 'Nesting level lines: {}'.format(nesting_level_lines))

util.catprint('info', 'Total time taken to run: {}'.format(t_taken))


if arg.json_result:
	if output_folder is None:
		util.catprint('ERROR', '-jr/--json-result passed, but no output folder specified!')
	else:
		if not arg.features:
			util.catprint('ERROR', '-jr/--json-result passed, but not -f/--features (will be empty!)')

		json_name = '{}/pdparser-result.json'.format(output_folder)
		with open(json_name, 'w') as outfile:
			json.dump(
				{
					'n_source_files': n_source_files,
					'n_ignored_files': n_ignored_files,
					'n_parser_errors': n_parser_errors,
					'ignored_exts': list(ignored_exts),
					'n_possible_guards': len(all_features_possible_guards),
					'possible_guards': list(all_features_possible_guards),
					'n_other_defines': len(all_features_not_guards),
					'other_defines': list(all_features_not_guards),
					'n_features': len(all_features_trimmed),
					'features': list(all_features_trimmed),
					'feature_interaction_blocks': feature_interaction_blocks,
					'nesting_level_blocks': nesting_level_blocks,
					'feature_interaction_lines': feature_interaction_lines,
					'nesting_level_lines': nesting_level_lines,
					'time_taken': t_taken,
				},
				outfile
			)

		util.catprint('info', 'Wrote result json to {}'.format(json_name))

if arg.json_pinpoint:
	if output_folder is None:
		util.catprint('ERROR', '-jp/--json-pinpoint passed, but no output folder specified!')
	elif not arg.features:
		util.catprint('ERROR', '-jr/--json-pinpoint passed, but not -f/--features!)')
	else:
		json_name = '{}/pdparser-pinpoint-feature-interaction.json'.format(output_folder)
		with open(json_name, 'w') as outfile:
			json.dump(pinpoint_feature_interaction_blocks, outfile)
		util.catprint('info', 'Wrote feature interaction pinpoint json to {}'.format(json_name))

		json_name = '{}/pdparser-pinpoint-nesting-level.json'.format(output_folder)
		with open(json_name, 'w') as outfile:
			json.dump(pinpoint_nesting_level_blocks, outfile)
		util.catprint('info', 'Wrote nesting level pinpoint json to {}'.format(json_name))
