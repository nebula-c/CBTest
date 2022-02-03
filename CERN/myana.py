import mydigtalscan
import mythrscanana
import mythrshist
import power_mean
import mydacana_V
import mydacana_I
import pastdac_I
import pastdac_V
import seperate_IV

#chips = ["1_023C"]
chips = ["1_023C", "2_024C", "4_024C_2", "5_011B", "6_012B", "7_051C"]

for chip in chips:
    #mythrscanana.Run(f"{chip}/thrscan/")
    #mythrshist.Run(f"{chip}/thrscan/")
    #pastdac_I.Run(f"{chip}/past-dac/")
    #pastdac_V.Run(f"{chip}/past-dac/")
    #seperate_IV.OnlyV(f"{chip}/dac/")
    #seperate_IV.OnlyI(f"{chip}/dac/")
    mydacana_I.Run(f"{chip}/dac/")
    mydacana_V.Run(f"{chip}/dac/")
