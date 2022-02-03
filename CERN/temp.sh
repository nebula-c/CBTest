#!/bin/zsh

onerun(){

	cd $1/past-dac
	#mkdir Voltage Current
	rm ./*png ./*dat OnlyV.txt OnlyI.txt
	cd ../../
}

onerun 1_023C
onerun 2_024C
onerun 4_024C_2
onerun 5_011B
onerun 6_012B
onerun 7_051C
