#!/bin/bash

for p in ../TEST-PDPARSER/*; do
	echo 'PROJECT ' $p
	cd $p
	#rm pdparser-*
	#git reset --hard
	git status
	cd ..
done
