#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 09:15:13 2021

@author: rdel1cmc
"""

#write a script that calculates the length of drawdown of at least 5 days within a season or year of each lake. for the drawdown length, i need to calculate the %difference over that time period. Also need to output the start date and end date of the drawdown period.
#the way we are going to handle decimal points is that we will round to the nearest 0.5 ft. So the tenth place will either be 0 or 5.


#read in the .csv file

import pandas as pd
import collections
import os




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



def ReadElevationData(filename):
    return pd.read_csv(filename, index_col ="Date")


#apply a rounding rule to the elevation data in each csv cell


def rounding_off(number):
    return round(number*5)/5

    
#compare the elevation of each date and see if there is an increase or decrease (i.e., day 1 vs day 2; day 2 vs day 3)
def elev_decrease(number1,number2):
    return(number2 < number1)
    
    
    
def elev_decrease_equal(number1, number2):
    #number1 = rounding_off(number1)
    #number2 = rounding_off(number2)
    return (number2 <= number1)
    
#if Day X is less or equal to Day Y, then that is included in the drawdown period.
def drawdown_check(list, number1, number2):
    number1 = rounding_off(number1)
    number2 = rounding_off(number2)
    if (elev_decrease_equal(number1,number2)):
        list.append(number1)
        return True
    else:
        list.append(number1)
        return False
        
#if the duration is less than 5 days, then it doesn't count as a drawdown event.
def duration_check(list):
    if len(list) < 5:
        return False
    else:
        return True
    
def drawdown_frequency(frequency):
    return (collections.Counter(frequency))

def percent_drawdown_time(number):
    return (number/365)

def avg_drawdown_length(x,y):
    return(x/y)

def rate_of_change(duration, elevation):
    return(elevation/duration)
    

def percent_difference(x,y):
    return (y-x)/x

def sum_percent_difference(values):
    return(sum(values))



#repeat the loop until there is an increase in elevation.

def drawdown_list(elev_data, start_date, end_date):
    start_index = elev_data.index.get_loc(start_date)
    end_index = elev_data.index.get_loc(end_date)
    OutputList = []
    list = []
    for index in range(end_index-start_index):
        if (not drawdown_check(list,elev_data.iloc[start_index+index,0], elev_data.iloc[start_index+index+1,0])):
            if(duration_check(list)):
                date1 = elev_data.index[start_index+index-len(list)+1]
                date2 = elev_data.index[start_index+index]
                OutputList.append([date1,date2,len(list),list[0],list[len(list)-1], percent_difference(list[0],list[len(list)-1])])
            list = []
    return (OutputList)

#output a .csv or .xlsx file that will spit out the start date, end date, start elevation, end elevation, percent difference of that duration

def writeSimplePercentDifferenceCSV(filename, ListofList):
    out_file = open(filename, "w")
    out_file.write("Start Date, End Date, Duration, Start Elevation, End Elevation, Percent Difference\n")
    for i in range(len(ListofList)):
        out_file.write(str(ListofList[i][0]) + "," + str(ListofList[i][1]) + "," + str(ListofList[i][2]) + "," + str(ListofList[i][3]) + "," + str(ListofList[i][4]) + "," + str(ListofList[i][5]) + "\n")
    out_file.close()
    
# Main
pathname = "/Users/rdel1cmc/Desktop/rdel1cmc/Desktop/Carra_ACE-IT_computer/wetlands_and_coastal/todd/bureau_of_reclamation/FY21_Info/Yale_Project/YaleProject/"
filename = "Metadata_File_for_runs.csv"
readmetadatafile = readfilename(pathname + filename)

def GetOnlyFilename(filename):
    return os.path.basename(filename).split('.', 1)[0]

filename = "path/to/something.csv"
testing = GetOnlyFilename(filename)
print(testing)

'''
file_dimensions = filedimensions(readmetadatafile)
i=1
for i in range(file_dimensions):
    print("The file name is: {}".format(readCSVfile(readmetadatafile,i)))
    print(readCSVfile(readmetadatafile,i)) 
    ElevationDataFrame = ReadElevationData(pathname + readCSVfile(readmetadatafile,i))
    print(ElevationDataFrame)
    print(os.path.splitext(readmetadatafile))

    start_date = getstartdate(readmetadatafile,i)
    end_date = getenddate(readmetadatafile,i)
#start_date = "1/1/97"
#end_date = "1/1/98"
    ListOfList = drawdown_list(ElevationDataFrame, start_date, end_date)
    writeSimplePercentDifferenceCSV("Trial_" + "_Duration_" + 'csv', ListOfList)
'''    










