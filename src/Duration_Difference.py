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
import matplotlib.pyplot as plt


def ReadElevationData(filename):
    """This function will read the csv input file (expected format "date, elevation") and index it based on the date column."""
    return pd.read_csv(filename)



def truncate_dataframe(dataframe, startdate, enddate):
    '''This function will take in the dataframe, start date, and end date and truncate the data along those values'''
    return dataframe.truncate(before=dataframe['Date'][dataframe['Date']==pd.to_datetime(startdate)].index[0], after=dataframe['Date'][dataframe['Date']==pd.to_datetime(enddate)].index[0])


def elevation_difference(dataframe):
    '''this function will take in the dataframe and then find the difference in elevation moving 1 day at a time'''
    dataframe['Diff'] = dataframe['Elevation (ft)'].diff()
    return 

test = ReadElevationData('/Users/rdel1cmc/Desktop/rdel1cmc/Desktop/Carra_ACE-IT_computer/wetlands_and_coastal/todd/bureau_of_reclamation/FY21_Info/Yale_Project/YaleProject/Data/Negative_Elevation_csv/Platoro_Reservoir_elevation_daily.csv')
test['Date']=pd.to_datetime(test['Date'])
test.sort_values(by='Date',inplace=True)
#test.plot(x='Date')
#plt.show()


 
truncated_data = truncate_dataframe(test, "5/01/19", "5/11/19")


elevation_difference(truncated_data)
truncated_data.plot(x='Date', y='Diff')
truncated_data.plot(x='Date', y='Elevation (ft)')
plt.show()
print(truncated_data)

