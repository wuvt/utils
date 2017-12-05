#!/bin/bash
#dumps access databases to csv of each table in current dir.
#requires https://github.com/brianb/mdbtools
DATABASE="$1"
mdb-tables "$DATABASE" -d, | while IFS= read -r -d , table;
do
	FILENAME=$(echo "$table"|sed s/\ /_/g)
	mdb-export "$DATABASE" "$table" >> $FILENAME.csv
done
