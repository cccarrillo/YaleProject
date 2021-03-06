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
import os
import numpy as np



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
    return round(number*1)/1

    
#compare the elevation of each date and see if there is an increase or decrease (i.e., day 1 vs day 2; day 2 vs day 3)
def elev_decrease(number1,number2):
    number1 = rounding_off(number1)
    number2 = rounding_off(number2)
    return(number2 < number1)
    
    
    
def elev_decrease_equal(number1, number2):
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
    
def get_year(date):
    date_df = pd.to_datetime(date,format= '%m/%d/%y')
    date_year = date_df.year
    return date_year

def list_frequency(lists):
    return len(lists)
    
def yearly_percent_drawdown(list):
    durations = []
    for i in range(len(list)):
        durations.append(list[i][2])
    return sum(durations)/365

def avg_drawdown_length(list):
    durations = []
    for i in range(len(list)):
        durations.append(list[i][2])
    return sum(durations)/len(durations)

def avg_percent_difference(list):
    difference = []
    for i in range(len(list)):
        difference.append(list[i][5])
    return sum(difference)/len(difference)

def avg_slope(list):
    slope = []
    for i in range(len(list)):
        slope.append(list[i][6])
    return sum(slope)/len(slope)

def rate_of_change(list):
    point1 = list[0]
    point2 = list[-1]
    length = len(list)-1
    slope = (point2 - point1)/length
    return slope

def drawdown_standard_deviation(list):
    duration = []
    for i in range(len(list)):
        duration.append(list[i][2])
    return np.std(duration)

def percent_standard_deviation(list):
    difference = []
    for i in range(len(list)):
        difference.append(list[i][5])
    return np.std(difference)

def slope_standard_deviation(list):
    slope = []
    for i in range(len(list)):
        slope.append(list[i][6])
    return np.std(slope)
    


def percent_difference(x,y):
    return (y-x)/x

def drawdown_difference(x,y):
    return(y-x)

def GetOnlyFilename(filename):
    return os.path.basename(filename).split('.', 1)[0]

#repeat the loop until there is an increase in elevation.

def drawdown_list(elev_data, start_date, end_date):
    start_index = elev_data.index.get_loc(start_date)
    end_index = elev_data.index.get_loc(end_date)
    OutputList = []
    list = []
    DiscardedList = []
    for index in range(end_index-start_index):
        if (len(list)==0):
            if (elev_decrease(elev_data.iloc[start_index+index,0], elev_data.iloc[start_index+index+1,0])):
                list.append(rounding_off(elev_data.iloc[start_index+index,0]))
        elif (not drawdown_check(list,elev_data.iloc[start_index+index,0], elev_data.iloc[start_index+index+1,0])):
            if(duration_check(list)):
                date1 = elev_data.index[start_index+index-len(list)+1]
                date2 = elev_data.index[start_index+index]
                slope = rate_of_change(list)
                OutputList.append([date1,date2,len(list),list[0],list[len(list)-1], percent_difference(list[0],list[len(list)-1]),slope, drawdown_difference(list[0],list[len(list)-1])])
            elif (len(list) < 5):
                date1 = elev_data.index[start_index+index-len(list)+1]
                date2 = elev_data.index[start_index+index]
                DiscardedList.append([date1,date2,len(list),list[0],list[len(list)-1], drawdown_difference(list[0], list[len(list)-1])]) 
            list = []
        elif (len(list) >= 10):
            if list[len(list)-1] - list[len(list)-5] == 0:
                date1 = elev_data.index[start_index+index-len(list)+1]
                date2 = elev_data.index[start_index+index]
                slope = rate_of_change(list)
                OutputList.append([date1,date2,len(list),list[0],list[len(list)-1], percent_difference(list[0],list[len(list)-1]),slope, drawdown_difference(list[0],list[len(list)-1])])             
                list = []
                
                
            
    return (OutputList, DiscardedList)


def MetricsList(lists):
    mydict = {}
    for i in range(len(lists)):
        if (mydict.__contains__((get_year(lists[i][0])))):
            mydict[get_year(lists[i][0])].append(lists[i])
        else:
            mydict[get_year(lists[i][0])] = [lists[i]]
    return mydict

def max_daily_drawdown_list(list):
    drawdown = 0
    for i in range(len(list)):
        elev1 = list[i][3]
        elev2 = list[i][4]
        elev_difference = elev2 - elev1
        if elev_difference < drawdown:
            drawdown = elev_difference
    return drawdown

def daily_elev_decrease(number1,number2):
   
    return(number2 < number1)

def daily_drawdown_check(list, number1, number2):
    if (daily_elev_decrease(number1,number2)):
        list.append(number1)
        return True
    else:
        list.append(number1)
        return False
    
def daily_drawdown_list(panda_dataframe, start_date, end_date):
    start_index = panda_dataframe.index.get_loc(start_date)
    end_index = panda_dataframe.index.get_loc(end_date)
    daily_drawdown = 0
    OutputList = []
    list = []
    for index in range(end_index-start_index):
        if (daily_elev_decrease(panda_dataframe.iloc[start_index+index,0], panda_dataframe.iloc[start_index+index+1,0])):
            date1 = panda_dataframe.index[start_index+index-len(list)+1]
            date2 = panda_dataframe.index[start_index+index]
            elev1 = panda_dataframe.iloc[start_index+index,0]
            elev2 = panda_dataframe.iloc[start_index+index+1,0]
            elev_difference = elev2 - elev1
            if elev_difference < daily_drawdown:
                daily_drawdown = elev_difference
            OutputList.append([date1, date2, len(list), elev1, elev2, daily_drawdown])
            list = []
    return OutputList

