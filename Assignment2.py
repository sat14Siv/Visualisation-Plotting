
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Miami Beach, Florida, United States**, and the stations the data comes from are shown on the map below.

# In[39]:

import matplotlib as mpl
import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
import numpy as np

def leaflet_plot_stations(binsize, hashid):
    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))
    station_locations_by_hash = df[df['hash'] == hashid]
    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()
    plt.figure(figsize=(8,8))
    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)
    return mplleaflet.display()
leaflet_plot_stations(400,'381398cf597bf0c79d1bf9352eb67e3fe22eeacf2f716a5504d524da') #HashID corresponds to Miami Beach,FL.


# In[40]:

data = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/381398cf597bf0c79d1bf9352eb67e3fe22eeacf2f716a5504d524da.csv')
data.drop('ID',axis=1,inplace =True)   #Dropping the column 'ID'
data = data[data['Date'] < '2015']     #Only retaining data till the end of 2014, as that is to be used for line plot.
data['Data_Value'] = data['Data_Value']/10 #Temperature data is given in tenths of degrees. So converting to actual values.

#Here, I have modified the dates such that the year is omitted. Eg:-'2011-09-12'->'09-12'. I have done this so that I can set
#the dates as the index and find out the max and min temps throughout all the years on that particular date.
ser =[]
for i in range(len(data)):
    ser.append(data.iloc[i]['Date'][5:])
data['Date'] = pd.Series(ser)    #Modified 'Date' column.
data.sort('Date',inplace = True)
dates = list(data['Date'].unique())
dates.remove('02-29')            #Removing 29th February.
dates = dates[:-1]
data.set_index(['Date','Element'],inplace = True)

maxi, mini = ([] for i in range(2))  #maxi and mini are 365 element lists containing the max and min temperatures on each date
                                     #over the years 2005-2014.
for item in dates:
        maxi.append(max(data.loc[item]['Data_Value']))
        mini.append(min(data.loc[item]['Data_Value']))


# In[41]:

#Now I will retain only the data corresponding to the year 2015.
data2 = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/381398cf597bf0c79d1bf9352eb67e3fe22eeacf2f716a5504d524da.csv')
data2.drop('ID',axis=1,inplace =True)
data2 = data2[data2['Date']>'2015']
data2['Data_Value'] = data2['Data_Value']/10
data2_max = data2[data2['Element']=='TMAX'] #Creating a data frame containing only TMAX values.
data2_min = data2[data2['Element']=='TMIN'] #Creating a data frame containing only TMIN values.
data2_max.sort('Date',inplace = True)
data2_min.sort('Date',inplace = True)

#Here I am attempting to find out the dates(in the form of index,which gives the day of the year) on which the 2015 data 
#breaks the record data till 2014.
mini2, maxi2, index_min, index_max = ([] for i in range(4))
for i in range(365):
    if data2_min.iloc[i]['Data_Value'] < mini[i]:
        mini2.append(data2_min.iloc[i]['Data_Value'])
        index_min.append(i+1)       #(i+1) since i runs from 0-364 and days are from 1-365.
    if data2_max.iloc[i]['Data_Value'] > maxi[i]:
        maxi2.append(data2_max.iloc[i]['Data_Value'])
        index_max.append(i+1)


# In[44]:

days = list(np.arange(1,366))
mpl.rcParams['figure.figsize'] = (15, 8)
plt.title('Highest and Lowest Temperatures Recorded in Miami on each day of the year in the period 2005-2014 ($^\circ$C)')
plt.plot(days,mini,'-',days,maxi,'-',linewidth =0.8)                       #Line Plot
plt.scatter(index_max,maxi2,c='b',s=10, label = 'Record highs set in 2015')#Scatter plot of 2015 record high temperatures.
plt.scatter(index_min,mini2,c='red',s=10, label = 'Record lows set in 2015')#Scatter plot of 2015 record low temperatures.
plt.gca().fill_between(range(1,len(maxi)+1),mini,maxi,facecolor='grey',alpha=0.15)
month_beg = [1,29,60,90,121,151,182,213,243,274,304,335]    #The starting days of each month.
months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
plt.subplot().set_xticks(month_beg)
plt.subplot().set_xticklabels(months)  #Setting the starting day of each month to the month name on the x-axis.
plt.legend(['Minimum Temperatures till 2014','Maximum Temperatures till 2014','Record highs which were set in 2015','Record lows which were set in 2015'],loc=1,frameon = False)
plt.ylim((0,45))   #Increasing the temperature limit to 45 C.


# In[45]:

plt.show()

