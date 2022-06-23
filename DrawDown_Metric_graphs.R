# This script uses a for nested loop to create a (ggplot) Fig for each individual CSV file

# Install packages with: 
# install.packages('INSERT PACKAGE/LIBRARY NAME HERE')

# Load libraries needed
library(stringr) # for file name string manipulation
library(lubridate) # for date manipulations 
library(dplyr) # from the tidyverse - data manipulation
library(ggplot2) # for plotting
library(gridExtra) # for organizing multiple plots on a single page

# Below is a loop that converts each individual  file into a set of figures

# Folder where all the needed files are
setwd('/Users/rdel1cmc/Desktop/rdel1cmc/Desktop/Carra_ACE-IT_computer/wetlands_and_coastal/todd/bureau_of_reclamation/FY21_Info/Yale_Project/YaleProject/Results/Python_results/') 
options(warn = 1) # prints warnings as they occur

files <- list.files() #list of all files in folder

# Pulls out duration and metric files from full file list
file_duration <- files[grepl('Duration', files)]
file_metric <- files[grepl('Metrics', files)]

# Pulls out 0.2ft and 1ft files from duration and metric files
file_duration_0.2 <- file_duration[grepl('0.2_FT', file_duration)]
file_metric_0.2 <- file_metric[grepl('0.2_FT', file_metric)]
#file_duration_1 <- file_duration[grepl('1FT', file_duration)]
#file_metric_1 <- file_metric[grepl('1FT', file_metric)]

# Columns names for each file are are funky so reformat for R
# this is a vector of the names that will be used in the "J loop" below
New_dur_colnames <- c("Start_date", "End_date", "Duration", "Start_elevation", "End_elevation", "Percent_Diff", "Rate_of_Change", "Drawdown")
New_met_colnames <- c("Year", "Number_drawdowns", "Percent_yr_drawdown", "Mean_days_drawdown", "SD_days_drawdown", "Mean_percent_diff", "SD_percent_diff", "Mean_rate", "SD_rate", "Max_Daily_Drawdown")

# Define which months we want to put in each season
# This will be used in the "J loop" below
Spring <- c('March', 'April', 'May')
Summer <- c('June','July','August')
Fall <- c('September', 'October', 'November')
Winter <- c('December','January','February')
# Note: I set these to the month level for simplicity - 
# we can change them to the true date ranges of the seasons if needed (e.g., Spring = MARCH 22-JUNE 22)
# I think you'd want to use the seq() fxn to create a list of dates in that range...but I'd have to check

# Create vectors of single word unique identifiers for each lake and group by the mussel infestation statuses
# will be used in J loop to ID the status of each lake as the loop works through the file
est <- c('Apache', 'Canyon', 'Havasu', 'Mead', 'Mohave', 'Powell', 'Saguaro')
neg <- c('Calamus', 'Carter', 'Currant', 'Davis','Flatiron', 'Folsom', 'Keith', 
         'Kirwin', 'Estes','Tschida', 'Lost', 'Moon', 'Newton', 'Pactola', 'Paonia',
         'Pinewood', 'Platoro', 'Ruedi', 'Silver', 'Taylor','Trinity', 'Twin', 'Webster', 'Whiskeytown')
sus <- c('Angostura', 'Bartlett', 'Blue', 'Deer', 'Flaming','Green', 'Jordanelle', 
         'Elwell', 'Navajo', 'Pueblo','Theodore', 'Willard')

#************************************************
# LOOP TESTING!!!!

# When testing if a loop works: set i=1, then run the lines INSIDE each loop 
# (do not run any line that says for() until you know the code in the loop works and does what you want)

#i=1 #un-comment this for loop testing

#*******************************************


#******************************************************************************************************
# UNCOMMENT ONE SET OF FILESMAIN AND FOLDER PER RUN TO GET FIGS INTO NEW FOLDERS DEPENDING ON CSV/DATA TYPE

# Definitions to change depending on which set of files/folder you want to use

filesMain <- file_duration_0.2 # uncomment one filesMain
folder <- 'Duration_0.2ft' # uncomment one folder

#filesMain <- file_metric_0.2 # uncomment one filesMain
#folder <- 'Metric_0.2ft' # uncomment one folder

# filesMain <- file_duration_1 # uncomment one filesMain
# folder <- 'Duration_1ft' # uncomment one folder

