# -*- coding: utf-8 -*-
"""ProjectNewsAnalysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RkbwZhMu8l7Wc6zJrJslP59VAykrzzgw
"""

# !pip install investpy
#!pip install python-dateutil

import pandas as pd
import investpy

invest = investpy.news.economic_calendar(time_zone="GMT +5:30",from_date="15/11/2022",to_date="20/11/2022")

#USD Events       ,  note --- dataframe.iloc[:,3] -> all row, particular column    and   dataframe.iloc[3,4] -> 4th row, 5th column
usdEvents = (invest[invest.iloc[:, 4] == "USD"]).reset_index()  # ---------- (01)    ,   this usdEvents is new dataframe, it is using usual indexs as 0,1,2,3,....

def removeLowImpacts():      # to remove events having "low" impact  ------------(02)
  df = pd.DataFrame()   # create new dataframe
  for x in range(0,len(usdEvents.index)):
    if(usdEvents.iloc[x].importance=="medium" or usdEvents.iloc[x].importance=="high"):   # usdEvents.iloc[x] means object & importance is like attribute
       df = df.append(usdEvents.iloc[x,:], ignore_index=True)
  
  return df 

def detectTrendSignal(dataframe):  #to detect trend signals   ----------------(03)(a)
  dataframe['signal'] = None
  for x in range(0,len(dataframe.index)):
    if(dataframe.iloc[x].forecast==None or dataframe.iloc[x].previous==None):
      dataframe.iloc[x,11] = None
    else:
      forecast = dataframe.iloc[x].forecast
      previous = dataframe.iloc[x].previous

      forecast = forecast.replace('M','')
      forecast = forecast.replace('%','')
      forecast = forecast.replace('K','')
      forecast = forecast.replace('B','')
      forecast = float(forecast)

      previous = previous.replace('M','')
      previous = previous.replace('%','')
      previous = previous.replace('K','')
      previous = previous.replace('B','')
      previous = float(previous)

      if(forecast<previous):
        dataframe.iloc[x,11] = "Buy"
      elif(previous<forecast):
        dataframe.iloc[x,11] = "Sell"
      else:
        dataframe.iloc[x,11] = "Neutral"  

  return dataframe

def separateGroups(dataframe):   # to separate groups  ---------------(03)(b)          
  y = 0
  groupList = [pd.DataFrame()]
  groupList[0] = groupList[0].append(dataframe.iloc[0,:], ignore_index=True)
  for x in range(1,len(dataframe.index)):
    if(dataframe.iloc[x,11]==dataframe.iloc[x-1,11]):
      groupList[y] = groupList[y].append(dataframe.iloc[x,:], ignore_index=True)   
    else:
      groupList.append(pd.DataFrame())
      y += 1
      groupList[y] = groupList[y].append(dataframe.iloc[x,:], ignore_index=True)
  return groupList     # return list contains dataframes

def findHighImpacts(list):    # check whether previous groups have at least one high impact event & separate those groups ----------------(04) & (05)
  groupList = []
  for i in list:
    for x in range(0,len(i.index)):
      if(i.iloc[x,6]=="high"):
        groupList.append(i)
        break
  return groupList    # return list contains dataframes  

def generateTimeIntervals(list):    # generate time/time interval of those groups made in previous step   ------------------------(06)
  df = pd.DataFrame(columns=['from_time','to_time','signal']) 
  for i in list:
    array =[]   # create new array as new row to "df" dataframe
    from_time = None
    to_time = None
    # dic_ =	{}   
    # dic_["signal"] = i.iloc[0,11]
    if(len(i.index)==1):
      from_time = i.iloc[0,2] +" "+ i.iloc[0,3]
    else:  
      from_time = i.iloc[0,2] +" "+ i.iloc[0,3]
      to_time = i.iloc[len(i.index)-1,2] +" "+ i.iloc[len(i.index)-1,3]

    array.append(from_time)
    array.append(to_time)
    array.append(i.iloc[0,11])
    df.loc[len(df.index)] = array  # add new row into "df" dataframe
    # df = df.append(dic_, ignore_index=True)    add new row into "df" dataframe
  
  return df    # return dataframe having time/time intervals and signal



dataframeList_last = pd.DataFrame()

if(len(usdEvents.index)!=0):
  dataframe_02 = removeLowImpacts()  # output of step 02
  if(len(dataframe_02.index)!=0):
    dataframe_03 = detectTrendSignal(dataframe_02)   # output of step 03-a
    if(len(dataframe_03.index)!=0):
      dataframeList_01 = separateGroups(dataframe_03)   # output of step 03-b  , It,s a list of dataframes
      if(len(dataframeList_01) != 0):
        dataframeList_02 = findHighImpacts(dataframeList_01)   # output of step 4 & 5,  it's a list of dataframes
        if(len(dataframeList_02) != 0):
          dataframeList_last = generateTimeIntervals(dataframeList_02)  # output of step 6, it,s dataframe having time/time intervals and signal
        else:
          print("Nothing,,, code execution is stopped.")  
      else:
        print("Nothing,,, code execution is stopped.")

    else:
      print("Nothing,,, code execution is stopped.")
  else:
    print("Nothing,,, code execution is stopped.")
  
else:
  print("Nothing,,, code execution is stopped.")


json = dataframeList_last.to_json()
print(dataframeList_last)



