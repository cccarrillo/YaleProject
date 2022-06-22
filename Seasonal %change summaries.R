# Seasonal summarization of % percent change

library(reshape2)
library(stringr)
library(lubridate)
library(dplyr)
library(ggplot2)

#### Seasonal and Yearly-Seasonal %change summaRY C#SV file creation #### -----------------------------------------------------------------------------------------------------------------

# Below is a loop that converts each individual elevation % change file (both 7 and 28 day step sizes) into a seasonal summarisation graph

# Folder where all the needed files are

setwd("C:/Users/RDEL1CMC/Desktop/Yale_Project/YaleProject/src")
options(warn = 1) # prints warnings as they occur

files <- list.files() #list of all files in folder
files_D <- files[grepl('_Duration_0.2_FT', files)] # pulls out duration files
files_M <- files[grepl('_Metrics_0.2_FT', files)] #i pulls out Metrics files

# Columns names for each file are are funky so reformat for R
New_colnames <- c("Start_date", "End_date", "Duration", "Start_elevation", "End_elevation", "Percent_Diff", "Rate_of_Change", "Drawdown")

# Define which months we want to put in each season
Spring <- c('March', 'April', 'May')
Summer <- c('June','July','August')
Fall <- c('September', 'October', 'November')
Winter <- c('December','January','February')

#******************************************************************************************************
# Definitions to change depending on which set of files/folder you want to use

#filesMain <- files_D # uncomment one filesMain
#folder <- 'Duration' # uncomment one folder
 
filesMain <- files_M # uncomment one filesMain
folder <- 'Metrics' # uncomment one folder
#******************************************************************************************************

# NESTED FOR LOOP for CSV file creation
for (i in 1:length(filesMain)){ # cycle through each file in set
  fileTrip <- filesMain[i] # choose file to access for loop
  setwd(paste("C:/Users/RDEL1CMC/Desktop/Yale_Project/YaleProject/Results/", folder, sep = '')) #adjust directory for this iteration
  print(paste('Now running :', str_split_fixed(fileTrip,"_", n = 5)[1],str_split_fixed(fileTrip,"_", n = 5)[2], ': Number', i, 'of', length(filesMain), 'lakes', sep =' '))
  
  # inner loop that manipulates each file to get a seasonal % change summary
  for (j in 1:length(fileTrip)){
    data <- read.csv(paste('C:/Users/RDEL1CMC/Desktop/Yale_Project/YaleProject/src/', fileTrip, sep = '')) # read in the csv
    colnames(data) <- New_colnames #change the col names 
    data$Start_date <-as.Date(data$Start_date, format = "%m/%d/%y") # put start date in date format
    data$Year <- format(data$Start_date, format = '%Y') # create a year col for the start date
    data$Month <- month(data$Start_date, label = T, abbr = F) # create a month col for the start date
    # create a season col depending on the moneht of the start date
    data$Season <- ifelse(data$Month %in% Spring, "Spring",
                          ifelse(data$Month %in% Summer, "Summer",
                                 ifelse(data$Month %in% Fall, "Fall","Winter")))
    # get the seasonal mean (across years) of %change in elevation
    seasonal_datasum <- data %>% group_by(Season) %>% 
      summarise(n = length(!is.na(Percent_Diff)),
                mean_Prop_Diff = mean(Percent_Diff, na.rm = T), sd_Prop_Diff = sd(Percent_Diff, na.rm = T), 
                mean_Perc_Diff = mean(Percent_Diff*100, na.rm = T), sd_Perc_Diff = sd(Percent_Diff*100, na.rm = T))
    # get the Annual seasonal mean of %change in elevation
    yearseason_datasum <- data %>% group_by(Year,Season) %>% 
      summarise(n = length(!is.na(Percent_Diff)), 
                mean_Prop_Diff = mean(Percent_Diff, na.rm = T), sd_Prop_Diff = sd(Percent_Diff, na.rm = T), 
                mean_Perc_Diff = mean(Percent_Diff*100, na.rm = T), sd_Perc_Diff = sd(Percent_Diff*100, na.rm = T))
  }
  
  # Goes along with i loop to add new file to Seasonal %change summaries folder
  filename1 <- paste(str_split_fixed(fileTrip,".csv", n = 2)[1], '_Seasonal.csv', sep = '')
  filename1 <- paste(getwd(), '/', filename1, sep = '')
  write.csv(seasonal_datasum, file = filename1)
  
  filename2 <- paste(str_split_fixed(fileTrip,".csv", n = 2)[1], '_YearlySeasonal.csv', sep = '')
  filename2 <- paste(getwd(), '/', filename2, sep = '')
  write.csv(yearseason_datasum, file = filename2)
}