def max_daily_drawdown(panda_dataframe, start_date, end_date):
    start_index = panda_dataframe.index.get_loc(start_date)
    end_index = panda_dataframe.index.get_loc(end_date)
    max_start_date = ""
    daily_drawdown = 0
    for index in range(end_index - start_index):
        elev1 = panda_dataframe.iloc[start_index+index,0]
        elev2 = panda_dataframe.iloc[start_index+index+1,0]
        elev_difference = elev2 - elev1
        if elev_difference < daily_drawdown:
            daily_drawdown = elev_difference
            #max_start_date = panda_dataframe.index[start_index+index]
    return daily_drawdown
    
 

#output a .csv or .xlsx file that will spit out the start date, end date, start elevation, end elevation, percent difference of that duration

def writeSimplePercentDifferenceCSV(filename, ListofList):
    out_file = open(filename, "w")
    out_file.write("Start Date, End Date, Duration, Start Elevation, End Elevation, Percent Difference, Rate of Change, Drawdown\n")
    for i in range(len(ListofList)):
        out_file.write(str(ListofList[i][0]) + "," + str(ListofList[i][1]) + "," + str(ListofList[i][2]) + "," + str(ListofList[i][3]) + "," + str(ListofList[i][4]) + "," + str(ListofList[i][5]) + "," + str(ListofList[i][6]) + "," + str(ListofList[i][7]) + "\n")
    out_file.close()

def write_less_five_day_drawdown_CSV(filename, ListofList):
    out_file = open(filename, "w")
    out_file.write("Start Date, End Date, Duration, Start Elevation, End Elevation, Drawdown\n")
    for i in range(len(ListofList)):
        out_file.write(str(ListofList[i][0]) + "," + str(ListofList[i][1]) + "," + str(ListofList[i][2]) + "," + str(ListofList[i][3]) + "," + str(ListofList[i][4]) + "," + str(ListofList[i][5]) + "\n")
    out_file.close()

def write_yearly_metrics_csv(filename, list):
    
    out_file = open(filename, "w")
    out_file.write("Year, Number of Drawdowns, Percent of Year in Drawdown, Average Days of Drawdown, SD of Drawdown, Average Percent Difference, SD Percent Difference, Average Rate of Change, SD Rate of Change, Max Daily Drawdown\n")
    for key in list:
        listfrequency = list_frequency(data_yearly_dict[key])
        yearlydrawdown = yearly_percent_drawdown(data_yearly_dict[key])
        averagedrawdown = avg_drawdown_length(data_yearly_dict[key])
        SDdrawdown = drawdown_standard_deviation(data_yearly_dict[key])
        averagepercent = avg_percent_difference(data_yearly_dict[key])
        SDpercent = percent_standard_deviation(data_yearly_dict[key])
        averageslope = avg_slope(data_yearly_dict[key])
        SDslope = slope_standard_deviation(data_yearly_dict[key])
        DailyDrawdown = max_daily_drawdown_list(Raw_yearly_dict[key])
        out_file.write(str(key) + "," + str(listfrequency) + "," + str(yearlydrawdown) + "," + str(averagedrawdown) + "," + str(SDdrawdown) + "," + str(averagepercent) + "," + str(SDpercent) + "," + str(averageslope) + "," + str(SDslope) + "," + str(DailyDrawdown) + "\n")
    out_file.close()


# Main
pathname = "/Users/rdel1cmc/Desktop/rdel1cmc/Desktop/Carra_ACE-IT_computer/wetlands_and_coastal/todd/bureau_of_reclamation/FY21_Info/Yale_Project/YaleProject/"
filename = "Metadata_File_for_runs.csv"
readmetadatafile = readfilename(pathname + filename)



file_dimensions = filedimensions(readmetadatafile)

output_file = open("Max_Daily_Drawdown_1ft_.csv", "w")
output_file.write("Lake Name, Max Daily Drawdown\n")
for i in range(file_dimensions):
    print("The file name is: {}".format(readCSVfile(readmetadatafile,i)))
    ElevationDataFrame = ReadElevationData(pathname + readCSVfile(readmetadatafile,i))

    start_date = getstartdate(readmetadatafile,i)
    end_date = getenddate(readmetadatafile,i)

    ListOfList, DiscardedListofList = drawdown_list(ElevationDataFrame, start_date, end_date)
    
    UnRoundedList = daily_drawdown_list(ElevationDataFrame, start_date, end_date)
    Raw_yearly_dict = MetricsList(UnRoundedList) 

    
    writeSimplePercentDifferenceCSV(GetOnlyFilename(readCSVfile(readmetadatafile,i)) + "_Duration_1FT_" + '.csv', ListOfList)
    data_yearly_dict = MetricsList(ListOfList)
    write_yearly_metrics_csv(GetOnlyFilename(readCSVfile(readmetadatafile,i)) + "_Metrics_1FT_" + '.csv', data_yearly_dict)
    write_less_five_day_drawdown_CSV(GetOnlyFilename(readCSVfile(readmetadatafile,i)) + "_Less_5_Days_1FT_" + ".csv", DiscardedListofList)
    
    #print(max_daily_drawdown(ElevationDataFrame, start_date, end_date))
    output_file.write(str(GetOnlyFilename(readCSVfile(readmetadatafile,i))) + "," + str(max_daily_drawdown(ElevationDataFrame, start_date, end_date)) + "\n")
output_file.close() 





