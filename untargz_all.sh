#!/bin/bash

if [ $# -lt 1 ]; then
	echo "Usage: $(basename $0) FOLDER"
	exit 1
fi

FOLDER=$1

find $FOLDER -name "*.tar.gz" -print0 |
	while IFS= read -r -d $'\0' f; do
		FILE_DEST=$(dirname $f)
		DESTFOLDER=${f%.tar.gz}
		mkdir $DESTFOLDER
		tar -C $DESTFOLDER -xvzf $f
	done
