#!/bin/zsh

link=$1
list_file=$2

while read line; do
	echo ${link}${line}.txt >> path.txt
done < ${list_file}

wget --user=$3 --ask-password -i path.txt

rm path.txt