#filesMain <- file_metric_1 # uncomment one filesMain
#folder <- 'Metric_1ft' # uncomment one folder
#******************************************************************************************************


# NESTED FOR LOOP for ggplot creation
# The beginning of the "I loop" is used to pull up each csv file in filesMain 
for (i in 1:length(filesMain)){ # cycle through each file in the folder
  
  fileTrip <- filesMain[i] # choose file to access for I loop
  
  # Adjust directory - where to put the graph made in the "J loop"
  setwd(paste('/Users/rdel1cmc/Desktop/rdel1cmc/Desktop/Carra_ACE-IT_computer/wetlands_and_coastal/todd/bureau_of_reclamation/FY21_Info/Yale_Project/YaleProject/Results/', folder, sep = '')) 
  
  # Depending on the name of each csv file in the folder this print() line will need to change:
  # unlist(strsplit()) takes the name of the file (fileTrip) and splits it at the symbol in the quotes: in this case an upper or lowercase "_Elevation_"
  # The [1] says print the first segment before the split symbol
  # Test this line with i=1 to see what this looks like in practice
  # This line helps you keep track of what files are throwing warnings/errors if they occur
  print(paste('Now running :', unlist(strsplit(fileTrip, "(?i:_Elevation_)",perl=T))[1], ': Number', i, 'of', length(filesMain), 'lakes', sep =' '))

  # This J loop manipulates each file to create a figure from the data
  for (j in 1:length(fileTrip)){
    
    # Read in the csv
    data <- read.csv(paste('/Users/rdel1cmc/Desktop/rdel1cmc/Desktop/Carra_ACE-IT_computer/wetlands_and_coastal/todd/bureau_of_reclamation/FY21_Info/Yale_Project/YaleProject/Results/Python_results/',fileTrip, sep = '')) 
    
    if(grepl('Duration', fileTrip)){ # If the file is in the 'duration' format, this code will create 2 figs from those data
      
      # Format each file to be readable by loop 
      colnames(data) <- New_dur_colnames # Changes the column names to the vector of names defined above
      data$Start_date <-as.Date(data$Start_date, format = "%m/%d/%y") # Puts start date in date format
      data$Year <- format(data$Start_date, format = '%Y') # Creates year column for the start date
      data$Month <- month(data$Start_date, label = T, abbr = F) # Creates a month column for the start date
      
      # # These print statements will help me determine the ylims and legends for the figs
      # print(paste('Max draw down duration (days):', max(data$Duration), sep =' ')) 
      # # plot1
      # print(paste('Min draw down magnitude (%change ymin):', signif(min(data$Percent_Diff*100), digits = 4), sep =' '))
      # # plot2
      # print(paste('Min draw down rate (rate ymin):', signif(min(data$Rate_of_Change), digits = 4), sep =' '))

      # Uses a nested if/else statement to create a season column depending on the month of the start date
      data$Season <- ifelse(data$Month %in% Spring, "Spring",
                            ifelse(data$Month %in% Summer, "Summer",
                                   ifelse(data$Month %in% Fall, "Fall","Winter")))
      # R automatically orders factors alphabetically - but we want these seasons in true annual order
      # The order only really matters for the figure legend and colors
      data$Season <- factor(data$Season, levels = c('Spring','Summer','Fall','Winter'))
      
      # Plots percent difference (magnitude of draw down) vs date (year) 
      # with color based on season of start date and size based on duration of draw down
      
      
      plot1 <- ggplot(data) + aes(ymax = 0) + # Tells ggplot to use 'data' to create graph 
        geom_point(aes(x = Start_date, y = Percent_Diff*100, size = Duration, col = Season)) + # Creates points (Note: Percent_Diff is * 100 to covert to %)
        geom_hline(yintercept = 0, linetype = 2) + # Adds horizontal reference line at y = 0
        scale_size_continuous(limits = c(1,365), breaks = seq(0,200,50)) + # Makes sure the legend have a size reference for every 50 days of duration
        #scale_color_manual(values = c('pink', 'green', 'orange', 'blue')) + # uncomment to can change the colors of the points - the automatic colors are fine for now 
        labs(x = "Year", y = "% Change in Elevation", size = "Duration (days)", col = "Season") + # Adds axis and legend labels
        theme_classic() + # An uncluttered theme for the plot
        theme(legend.position = 'none') + # removes legend
        ggtitle(paste(unlist(strsplit(fileTrip, "(?i:_Elevation_)",perl=T))[1], ":\nmagnitude (%) of change", sep = " "))
      
      # Set the yaxis limits depending on the file names and the min y of the lake
      if(signif(min(data$Percent_Diff*100) < 0) & signif(min(data$Percent_Diff*100) > -1)){ 
        plot1 <- plot1 + aes(ymin = -1)
      }
      if(signif(min(data$Percent_Diff*100) < -1) & signif(min(data$Percent_Diff*100) > -5)){ 
        plot1 <- plot1 + aes(ymin = -3)
      }
      if(signif(min(data$Percent_Diff*100) < -3) & signif(min(data$Percent_Diff*100) > -5)){ 
        plot1 <- plot1 + aes(ymin = -5)
      }
      if(signif(min(data$Percent_Diff*100) < -18)){ 
        plot1 <- plot1 + aes(ymin = -20)
      }
      
      
      # Plots rate of change (rate of draw down) vs date (year) 
      # with color based on season of start date and size based on duration of draw down
      plot2 <- ggplot(data) + aes(ymax = 0) + # Tells ggplot to use 'data' to create graph 
        geom_point(aes(x = Start_date, y = Rate_of_Change, size = Duration, col = Season)) + # Creates points 
        geom_hline(yintercept = 0, linetype = 2) + # Adds horizontal reference line at y = 0
        scale_size_continuous(limits = c(1,365), breaks = seq(0,200,50)) + # Makes sure the legend have a size reference for every 50 days of duration
        #scale_color_manual(values = c('pink', 'green', 'orange', 'blue')) + # uncomment to can change the colors of the points - the automatic colors are fine for now 
        labs(x = "Year", y = "Rate of Change in Elevation (ft/day)", size = "Duration (days)", col = "Season") + # Adds axis and legend labels
        theme_classic() + # An uncluttered theme for the plot
        theme(legend.position = 'right') + # Puts the legend on the right
        ggtitle(paste(unlist(strsplit(fileTrip, "(?i:_Elevation_)",perl=T))[1], ":\nrate of change", sep = " ")) # Adds a plot title based on the csv file name
      
      # Set the yaxis limits depending on the file names and the min y of the lake
      if(signif(min(data$Rate_of_Change) > -1)){ 
        plot2 <- plot2 + aes(ymin = -1)
      }
      if(signif(min(data$Rate_of_Change) < -1) & signif(min(data$Rate) > -4)){ 
        plot2 <- plot2 + aes(ymin = -4)
      }
      if(signif(min(data$Rate_of_Change) < -4) & signif(min(data$Rate) > -8)){ 
        plot2 <- plot2 + aes(ymin = -8)
      }
      if(signif(min(data$Rate_of_Change) > -8) & signif(min(data$Rate) < -18)){ 
        plot2 <- plot2 + aes(ymin = -20)
      }
      
      # ON SECOND THOUGHT, NOT SURE IF THIS FIG (plot3) IS USEFUL AT ALL CONSIDERING DIFFERENCE IN UNITS
      
      # Plots rate of change vs % change with reference y=x line
      # plot3 <- ggplot(data) + # Tells ggplot to use 'data' to create graph 
      #   geom_point(aes(x = as.numeric(Percent_Diff*100), y = Rate_of_Change, size = Duration, col = Season)) + # Creates points (Note: Percent_Diff is * 100 to covert to %)
      #   geom_abline(intercept = 0, slope = 1, linetype = 2) + # Adds  reference line at y = x
      #   scale_size_continuous(limits = c(1,365), breaks = seq(0,350,50)) + # Makes sure the legend have a size reference for every 50 days of duration
      #   #scale_color_manual(values = c('pink', 'green', 'orange', 'blue')) + # uncomment to can change the colors of the points - the automatic colors are fine for now 
      #   labs(x = "% Change in elevation", y = "Rate of Change in Elevation (ft/day)", size = "Duration (days)", col = "Season") + # Adds axis and legend labels
      #   theme_classic() + # An uncluttered theme for the plot
      #   theme(legend.position = 'right') + # Puts the legend on the right
      #   ggtitle(paste(unlist(strsplit(fileTrip, "(?i:_Elevation_)",perl=T))[1], ":\nmagnitude vs rate of change", sep = " ")) # Adds a plot title based on the csv file name
      # 
    } # End of plotting code for duration csvs 
    
    
    if(grepl('Metrics', fileTrip)){ # If the file is in the 'metrics' format, this code will create 4 figs from those data
      
      # Format each file to be readable by loop 
      colnames(data) <- New_met_colnames # Changes the column names to the vector of names defined above 
      data$Year <- as.numeric(data$Year) # Creates year column for the start date
      
      # # print statements will help me determine the ylims and legends for the figs
      # #plot1
      # print(paste('Max draw down magnitude (%change ymax):', signif(max(data$Mean_percent_diff*100 + data$SD_percent_diff*100), digits = 4), sep =' '))
      # print(paste('Min draw down magnitude (%change ymin):', signif(min(data$Mean_percent_diff*100 - data$SD_percent_diff*100), digits = 4), sep =' '))
      # #plot2
      # print(paste('Max draw down rate (rate ymax):', signif(max(data$Mean_rate + data$SD_rate), digits = 4), sep =' '))
      # print(paste('Min draw down rate (rate ymin):', signif(min(data$Mean_rate - data$SD_rate), digits = 4), sep =' '))
      # #plot3
      # print(paste('Max days per draw down (days ymax):', signif(max(data$Mean_days_drawdown + data$SD_days_drawdown), digits = 2), sep =' '))
      # print(paste('Min days per draw down (days ymin):', signif(min(data$Mean_days_drawdown - data$SD_days_drawdown), digits = 2), sep =' '))
      # #plot3
      # print(paste('Max draw downs per yr (events ymax):', signif(max(data$Number_drawdowns), digits = 2), sep =' '))

      
      # Plots mean +/- SD percent difference (mean magnitude of draw down) vs year
      # with color based on % of year in draw down   
      plot1 <- ggplot(data) + # Tells ggplot to use 'data' to create graph 
        geom_errorbar(aes(x = Year, ymin = Mean_percent_diff*100 - SD_percent_diff*100, ymax = Mean_percent_diff*100 + SD_percent_diff*100), 
                      size = 1, width = 0.1) +
        geom_point(aes(x = Year, y = Mean_percent_diff*100, color = Percent_yr_drawdown*100), size = 5) + # Creates points (Note: Percent_Diff is * 100 to covert to %)
        geom_hline(yintercept = 0, linetype = 2) + # Adds horizontal reference line at y = 0
        scale_color_gradientn(colors = rainbow(4), limits = c(0,100), breaks = seq(0,100,25)) + # Makes sure the legend have a size reference for every 10% of year in draw down
        labs(x = "Year", y = " Mean +/- SD % Change in Elevation", color = "% Year in\ndraw down") + # Adds axis and legend labels
        theme_classic() + # An uncluttered theme for the plot
        theme(legend.position = 'none') + #  removes legend
        ggtitle(paste(unlist(strsplit(fileTrip, "(?i:_Elevation_)",perl=T))[1], ":\nMean magnitude (%) of draw down", sep = " "))

      
      # Set the yaxis limits depending on the file names and the min y of the lake
      # set ymax 
      if(signif(max(data$Mean_percent_diff*100 + data$SD_percent_diff*100) > 0) & signif(max(data$Mean_percent_diff*100 + data$SD_percent_diff*100) < 0.25)){
        plot1 <- plot1 + aes(ymax=0.25)
      }
      if(signif(max(data$Mean_percent_diff*100 + data$SD_percent_diff*100) > 0.25) & signif(max(data$Mean_percent_diff*100 + data$SD_percent_diff*100) < 0.75)){
        plot1 <- plot1 + aes(ymax=0.75)
      }
      if(signif(max(data$Mean_percent_diff*100 + data$SD_percent_diff*100) > 0.75)){
        plot1 <- plot1 + aes(ymax=3.5)
      }
      if(grepl('1FT', fileTrip) & signif(max(data$Mean_percent_diff*100 + data$SD_percent_diff*100) <= 0)){
        plot1 <- plot1 + aes(ymax=0)
      }
      
      # set ymin
      if(signif(min(data$Mean_percent_diff*100 - data$SD_percent_diff*100) < 0) & signif(min(data$Mean_percent_diff*100 - data$SD_percent_diff*100) > -1)){ 
        plot1 <- plot1 + aes(ymin = -1)
      }
      if(signif(min(data$Mean_percent_diff*100 - data$SD_percent_diff*100) < -1) & signif(min(data$Mean_percent_diff*100 - data$SD_percent_diff*100) > -3)){ 
        plot1 <- plot1 + aes(ymin = -3)
      }
      if(signif(min(data$Mean_percent_diff*100 - data$SD_percent_diff*100) < -3) & signif(min(data$Mean_percent_diff*100 - data$SD_percent_diff*100) > -5)){ 
        plot1 <- plot1 + aes(ymin = -5)
      }
      if(signif(min(data$Mean_percent_diff*100 - data$SD_percent_diff*100) < -12)){ 
        plot1 <- plot1 + aes(ymin = -16)
      }
      
      
      # Plots mean +/- SD rate of change (mean rate of draw down) vs year
      # with color based on % of year in draw down
      plot2 <- ggplot(data) + # Tells ggplot to use 'data' to create graph 
        geom_errorbar(aes(x = Year, ymin = Mean_rate - SD_rate, ymax = Mean_rate + SD_rate), 
                      size = 1, width = 0.1) +
        geom_point(aes(x = Year, y = Mean_rate, color = Percent_yr_drawdown*100), size = 5) + # Creates points 
        geom_hline(yintercept = 0, linetype = 2) + # Adds horizontal reference line at y = 0
        scale_color_gradientn(colors = rainbow(4), limits = c(0,100), breaks = seq(0,100,25)) + # Makes sure the legend have a size reference for every 10% of year in draw down
        labs(x = "Year", y = " Mean +/- SD rate (ft/day) of draw down", size = "% Year in\ndraw down") + # Adds axis and legend labels
        theme_classic() + # An uncluttered theme for the plot
        theme(legend.position = 'none') + #  removes legend
        ggtitle(paste(unlist(strsplit(fileTrip, "(?i:_Elevation_)",perl=T))[1], ":\nMean rate of draw down", sep = " ")) # Adds a plot title based on the csv file name
  
      # Set the yaxis limits depending on the file names and the min y of the lake
      # set ymax
      if(signif(max(data$Mean_rate + data$SD_rate) > 0.4)){ 
        plot2 <- plot2 + aes(ymax = 4)
      }
      if(signif(max(data$Mean_rate + data$SD_rate) > 0.1) & signif(max(data$Mean_rate + data$SD_rate) < 0.4)){ 
        plot2 <- plot2 + aes(ymax = 0.4)
      }
      if(signif(max(data$Mean_rate + data$SD_rate) > 0) & signif(max(data$Mean_rate + data$SD_rate) < 0.1)){ 
        plot2 <- plot2 + aes(ymax = 0.1)
      }
      if(signif(max(data$Mean_rate + data$SD_rate) > 0.1) & signif(max(data$Mean_rate + data$SD_rate) < 0.4)){ 
        plot2 <- plot2 + aes(ymax = 0.4)
      }
      if(signif(max(data$Mean_rate + data$SD_rate) < 0)){ 
        plot2 <- plot2 + aes(ymax = 0)
      }
      
      # set ymin
      if(signif(min(data$Mean_rate - data$SD_rate) < 0) & signif(min(data$Mean_rate - data$SD_rate) > -1)){ 
        plot2 <- plot2 + aes(ymin = -1)
      }
      if(signif(min(data$Mean_rate - data$SD_rate) < -1) & signif(min(data$Mean_rate - data$SD_rate) > -3.5)){ 
        plot2 <- plot2 + aes(ymin = -3.5)
      }
      if(signif(min(data$Mean_rate - data$SD_rate) < -3.5) & signif(min(data$Mean_rate - data$SD_rate) > -5)){ 
        plot2 <- plot2 + aes(ymin = -5)
      }
      if(signif(min(data$Mean_rate - data$SD_rate) < -5)){ 
        plot2 <- plot2 + aes(ymin = -9)
      }
      
      # Plots mean +/- SD days per draw down (mean duration of draw down) vs year
      # with color based on % of year in draw down
      plot3 <- ggplot(data) + # Tells ggplot to use 'data' to create graph 
        geom_errorbar(aes(x = Year, ymin = Mean_days_drawdown - SD_days_drawdown, ymax = Mean_days_drawdown + SD_days_drawdown), 
                      size = 1, width = 0.1) +
        geom_point(aes(x = Year, y = Mean_days_drawdown, color = Percent_yr_drawdown*100), size = 5) + # Creates points 
        # geom_hline(yintercept = 0, linetype = 2) + # Adds horizontal reference line at y = 0
        scale_color_gradientn(colors = rainbow(4), limits = c(0,100), breaks = seq(0,100,25)) + # Makes sure the legend have a size reference for every 10% of year in draw down
        labs(x = "Year", y = " Mean +/- SD No. days per draw down", size = "% Year in\ndraw down") + # Adds axis and legend labels
        theme_classic() + # An uncluttered theme for the plot
        theme(legend.position = 'none') + # removes legend
        ggtitle(paste(unlist(strsplit(fileTrip, "(?i:_Elevation_)",perl=T))[1], ":\nMean duration of draw down", sep = " ")) # Adds a plot title based on the csv file name
      
      # Set the yaxis limits depending on the file names and the min y of the lake
      # set ymax
      if(grepl('1FT', fileTrip)){ 
        plot3 <- plot3 + aes(ymax = 161)
      }
      if(grepl('0.2FT', fileTrip)){ 
        plot3 <- plot3 + aes(ymax = 250)
      }
      
      # set ymin
      if(signif(min(data$Mean_days_drawdown - data$SD_days_drawdown) > 0)){ 
        plot3 <- plot3 + aes(ymin = 0)
      }
      if(signif(min(data$Mean_days_drawdown - data$SD_days_drawdown) < 0) & signif(min(data$Mean_days_drawdown - data$SD_days_drawdown) > -10)){ 
        plot3 <- plot3 + aes(ymin = -10)
      }
      if(signif(min(data$Mean_days_drawdown - data$SD_days_drawdown) < -10) & signif(min(data$Mean_days_drawdown - data$SD_days_drawdown) > -20)){ 
        plot3 <- plot3 + aes(ymin = -20)
      }
      if(signif(min(data$Mean_days_drawdown - data$SD_days_drawdown) < -20) & signif(min(data$Mean_days_drawdown - data$SD_days_drawdown) > -30)){ 
        plot3 <- plot3 + aes(ymin = -30)
      }
      # Plots total number of draw down (freq of draw down) vs year
      # with color based on % of year in draw down
      plot4 <- ggplot(data) + aes(ymin = 0, ymax = 40) + # Tells ggplot to use 'data' to create graph 
        geom_point(aes(x = Year, y = Number_drawdowns, color = Percent_yr_drawdown*100), size = 5) + # Creates points 
        # geom_hline(yintercept = 0, linetype = 2) + # Adds horizontal reference line at y = 0
        scale_color_gradientn(colors = rainbow(4), limits = c(0,100), breaks = seq(0,100,25)) + # Makes sure the legend have a size reference for every 10% of year in draw down
        labs(x = "Year", y = " No. draw down events per year", col = "% Year in\ndraw down") + # Adds axis and legend labels
        theme_classic() + # An uncluttered theme for the plot
        theme(legend.position = 'right') + # Puts the legend on the right
        ggtitle(paste(unlist(strsplit(fileTrip, "(?i:_Elevation_)",perl=T))[1], ": \nFrequency of draw downs", sep = " ")) # Adds a plot title based on the csv file name

    } # End of plotting code for metrics csvs
    
  } # End of J loop
  
  # Back to I loop to add new plot pdf file to the folder
  if(grepl(paste(est, collapse = '|'), fileTrip)){ 
    status <- "Established"
  }
  if(grepl(paste(sus, collapse = '|'), fileTrip)){
    status <- "Suspect"
  }
  if(grepl(paste(neg, collapse = '|'), fileTrip)){
    status <- "Negative"
  }
  
  filename <- paste(status,'_', str_split_fixed(fileTrip,".csv", n = 2)[1], '_plots.pdf', sep = '') # New pdf file name
  
  # Creates duration fig layout
  if(grepl('Duration', fileTrip)){
    pdf(filename, width = 11, height = 4) # Creates the pdf by the file named above
    print(grid.arrange(plot1, plot2, nrow = 1, widths = c(1,1.2))) # Prints 3 plots to pdf
  }
  
  # Creates metric fig layout
  if(grepl('Metrics', fileTrip)){
    pdf(filename, width = 8, height = 8) # Creates the pdf by the file named above
    print(grid.arrange(plot1, plot2, plot3, plot4, ncol = 2, nrow = 2)) # Prints 4 plots to pdf
  }
  
  dev.off() #Honestly not sure what this line means, but it's needed...maybe it closes the file? *shrug*
  print('') #creates space between prints in console
  print('')
  print('')
  
} # End of I loop

# You should now have a figure PDF for each CSV file in the folder you set in the beginning of the I loop 


