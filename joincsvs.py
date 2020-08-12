# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 06:56:16 2019
@author: Chris
"""
# credited:
# https://stackoverflow.com/questions/9234560/find-all-csv-files-in-a-directory-using-python/12280052

import os
import glob
import pandas as pd

# set working directory
os.chdir("/home/maina/OpenSource/Photon/www.parliament.go.ke/")

# find all csv files in the folder
# use glob pattern matching -> extension = 'csv'
# save result in list -> all_filenames
extension = 'csv'
senators = [i for i in glob.glob('senator*.{}'.format(extension))]
mps = [i for i in glob.glob('mps*.{}'.format(extension))]
# print(all_filenames)

# combine all files in the list
combined_senator_csv = pd.concat([pd.read_csv(f) for f in senators])
combined_mp_csv = pd.concat([pd.read_csv(f) for f in mps])
# export to csv
combined_senator_csv.to_csv("senators.csv", index=False, encoding='utf-8-sig')
combined_mp_csv.to_csv("mps.csv", index=False, encoding='utf-8-sig')
