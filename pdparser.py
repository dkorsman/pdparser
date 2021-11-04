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
arg_parse.add_argument('-v', '--verbosity', type=int, choices=[0,1,2], default=1, help='determine level of output verbosity')
arg_parse.add_argument('-d', '--hide-code', action='store_true', help='hide code from output files except preprocessor directives and annotations')
arg_parse.add_argument('-f', '--features', action='store_true', help='try to get all involved features in defined(X)')
arg_parse.add_argument('-jr', '--json-result', action='store_true', help='store a json file with general results in the output folder')
arg_parse.add_argument('-jp', '--json-pinpoint', action='store_true', help='store json files with all locations of nesting levels and feature interactions')
arg = arg_parse.parse_args()

util.set_verbosity(arg.verbosity)

if arg.output is None:
	util.vprint(1, 'Dry-running: no output folder passed (-o/--output)')
	output_folder = None
else:
	output_folder = os.path.abspath(arg.output)

source_folder = os.path.abspath(arg.source)

util.vprint(1, 'Using source folder {}'.format(source_folder))

folders = [source_folder]

n_source_files = 0
n_ignored_files = 0
n_parser_errors = 0
ignored_exts = set()
all_features = set()
all_features_possible_guards = set()
all_features_trimmed = set()
feature_interaction_stats = {}
nesting_level_stats = {}
pinpoint_feature_interaction_stats = {}
pinpoint_nesting_level_stats = {}

t_start = time.perf_counter()

while folders:
	folder = folders.pop(0)

	for f in os.scandir(folder):
		relative_path = f.path
		if f.path.startswith(source_folder):
			relative_path = f.path[len(source_folder)+1:]

		if f.is_symlink():
			util.vprint(2, 'Ignoring symlink {}'.format(relative_path))
			continue
		if f.is_dir():
			if f.name != '.git':
				folders.append(os.path.abspath(f.path))
			continue
		if not f.is_file():
			util.vprint(2, '{} is not a file or folder or symlink'.format(relative_path))
			continue

		name_ext = os.path.splitext(f.path)

		if name_ext[1].lower() in ('.c', '.cpp', '.h', '.hpp', '.cxx', '.m', '.cc'):
			util.vprint(1, 'Found {}'.format(relative_path))
			n_source_files += 1

			result = source_parser.parse(
				f.path,
				relative_path,
				output_folder,
				arg,
				# ref:
				all_features,
				all_features_possible_guards,
				nesting_level_stats,
				feature_interaction_stats,
				pinpoint_nesting_level_stats,
				pinpoint_feature_interaction_stats
			)

			if not result:
				n_parser_errors += 1
		else:
			util.vprint(2, 'Ignoring {}'.format(relative_path))
			n_ignored_files += 1
			if name_ext[1] != '':
				ignored_exts.add(name_ext[1])

t_end = time.perf_counter()
t_taken = t_end - t_start

util.vprint(1, '{} source files, {} ignored files, {} parser errors'.format(
		n_source_files, n_ignored_files, n_parser_errors
	)
)
util.vprint(1, 'Ignored file extensions: {}'.format(ignored_exts))

if arg.features:
	util.vprint(1, '{} possible guards: {}'.format(len(all_features_possible_guards), all_features_possible_guards))

	all_features_trimmed = all_features.difference(all_features_possible_guards)
	util.vprint(1, '{} features without guards: {}'.format(len(all_features_trimmed), all_features_trimmed))

	util.vprint(1, 'Feature interaction stats (#features occurring in conditional): {}'.format(feature_interaction_stats))

util.vprint(1, 'Nesting level stats: {}'.format(nesting_level_stats))

util.vprint(1, 'Total time taken to run: {}'.format(t_taken))


if arg.json_result:
	if output_folder is None:
		util.vprint(1, '-jr/--json-result passed, but no output folder specified!')
	else:
		if not arg.features:
			util.vprint(1, '-jr/--json-result passed, but not -f/--features (will be empty!)')

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
					'n_features': len(all_features_trimmed),
					'features': list(all_features_trimmed),
					'feature_interaction_stats': feature_interaction_stats,
					'nesting_level_stats': nesting_level_stats,
					'time_taken': t_taken,
				},
				outfile
			)

		util.vprint(1, 'Wrote result json to {}'.format(json_name))

if arg.json_pinpoint:
	if output_folder is None:
		util.vprint(1, '-jp/--json-pinpoint passed, but no output folder specified!')
	elif not arg.features:
		util.vprint(1, '-jr/--json-pinpoint passed, but not -f/--features!)')
	else:
		json_name = '{}/pdparser-pinpoint-feature-interaction.json'.format(output_folder)
		with open(json_name, 'w') as outfile:
			json.dump(pinpoint_feature_interaction_stats, outfile)
		util.vprint(1, 'Wrote feature interaction pinpoint json to {}'.format(json_name))

		json_name = '{}/pdparser-pinpoint-nesting-level.json'.format(output_folder)
		with open(json_name, 'w') as outfile:
			json.dump(pinpoint_nesting_level_stats, outfile)
		util.vprint(1, 'Wrote nesting level pinpoint json to {}'.format(json_name))
