#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 09:15:13 2021

@author: rdel1cmc
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

def ReadElevationData(filename):
    """This function will read the csv input file (expected format "date, elevation") and index it based on the date column."""
    return pd.read_csv(filename)

def readCSVfile(filename, index):
    return filename.iloc[index,0]

def filedimensions(filename):
    return filename.shape[0]

def GetOnlyFilename(filename):
    return os.path.basename(filename).split(".",1)[0]

def getstartdate(filename, index):
    return filename.iloc[index,1]

def getenddate(filename, index):
    return filename.iloc[index,2]

def truncate_dataframe(dataframe, startdate, enddate):
    '''This function will take in the dataframe, start date, and end date and truncate the data along those values'''
    return dataframe.truncate(before=dataframe['Date'][dataframe['Date']==pd.to_datetime(startdate)].index[0], after=dataframe['Date'][dataframe['Date']==pd.to_datetime(enddate)].index[0])

def elevation_difference(dataframe):
    '''this function will take in the dataframe and then find the difference in elevation moving 1 day at a time'''
    dataframe['Diff'] = dataframe['Elevation (ft)'].diff()
    return 

def find_local_max_min(dataframe):
    dataframe['Max/Min'] = dataframe['Diff']+0.0000001 * dataframe['Diff'].shift(-1) < 0
    #dataframe['Max/Min'].iloc[-1] = True
    return

def get_local_max_min_points(dataframe):
    return dataframe[dataframe['Max/Min'] == True]

def find_local_max(dataframe):
    #dataframe['SecondDiff'].iloc[0] = -1.0
    #dataframe['SecondDiff'].iloc[-1] = -1.0
    return dataframe[dataframe['SecondDiff'] < 0.0]

def second_Derivative(dataframe):
    '''This function takes the second derivative of elevation difference with respect to time. it incorporates the elevation_difference function.'''
    dataframe['SecondDiff'] = dataframe['Diff'].diff().shift(-1)
    return

def rounding(dataframe, value):
    dataframe['Elevation (ft)'] = dataframe['Elevation (ft)'].apply(lambda x:round(x*value)/value)
    return
    
def evaluation(dataframe, trundataframe, value):
    list = []
    output = []
    dataframe['Drawdown'] = False
    indexes = []
    toremove = []
    for index, row in trundataframe.iterrows():
        indexes.append(index)
    for i in range(len(indexes)-1):
        if (indexes[i+1] - indexes[i] < 5):
            if (dataframe['Elevation (ft)'].loc[indexes[i+1]] - dataframe['Elevation (ft)'].loc[indexes[i]] < 0):
                toremove.append(indexes[i+1])
    for j in range(len(toremove)):
        for i in range(len(indexes)-1):
            if (indexes[i+1] - indexes[i] < 5):
                if (dataframe['Elevation (ft)'].loc[indexes[i+1]] - dataframe['Elevation (ft)'].loc[indexes[i]] < 0):
                    if (indexes[i+1] == toremove[j]):
                        indexes.remove(toremove[j])
                        break
    for i in range(len(indexes)-1):
        if (indexes[i+1] - indexes[i] >= 5):
            if (dataframe['Elevation (ft)'].loc[indexes[i]] - dataframe['Elevation (ft)'].loc[indexes[i]+5] >= 1/value):
                start_date = dataframe['Date'].loc[indexes[i]]
                start_elevation = dataframe['Elevation (ft)'].loc[indexes[i]]
                for j in range(indexes[i+1]-indexes[i]):
                    dataframe['Drawdown'].loc[indexes[i]+j] = True
                    end_date = dataframe['Date'].loc[indexes[i]+j]
                    end_elevation = dataframe['Elevation (ft)'].loc[indexes[i]+j]
                duration = end_date - start_date
                duration = duration.total_seconds()/60/60/24
                percent_diff = (start_elevation - end_elevation)/(start_elevation) * 100
                rate_of_change = (end_elevation - start_elevation) / duration
                start_date = start_date.strftime('%Y-%m-%d %X')
                end_date = end_date.strftime('%Y-%m-%d %X')
                list.append([start_date, end_date, duration, start_elevation, end_elevation, percent_diff, rate_of_change])
    return list
    #return dataframe[dataframe['Drawdown'] == True]
    
def writeCSVFile(filename, listoflist):
    out_file = open(filename, "w")
    out_file.write("Start Date, End Date, Duration, Start Elevation, End Elevation, Percent Difference, Rate of Change\n")
    for i in range(len(listoflist[0])):
        out_file.write(str(listoflist[i][0]) + "," + str(listoflist[i][1]) + "," + str(listoflist[i][2]) + "," + str(listoflist[i][3]) + "," + str(listoflist[i][4]) + "," + str(listoflist[i][5]) + "," + str(listoflist[i][6]) + "\n")
    out_file.close()
    
    
    
pathname = "/Users/rdel1cmc/Desktop/rdel1cmc/Desktop/Carra_ACE-IT_computer/wetlands_and_coastal/todd/bureau_of_reclamation/FY21_Info/Yale_Project/YaleProject/Data/"
filename = "Metadata_File_for_runs.csv"
readmetadatafile = ReadElevationData(pathname + filename)
file_dimensions = filedimensions(readmetadatafile)

for i in range(file_dimensions):
    print("The file name is: {}".format(readCSVfile(readmetadatafile,i)))
    test = ReadElevationData(pathname + readCSVfile(readmetadatafile, i))
    test['Date']=pd.to_datetime(test['Date'])
    test.sort_values(by='Date',inplace=True)
    
    start_date = getstartdate(readmetadatafile, i)
    end_date = getenddate(readmetadatafile,i)
 
    truncated_data = truncate_dataframe(test, start_date, end_date)
    rounding_value = 2
    rounding(truncated_data,rounding_value)

    elevation_difference(truncated_data)
#truncated_data.plot(x='Date', y='Diff')
#truncated_data.plot(x='Date', y='Elevation (ft)')
#plt.show()

    second_Derivative(truncated_data)
    find_local_max_min(truncated_data)

    temp = get_local_max_min_points(truncated_data)

    temp = find_local_max(temp)

    listoflist = evaluation(truncated_data, temp, rounding_value)


    output = writeCSVFile(GetOnlyFilename(readCSVfile(readmetadatafile,i)) + "_Duration_1FT_" + ".csv", listoflist)

#print(drawdown_events)

#ax = truncated_data.plot(x='Date', y='Elevation (ft)')
#temp.plot.scatter(x='Date', y='Elevation (ft)', ax = ax, c='Red')
#plt.show()

