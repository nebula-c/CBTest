import mydigtalscan
import mythrscanana
import mythrshist

chips = ["1_023C", "2_024C", "4_024C_2", "5_011B", "6_012B", "7_051C"]

for chip in chips:
    #mythrscanana.Run(f"{chip}/thrscan/")
    mythrshist.Run(f"{chip}/thrscan/")
