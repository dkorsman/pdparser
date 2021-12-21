#!/usr/bin/python3

import argparse
import json
import os

arg_parse = argparse.ArgumentParser()
arg_parse.add_argument('results', help='The results folder (RES-TEST-PDPARSER)')
arg = arg_parse.parse_args()

results_folder = os.path.abspath(arg.results)

print('Using results folder {}'.format(results_folder))

feature_counts = {}


for f in os.scandir(results_folder):
	if not f.is_dir():# or f.name.startswith('.'):
		continue

	results_file = '{}/{}'.format(f.path, 'pdparser-result.json')
	try:
		with open(results_file, 'r') as infile:
			data = json.load(infile)
	except FileNotFoundError:
		print('{} does not exist'.format(results_file))
		continue

	for feature in set(data['features']):
		if feature in feature_counts:
			feature_counts[feature] += 1
		else:
			feature_counts[feature] = 1

count_counts = {}

for feature in feature_counts:
	count = feature_counts[feature]

	if count in count_counts:
		count_counts[count] += 1
	else:
		count_counts[count] = 1

print('{}'.format(count_counts))

json_name = '{}/count-project-features.json'.format(results_folder)
with open(json_name, 'w') as outfile:
	json.dump(
		{
			'n_unique_features': len(feature_counts),
			'feature_counts': feature_counts,
			'n_count_counts': len(count_counts),
			'count_counts': count_counts
		},
		outfile
	)

	print('Wrote result json to {}'.format(json_name))
