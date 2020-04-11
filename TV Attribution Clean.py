# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 15:52:56 2019

@author: michael.gutierrez
"""

import pandas as pd
import datetime

##load in datasets
 
spotdf = pd.read_csv('')

#Break out AZ/FL spots

AZspots1 = spotdf.loc[spotdf["State"] == 'AZ'].reset_index(drop = True)

FLspots1 = spotdf.loc[spotdf["State"] == 'FL'].reset_index(drop = True)

#subset mobile and desktop

dfAZmob = pd.read_csv('')
dfAZdesk = pd.read_csv('')

dfFLmob = pd.read_csv('')
dfFLdesk = pd.read_csv('')


##dcmdf['date'] = str(dcmdf['date'])
##dcmdf.info()

#Create datetimes for spotdf
AZspots1['datetime'] = pd.to_datetime(AZspots1['DT Eastern'])
AZspots1['datetime'] = AZspots1['datetime'].values.astype('<M8[m]')

FLspots1['datetime'] = pd.to_datetime(FLspots1['DT Eastern'])
FLspots1['datetime'] = FLspots1['datetime'].values.astype('<M8[m]')

#Convert spot df times from eastern to pacific
AZspots1['datetime'] = AZspots1['datetime'].dt.tz_localize('US/Eastern',ambiguous = True).dt.tz_convert('America/Los_Angeles')
FLspots1['datetime'] = FLspots1['datetime'].dt.tz_localize('US/Eastern',ambiguous = True).dt.tz_convert('America/Los_Angeles')

#Duplicate spots datasets for later use 
AZspots2 = AZspots1.copy(deep =True)
AZspots3 = AZspots1.copy(deep =True)

FLspots2 = FLspots1.copy(deep =True)
FLspots3 = FLspots1.copy(deep =True)



##Find ad times that overalp +-1 to 10 min with other ad times for each state

#AZ overlap
df_o1 = pd.DataFrame()

for i in range(-10,11):
    df_o1[i] = AZspots1['datetime'] + datetime.timedelta(minutes = i )

x = pd.DataFrame(df_o1.values.flatten().transpose())
x.columns = ['datetime']
##x.drop_duplicates(subset = ['datetime'], keep = False,inplace =True)

##remove all rows for overalpping times
x['freq'] = x.groupby('datetime')['datetime'].transform('count')

dts_to_keep = x.loc[x['freq'] == 1].reset_index(drop = True)

dts_to_keep['dt'] = dts_to_keep['datetime']

for i in range(-10,11):
    AZspots1[i] = AZspots1['datetime'] + datetime.timedelta(minutes = i) 
    AZspots1[i] = pd.merge(AZspots1,dts_to_keep[['datetime','dt']], how = 'left', left_on= i, right_on ='datetime')['dt']
    
##New dataset
spots_cleanAZ = AZspots1
   
spots_cleanAZ = spots_cleanAZ.dropna().reset_index(drop =True)    

spots_clean_dtsAZ = pd.DataFrame(spots_cleanAZ['datetime'])


#FL Overlap
df_o2 = pd.DataFrame()

for i in range(-10,11):
    df_o2[i] = FLspots1['datetime'] + datetime.timedelta(minutes = i )

x2 = pd.DataFrame(df_o2.values.flatten().transpose())
x2.columns = ['datetime']
##x.drop_duplicates(subset = ['datetime'], keep = False,inplace =True)

##remove all rows for overalpping times
x2['freq'] = x2.groupby('datetime')['datetime'].transform('count')

dts_to_keep2 = x2.loc[x2['freq'] == 1].reset_index(drop = True)

dts_to_keep2['dt'] = dts_to_keep2['datetime']

for i in range(-10,11):
    FLspots1[i] = FLspots1['datetime'] + datetime.timedelta(minutes = i) 
    FLspots1[i] = pd.merge(FLspots1,dts_to_keep2[['datetime','dt']], how = 'left', left_on= i, right_on ='datetime')['dt']
    
##New dataset
spots_cleanFL = FLspots1
   
spots_cleanFL = spots_cleanFL.dropna().reset_index(drop =True)    

spots_clean_dtsFL = pd.DataFrame(spots_cleanFL['datetime'])


#Convert Mob/desk dfs to dt

#AZ
dfAZmob['datetime'] = pd.to_datetime(dfAZmob['date_time'].apply(str))
dfAZmob['datetime'] = dfAZmob['datetime'].values.astype('<M8[m]')
dfAZmob['datetime'] = dfAZmob['datetime'].dt.tz_localize('America/Los_Angeles',ambiguous = True)

dfAZdesk['datetime'] = pd.to_datetime(dfAZdesk['date_time'].apply(str))
dfAZdesk['datetime'] = dfAZdesk['datetime'].values.astype('<M8[m]')
dfAZdesk['datetime'] = dfAZdesk['datetime'].dt.tz_localize('America/Los_Angeles',ambiguous = True)

#FL
dfFLmob['datetime'] = pd.to_datetime(dfFLmob['date_time'].apply(str))
dfFLmob['datetime'] = dfFLmob['datetime'].values.astype('<M8[m]')
dfFLmob['datetime'] = dfFLmob['datetime'].dt.tz_localize('America/Los_Angeles',ambiguous = True)

dfFLdesk['datetime'] = pd.to_datetime(dfFLdesk['date_time'].apply(str))
dfFLdesk['datetime'] = dfFLdesk['datetime'].values.astype('<M8[m]')
dfFLdesk['datetime'] = dfFLdesk['datetime'].dt.tz_localize('America/Los_Angeles',ambiguous = True)


## for i in 1 to 15
## counter = []
## if time  = spot time + i
## sum =  counter + coount   

##counter = pd.DataFrame()
##counts = dcmdf
#count conversion by datetime
##counts = dcmdf.groupby(["datetime"]).size().reset_index(name = "Count")

#count distinct conversions by datetime
##dcounts = dcmdf.groupby("datetime").agg({"user_id":'nunique'}).reset_index()

#count conversion by datetime
##counts = dcmdf2.groupby(["datetime"]).size().reset_index(name = "Count")

#count distinct conversions by datetime
#dcounts = dcmdf2.groupby("datetime").agg({"user_id":'nunique'}).reset_index()

#account for overlap between spots
#if count([i])

##spotdf[time_diff] = 
 #if datetime = datetime +- 15min :
     #del datetime
#only use first user id for each day
#t.first <- species[match(unique(species$Taxa), species$Taxa),]

#for loop for getting counts of conversions by minutes out for each ad from counts df 
     
#Desktop 
#AZ     
for i in range(-10,11):
    AZspots2[i] = AZspots2['datetime'] + datetime.timedelta(minutes = i) 
    AZspots2[i] = pd.merge(AZspots2,dfAZdesk[['datetime','activity_count']], how = 'left', left_on= i, right_on ='datetime')['activity_count']
    df_new = AZspots2
    
#FL
for i in range(-10,11):
    FLspots2[i] = FLspots2['datetime'] + datetime.timedelta(minutes = i) 
    FLspots2[i] = pd.merge(FLspots2,dfFLdesk[['datetime','activity_count']], how = 'left', left_on= i, right_on ='datetime')['activity_count']
    df_new3 = FLspots2
    
#Mobile 
#AZ    
for i in range(-10,11):
    AZspots3[i] = AZspots3['datetime'] + datetime.timedelta(minutes = i) 
    AZspots3[i] = pd.merge(AZspots3,dfAZmob[['datetime','activity_count']], how = 'left', left_on= i, right_on ='datetime')['activity_count']
    df_new5 = AZspots3

#FL    
for i in range(-10,11):
    FLspots3[i] = FLspots3['datetime'] + datetime.timedelta(minutes = i) 
    FLspots3[i] = pd.merge(FLspots3,dfFLmob[['datetime','activity_count']], how = 'left', left_on= i, right_on ='datetime')['activity_count']
    df_new7 = FLspots3    
   
    
#remove overlapping dates

#Desktop
#AZ    
df_new2 = pd.merge(spots_cleanAZ[['datetime']],df_new, how='left',on = 'datetime')

df_new2 = df_new2[pd.notnull(df_new2['DT Eastern'])]

#FL
df_new4 = pd.merge(spots_cleanFL[['datetime']],df_new3, how='left',on = 'datetime')

df_new4 = df_new4[pd.notnull(df_new4['DT Eastern'])]

#Desktop Full
df_new2_vals = df_new2.drop(df_new2.columns[[0,1,2,3,4,5,6]],axis =1) 
df_new4_vals = df_new4.drop(df_new4.columns[[0,1,2,3,4,5,6]],axis =1) 
df_desk_full = df_new2_vals.add(df_new4_vals,fill_value=0)

#Mobile
#AZ    
df_new6 = pd.merge(spots_cleanAZ[['datetime']],df_new5, how='left',on = 'datetime')

df_new6 = df_new6[pd.notnull(df_new6['DT Eastern'])]

#FL
df_new8 = pd.merge(spots_cleanFL[['datetime']],df_new7, how='left',on = 'datetime')

df_new8 = df_new8[pd.notnull(df_new4['DT Eastern'])]

#Mobile full
df_new6_vals = df_new6.drop(df_new6.columns[[0,1,2,3,4,5,6]],axis =1) 
df_new8_vals = df_new8.drop(df_new8.columns[[0,1,2,3,4,5,6]],axis =1) 
df_mob_full = df_new6_vals.add(df_new8_vals,fill_value=0)

# heck head/tail of new df
head_new = df_new.head()
tail_new = df_new.tail()    
#write to csv
df_new2.to_csv("dAZ.csv",index=False)

df_new4.to_csv("dFL.csv",index = False)

df_new6.to_csv("mAZ.csv",index=False)

df_new8.to_csv("mFL.csv",index=False)

df_mob_full.to_csv("m.csv",index=False)
df_desk_full.to_csv("d.csv",index=False)

spots_clean.to_csv("clean.csv",index = False)
##test_df = pd.merge(df_new,counts,how='left', left_on = 13, right_on = 'datetime')
##df_test = pd.merge()

##for column in df_new.iteritems():
    ##df_new2 = pd.DataFrame.join(df_new,counts['Count'],how='left', left_on = column, right_on = 'datetime')
    
    #spotdf[i] = counts.loc[counts['datetime'].reset_index(drop=True) == spotdf[i].reset_index(drop =True), 'counts']
    #spotdf[i] = np.where(counts["datetime"] = spotdf[i])             
    ##df_new

##for i in range(16):
        ##spotdf[i] = counts.loc[counts["date"].reset_index(drop=True) == spotdf["bvs_date"].reset_index(drop=True)].sum(axis=1)
        ##df_new = spotdf
        


