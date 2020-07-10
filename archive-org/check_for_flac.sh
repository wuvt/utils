#!/bin/bash
# can also search for oggs in aircheck

for line in $(cat missing_files.txt); do
	DATE=$(echo $line |\
		sed -r -e 's/^WUVTFM_2017(..)(..)_(....)Z/2017-\1-\2 \3/'|\
		xargs -I{} date -d {} -u +%Y-%m-%d-%H_%M_%S+0000.flac)
	find /tank/archive/pgmcheck/fm/2017/ -iname $DATE -print -exec echo $line>>have_flac.txt \; 
done                                         
