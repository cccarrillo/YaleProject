#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 07:53:26 2021

@author: rdel1cmc
"""

# import required libraries

import pandas as pd

import os



#read the data file

Lake_data = pd.read_csv("/Users/rdel1cmc/Desktop/rdel1cmc/Desktop/Carra ACE-IT computer/wetlands and coastal/todd/bureau of reclamation/FY21 Info/Yale Project/Habitat_hydrological_data_2021-04-20/Established_Elevation_csv/Lake_Mohave_Elevation_daily.csv")

#convert date column into datetime object

Lake_data['Date'] = Lake_data['Date'].astype('datetime64[ns]')

#convert daily data to weekly

weekly_data = Lake_data.groupby('Measurement').resample('W-Wed', label='right', closed='right', on='Date').sum().reset_index().sort_values(by='Date')
print(weekly_data)


#divide  by 7 function
def division_by_seven(x):
    return x/7


weekly_data_average = weekly_data['Elevation '].map(division_by_seven)
print(weekly_data_average)


weekly_data["AverageElevation"] = weekly_data_average

weekly_data.to_excel('/Users/rdel1cmc/Desktop/rdel1cmc/Desktop/Carra ACE-IT computer/wetlands and coastal/todd/bureau of reclamation/FY21 Info/Yale Project/Habitat_hydrological_data_2021-04-20/Established_Elevation_csv/Lake_Mohave_Consolidated.xlsx')



