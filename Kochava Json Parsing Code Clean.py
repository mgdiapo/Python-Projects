# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 12:52:38 2019

@author: michael.gutierrez
"""

import pandas as pd
import json
import numpy as np

#load in data, rename file path to data
df_full = pd.read_csv("")

test = df_full.head()

#split unatttributed from rest of dataset
df_unatt = df_full[df_full.network_name == "-UNATTRIBUTED-"]

#Remove clicks/unattributeed observations
df_full = df_full[df_full.clicks == 0]
df_full = df_full[df_full.network_name != "-UNATTRIBUTED-"]
#Subset data into each channel

#Apple
df_apple = df_full[df_full.network_name == "Apple Search Ads"].reset_index(drop = True)
#Google
df_google = df_full[df_full.network_name == "Google Adwords"].reset_index(drop = True)
#Facebook
df_fb = df_full[df_full.network_name == "Facebook"].reset_index(drop = True)
#IG
df_ig = df_full[df_full.network_name == "Instagram"].reset_index(drop = True)
#Email
df_email = df_full[df_full.network_name == "SmartLinks"].reset_index(drop = True)

#Unpack JSON/rejoin function
def unpack_col(df,col):
    #unpack JSON
    mdf = df[col].apply(json.loads)
    mdf = pd.DataFrame(mdf.tolist())
    #join unpacked json with original data
    df_new = pd.concat([df,mdf], axis = 1)
    return (df_new)

#Unpack matched objects
adf = unpack_col(df_apple,'match_object')
gdf = unpack_col(df_google,'match_object')
gdf2 = unpack_col(gdf,'site_id')
fbdf = unpack_col(df_fb,'match_object')
igdf = unpack_col(df_ig,'match_object')
emaildf = unpack_col(df_email,'match_object')

test2 = igdf.head()

#Keep relevant columns, columns correspond to ids 

#apple
adf_final = adf.iloc[ :,np.r_[0:8,31]]
#goolge
gdf_final = gdf2.iloc[ :,np.r_[0:8,24,58]] #rename network fields in app pull to match google_property names in installs YouTube Video = youtube, 
#FB
fbdf_final =fbdf.iloc[ :,np.r_[0:8,18]]
#IG
igdf_final =igdf.iloc[ :,np.r_[0:8,18]]
#FB+IG
fbigdf_final = fbdf_final.append(igdf_final)


#Pivot final dfs
#apple
adf_pivot = adf_final.pivot_table( values = ['installs_original','activations','ecommerce_purchases'],index = ['network_name','date_utc','iad-campaign-id'],aggfunc = np.sum)
adf_pivot = adf_pivot.reset_index()
adf_pivot.to_csv("adf.csv")

#google
gdf_pivot = gdf_final.pivot_table( values = ['installs_original','activations','ecommerce_purchases'],index = ['network_name','date_utc','google_property','campaignid'],aggfunc = np.sum)
gdf_pivot = gdf_pivot.reset_index()
#write to csv
gdf_pivot.to_csv("gdf.csv")

#fb
fbigdf_pivot = fbigdf_final.pivot_table( values = ['installs_original','activations','ecommerce_purchases'],index = ['network_name','date_utc','campaign_group_id'],aggfunc = np.sum)
fbigdf_pivot = fbigdf_pivot.reset_index()
#make network names lowecase in order to make joining easier
fbigdf_pivot['network_name'] = fbigdf_pivot['network_name'].str.lower()
#write to csv
fbigdf_pivot.to_csv("fbigdf.csv")
#Be sure to open csv an dsave campaign_group_id as number to make joining easier 

#Email
email_final = emaildf.iloc[ :,np.r_[0:8]]
email_pivot = email_final.pivot_table( values = ['installs_original','activations','ecommerce_purchases'],index = ['app_name','network_name','date_utc'],aggfunc = np.sum)
email_pivot = email_pivot.reset_index()

#Unattributed
unatt_final = df_unatt.iloc[:,np.r_[0:8]]
unatt_pivot = unatt_final.pivot_table( values = ['installs_original','activations','ecommerce_purchases'],index = ['app_name','network_name','date_utc'],aggfunc = np.sum)
unatt_pivot = unatt_pivot.reset_index()

#combine email and unatt
email_unatt_final = unatt_pivot.append(email_pivot)
#write to csv
email_unatt_final.to_csv("email_unatt.csv")




