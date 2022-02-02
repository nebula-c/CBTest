#!/bin/zsh

oneana(){
	
	cd $1
	cd digital
	
	rm ./*png

	rawfile=`find . -name "*.raw"`
	datfile=`find . -name "*.dat"`
	alpide-digitalana $rawfile $datfile

	echo "============================="
	echo "$1: digitalana is done"
	echo "============================="
	
	cd ../..
}

oneana 3_235A
#oneana 2_024C
#oneana 4_024C_2
#oneana 5_011B
#oneana 6_012B
#oneana 7_051C
