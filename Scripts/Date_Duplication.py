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


def readfilename(filename):
    return pd.read_csv(filename)

def readCSVfile(filename, index):
    return filename.iloc[index,0] #pulling out a row and a column 

def getstartdate(filename,index):
    return filename.iloc[index,1]

def getenddate(filename,index):
    return filename.iloc[index,2]

def filedimensions(filename):
    return filename.shape[0]

def BeginRepeatCheck(filename):
    return pd.read_csv(filename, index_col ="Date")

def date_check(panda_dataframe, start_date, end_date):
    start_index = panda_dataframe.index.get_loc(start_date)
    end_index = panda_dataframe.index.get_loc(end_date)
    #OutputList = []
    
    #list = []
    for i in range(end_index - start_index): 
        if start_index == start_index + i+1:
            sys.exit('Duplication Occurred')
    #return ("Duplication occurred at: {}".format(start_index))
    

pathname = "C:/Users/RDEL1CMC/Desktop/Yale_Project/YaleProject/"
filename = "Metadata_File_for_runs.csv"
readmetadatafile = readfilename(pathname + filename)

file_dimensions = filedimensions(readmetadatafile)

for i in range(file_dimensions):
    print("The file name is: {}".format(readCSVfile(readmetadatafile,i)))
    DateFrame = BeginRepeatCheck(pathname + readCSVfile(readmetadatafile,i))
    
    begin_date = getstartdate(readmetadatafile,i)
    end_date = getenddate(readmetadatafile,i)
    trial = date_check(DateFrame, begin_date, end_date)

    