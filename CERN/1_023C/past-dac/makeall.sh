#!/bin/zsh

testname=(VRESETP VRESETD VCASP VCASN VPULSEH VPULSEL VCASN2 VCLIP VTEMP IAUX2 IRESET IDB IBIAS ITHR)

for ((i=1;i<=14;i++))
do
	mytest=${testname[i]}.txt	

	while read line; do
		if [[ $line == *value* ]]; then
			continue
		fi
	echo "${testname[i]}\t$line" >>past.txt
	done < $mytest
        echo ${testname[i]} is done
done
