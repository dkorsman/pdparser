#!/usr/bin/python3

import argparse
import os

import source_parser
import util

arg_parse = argparse.ArgumentParser()
arg_parse.add_argument('source', help='the source folder to operate on')
arg_parse.add_argument('-o', '--output', type=str, help='the folder to write annotated source files to')
arg_parse.add_argument('-v', '--verbosity', type=int, choices=[0,1,2], default=1, help='determine level of output verbosity')
arg_parse.add_argument('-d', '--hide-code', action='store_true', help='hide code from output files except preprocessor directives and annotations')
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
			folders.append(os.path.abspath(f.path))
			continue
		if not f.is_file():
			util.vprint(2, '{} is not a file or folder or symlink'.format(relative_path))
			continue

		name_ext = os.path.splitext(f.path)

		if name_ext[1].lower() in ('.c', '.cpp', '.h', '.hpp', '.cxx', '.inc', '.m', '.cc'):
			util.vprint(1, 'Found {}'.format(relative_path))
			n_source_files += 1

			if not source_parser.parse(f.path, relative_path, output_folder, arg.hide_code):
				n_parser_errors += 1
		else:
			util.vprint(2, 'Ignoring {}'.format(relative_path))
			n_ignored_files += 1
			if name_ext[1] != '':
				ignored_exts.add(name_ext[1])

util.vprint(1, '{} source files, {} ignored files, {} parser errors'.format(
		n_source_files, n_ignored_files, n_parser_errors
	)
)
util.vprint(1, 'Ignored file extensions: {}'.format(ignored_exts))
