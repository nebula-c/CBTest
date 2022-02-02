#!/bin/zsh

oneana(){
	
	cd $1
	cd dac
	txtfile=`find . -name "*.txt"`
	alpide-dacana $txtfile
	cd ../

	echo "============================="
	echo "dacana is done"
	echo "============================="


	cd digital
	rawfile=`find . -name "*.raw"`
	datfile=`find . -name "*.dat"`
	alpide-digitalana $rawfile $datfile
	cd../

	echo "============================="
	echo "digitalana is done"
	echo "============================="

	cd analog
	rawfile=`find . -name "*.raw"`
	alpide-analogana $rawfile
	cd ../

	echo "============================="
	echo "analogana is done"
	echo "============================="

	cd thrscan
	rawfile=`find . -name "*.raw"`
	jsonfile=`find . -name "*.json"`
	alpide-thrscanana $rawfile $jsonfile
	cd ../

	echo "============================="
	echo "thrscanana is done"
	echo "============================="
	
	cd ../
}


oneana 024C_2
oneana 012B
oneana 051C