#### GGPLOT CREATION #### -----------------------------------------------------------------------------------------------------------------


#******************************************************************************************************
# Definitions to change depending on which set of files/folder you want to use
# Folder where all the needed files are

#folder2 <- 'Duration' # uncomment one folder2
folder2 <- 'Metrics' # uncomment one folder2

#******************************************************************************************************

setwd(paste('C:/Users/RDEL1CMC/Desktop/Yale_Project/YaleProject/Results/', folder2, sep = ''))
options(warn = 1) # prints warnings as they occur

files2 <- list.files() #list of all files in folder
files_sznl <- files2[grepl('_Duration_0.2_FT', files2)] # pulls out 7_Days files
files_yrsznl <- files2[grepl('_Metrics_0.2_FT', files2)] # pulls out 28_Days files

#******************************************************************************************************
# Definitions to change depending on which set of files/folder you want to use
# plots will differ depending on the data organization 

#filesMain2 <- files_sznl # uncomment one filesMain2
filesMain2 <- files_yrsznl # uncomment one filesMain2

#******************************************************************************************************

# NESTED FOR LOOP for ggplot creation
for (i in 1:length(filesMain2)){ # cycle through each file in set
  fileTrip <- filesMain2[i] # choose file to access for loop
  setwd(paste('C:/Users/RDEL1CMC/Desktop/Yale_Project/YaleProject/Results/', folder2, sep = '')) #adjust directory for this iteration
  print(paste('Now running :', str_split_fixed(fileTrip,"_", n = 6)[1],str_split_fixed(fileTrip,"_", n = 6)[2], ': Number', i, 'of', length(filesMain2), 'lakes', sep =' '))
  
  # inner loop that manipulates each file to get a seasonal % change summary
  for (j in 1:length(fileTrip)){
    data <- read.csv(paste('C:/Users/RDEL1CMC/Desktop/Yale_Project/YaleProject/Results/',folder2,'/',fileTrip, sep = ''))[,-1] # read in the csv
    data$Season <- factor(data$Season, levels = c('Spring','Summer','Fall','Winter'))
    
    if(grepl('_Duration', fileTrip)) {
      plot <- ggplot(data) + geom_bar(stat = 'identity', position = 'dodge', size = 1, aes(x = Season, y = mean_Perc_Diff, fill = Season)) + 
        geom_errorbar(aes(x = Season, ymin = mean_Perc_Diff-sd_Perc_Diff, ymax = mean_Perc_Diff+sd_Perc_Diff), position = position_dodge(0.9), width = 0.1, size = 1) +
        labs(x = "Season", y = "Percent (%) Change in Elevation [Mean +/- SD ]") + theme_classic() + theme(legend.position = 'none') + 
        ggtitle(paste(str_split_fixed(fileTrip,"_", n = 6)[1], str_split_fixed(fileTrip,"_", n = 6)[2], ": Seasonal", sep = " ")) 
      }
    
    if(grepl('_Metrics', fileTrip)) {
      plot <- ggplot(data) + geom_bar(stat = 'identity', position = 'dodge', size = 1, aes(x = as.factor(Year), y = mean_Perc_Diff, fill = Season)) + 
        geom_errorbar(aes(group = Season, x = as.factor(Year), ymin = mean_Perc_Diff-sd_Perc_Diff, ymax = mean_Perc_Diff+sd_Perc_Diff), position = position_dodge(0.9), width = 0.1, size = 0.01) +
        labs(x = "Year", y = "Percent (%) Change in Elevation [Mean +/- SD ]") + theme_classic() + theme(legend.position = 'bottom') + 
        ggtitle(paste(str_split_fixed(fileTrip,"_", n = 6)[1], str_split_fixed(fileTrip,"_", n = 6)[2], ": Yearly Seasonal", sep = " ")) 
    }
  }
  
  # Goes along with i loop to add new file to Seasonal %change summaries folder
  filename <- paste(str_split_fixed(fileTrip,".csv", n = 2)[1], '_plot.pdf', sep = '')
  if(grepl('_Duration', fileTrip)) {
    w = 4; h = 4
  }
  if(grepl('_Metrics', fileTrip)) {
    w = 8; h = 4
  }
  pdf(filename, width = w, height = h) #creates the pdf by the file named above
  print(plot) #prints plot to pdf
  dev.off() #closes file
  
}


