# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 10:20:11 2022

@author: RDEL1CMC
"""

##This script is going to look through csv file, compare dates, and if dates are duplicated, then 
##the duplicated date is going to be removed from the dataset.

#read in csv file

#start at day 1 in date column

#compare day1 to day1+1. If day1 == day1 + 1 halt program and report duplication occurred

import pandas as pd
import os
import numpy as np
import sys 


data = pd.read_csv("C:/Users/RDEL1CMC/Desktop/Yale_Project/YaleProject/Habitat_hydrological_data_2021-04-20/Established_Elevation_csv/Apache_Lake_elevation_daily.csv")

for i in data:
    date = data.loc[:,"Date"]
    print(date.to_string(index=False))
