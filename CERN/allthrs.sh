#!/bin/zsh


oneana(){
	
	cd $1
	cd thrscan

	rawfile=`find . -name "*.raw"`
	jsonfile=`find . -name "*.json"`
	alpide-thrscanana $rawfile $jsonfile

	echo "============================="
	echo "thrscanana is done"
	echo "============================="
	
	cd ../..
}


oneana 2_024C
oneana 4_024C_2
oneana 5_011B
oneana 6_012B
oneana 7_051C
