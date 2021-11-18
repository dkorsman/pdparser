#!/bin/bash

cd ../TEST-PDPARSER
for p in *; do
	echo 'PROJECT ' $p
	../pdparser/pdparser.py ../TEST-PDPARSER/$p/ -df -jr -jp -o ../RES-TEST-PDPARSER/$p/ -q debug parser-debug feat
done
