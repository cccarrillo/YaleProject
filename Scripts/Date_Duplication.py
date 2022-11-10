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


data = pd.read_csv("C:/Users/RDEL1CMC/Desktop/Yale_Project/YaleProject/Negative_Elevation_csv/Davis_Creek_Reservoir_elevation_daily.csv")

for i in data:
    list = []
    date = data.loc[:,"Date"]
    new_date = date.to_string(index=False)
    #print(new_date)
    #print("Start Date: {}".format(new_date))
    duplicate = date[date.duplicated()]
    list.append(duplicate)
    print("Duplicated Dates: {}".format(list))
   
    #removed_date = date.drop_duplicates() 
    #print(removed_date)
    
     
   # for i in list:
    #    list.remove(i)
    #print("New List: {}".format(list))
    


 


        
    
    
    