# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 16:10:51 2018

@author: Sateesh
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
import numpy as np
#%%

#Read Data.
hinduStateData = pd.read_excel('C:\\Users\Sateesh\Documents\Python\Data Science Michigan\Visualization,Plotting\\U.S. Religion Census Religious Congregations and Membership Study, 2010 (State File).XLSX', usecols = [301,302,303,304,305,306,307,308,309,310,311,312,312,555,562,563,564])

stateGDP = pd.read_excel('C:\\Users\Sateesh\Documents\Python\Data Science Michigan\Visualization,Plotting\GDP_Data.xlsx',skiprows=[22,53],usecols=[0,1])

#%%
#Identifying the columns which contain data about Hindu adherents so that we can find out the total number of Hindus in a particular state.
totalHindus = []
for column in list(hinduStateData):
    if column[-3:] == 'ADH':
        totalHindus.append(column)

hinduStateData['Total_Hindus'] = hinduStateData[totalHindus].sum(axis=1)
sortedPop = hinduStateData.sort_values('Total_Hindus',ascending = False)
hinduStates = sortedPop['STNAME'][:10]  #Top 10 states with highest Hindu Population.

#Will retain only the data of the 10 most Hindu Populous states.
droprows = []
for index,state in list(enumerate(stateGDP['State'])):
    if not(state in list(hinduStates)):
        droprows.append(index)
req_states = stateGDP.drop(stateGDP.index[droprows])
        
req_states.set_index('State',inplace=True)
req_states = req_states.reindex(hinduStates)

#%%
fig, ax = plt.subplots()

plt.title('The Per capita income of the states in which most Hindus reside($)')

nationalGDP = 28889 

ax.bar(np.arange(1,11),list(req_states['Per capita income']))
ax.set_xticks([1,2,3,4,5,6,7,8,9,10])
ax.set_xticklabels(list(hinduStates))
ax.axhline(y=nationalGDP,color = 'black')  
plt.ylim((0,max(stateGDP['Per capita income']+10000)))
ax.axhline(y=max(stateGDP['Per capita income']),color='green')
ax.axhline(y=min(stateGDP['Per capita income']),color='red')

black_data = mpatch.Patch(color = 'black',label = 'National Average=${}'.format(nationalGDP))
green_data = mpatch.Patch(color = 'green',label = 'National High=${}'.format(max(stateGDP['Per capita income'])))
red_data = mpatch.Patch(color = 'red',label = 'National Low=${}'.format(min(stateGDP['Per capita income'])))

ax.legend(handles = [black_data,green_data,red_data],frameon = False)
