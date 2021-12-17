#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 09:15:13 2021

@author: rdel1cmc
"""

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

def find_local_max_min(dataframe):
    dataframe['Max/Min'] = dataframe['Diff']+0.0000001 * dataframe['Diff'].shift(-1) < 0
    return

def get_local_max_min_points(dataframe):
    return dataframe[dataframe['Max/Min'] == True]

def find_local_max(dataframe):
    dataframe['SecondDiff'].iloc[0] = 0.0
    dataframe['SecondDiff'].iloc[-1] = 0.0
    return dataframe[dataframe['SecondDiff'] <= 0.0]

def second_Derivative(dataframe):
    '''This function takes the second derivative of elevation difference with respect to time. it incorporates the elevation_difference function.'''
    dataframe['SecondDiff'] = dataframe['Diff'].diff().shift(-1)
    return

def rounding(dataframe, value):
    dataframe['Elevation (ft)'] = dataframe['Elevation (ft)'].apply(lambda x:round(x*value)/value)
    return
    
test = ReadElevationData('/Users/rdel1cmc/Desktop/rdel1cmc/Desktop/Carra_ACE-IT_computer/wetlands_and_coastal/todd/bureau_of_reclamation/FY21_Info/Yale_Project/YaleProject/Data/Negative_Elevation_csv/Platoro_Reservoir_elevation_daily.csv')
test['Date']=pd.to_datetime(test['Date'])
test.sort_values(by='Date',inplace=True)
 
truncated_data = truncate_dataframe(test, "5/01/19", "6/01/19")

rounding(truncated_data,2)

elevation_difference(truncated_data)
truncated_data.plot(x='Date', y='Diff')
truncated_data.plot(x='Date', y='Elevation (ft)')
plt.show()

second_Derivative(truncated_data)
find_local_max_min(truncated_data)

print(truncated_data)


temp = get_local_max_min_points(truncated_data)
temp = find_local_max(temp)

ax = truncated_data.plot(x='Date', y='Elevation (ft)')
temp.plot.scatter(x='Date', y='Elevation (ft)', ax = ax, c='Red')
plt.show()
