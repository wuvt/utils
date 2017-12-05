#!/bin/bash

# Shell script to check what files are missing from WUVT's internet archive
# input format: 
#   <script> -d [date specification] -- check all archives from date to today
#   <script> -e [missing file] -- check all archives listed in missing file
# 
# writes to missing_files.txt

#DEPS:
# curl

OUTPUTFILE='missing_files.txt'
TODAY=$(date +%s)
FILESTOCHECK=''

# check if file exists. return 0 if it does
check_file() {
	FILESPEC=$1
	if [[ $(curl -I -L https://retrofling.apps.wuvt.vt.edu/$FILESPEC\
		2>/dev/null | grep '404 Not Found' ) ]]; then
		return 1
	else
		return 0
	fi
}

if [[ $1 = '-e' ]]; then
	INPUTFILE=$2
	for line in $(cat $INPUTFILE); do
		FILESTOCHECK+=" $line"
	done

elif [[ $1 = '-d' ]]; then
	STARTDATE=$(date -u -d $2 +%s)
	for (( INDEXDATE=$STARTDATE ; $TODAY > $INDEXDATE ;\
		INDEXDATE=3600+$INDEXDATE ))
	do
		FILESTOCHECK+=" $(date -u -d @$INDEXDATE +WUVTFM_%Y%m%d_%H00Z)"
	done
else
	echo "Must provide either -d [start date] or -e [file]" >&2
	exit 1
fi

for FILE in $FILESTOCHECK; do
	check_file $FILE
	if [[ $? = 1 ]]
	then
		echo $FILE >> $OUTPUTFILE
		echo "$FILE not found" >&2
#	else
#		echo "$FILE found" >&2
	fi
done
