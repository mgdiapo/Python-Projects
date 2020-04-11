 # -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 13:34:20 2019

@author: michael.gutierrez
"""

import pandas as pd
import boto3
from win32com.client import Dispatch
import datetime
from io import StringIO

#retrieve attachment from email, make sure to run on date when email is recieved 
outlook = Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder("6")
all_inbox = inbox.Items
val_date = datetime.date.today()

#Define subject of email of interest
sub_today = ''
att_today = ''

#Searches inbox for message that has subject line of interest
for msg in all_inbox:
    if msg.Subject.find(sub_today) != -1 and msg.Senton.date() == val_date:
        break

for att in msg.Attachments:
    if att.FileName == att_today:
        break    
#retrieves and saves file to specific directory
try:
#define place to save the file
    att.SaveAsFile('' + att.FileName)
    print("Succesful")
except:
    print("Attachment Download Failed/No message found")    
    

#Read in sales info, change path if needed 
df_sales_sales = pd.concat(pd.read_excel("",sheet_name = None, skiprows = 3,usecols = "C:Q" ).values(),axis = 1)

#Read in stores list
df_sales_stores = pd.concat(pd.read_excel("",sheet_name = None, skiprows = 3,usecols = "A:B" ).values(),axis = 1)

#Read in matching table
df_match = pd.read_csv("")

#Get most up to date store list
df_sales_stores = df_sales_stores.iloc[:,list(range(2))]

#Remove unecessary observations from data #after row
df_sales_sales = df_sales_sales.iloc[:-8]
df_sales_stores = df_sales_stores.iloc[:-8]

#Join stores list and sales info
df_sales_xls = pd.concat([df_sales_stores,df_sales_sales],axis = 1)

#Pivot data
pivot_df_sales = df_sales_xls.melt(id_vars = ['Unnamed: 0', 'Store'], var_name = "date", value_name = "sales")

#Remove where sales = 0
pivot_df_sales = pivot_df_sales[pivot_df_sales.sales!=0]

#Remove where date = Unamed :7
pivot_df_sales = pivot_df_sales[pivot_df_sales.date!="Unnamed: 7"]

#Join on match table
df_final = pd.merge(pivot_df_sales, df_match, left_on = 'Store', right_on = 'store_num_location_state', how = 'left')

#Reorder columns for easy loading into S3
df_final_v2 = df_final[['date','storenum','store_num_location_state','asm_location_name','sales']]

#days to keep, change based on desired range
x = datetime.date.today() - datetime.timedelta(days=30)

#convert dates to datetime
df_final_v2['date'] = pd.to_datetime(df_final_v2['date'])

#retrieve days to keep from df
df_keep = df_final_v2[(df_final_v2['date'] >= x )]

#retrieve old data from s3 bucket

#imput keys
access_key = ''
secret_key = ''
s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key = secret_key)

#retreive file/define bucket and file of interest
csv_obj = s3.get_object(Bucket='bucket', Key='old file')

#convert file to df
body = csv_obj['Body']
csv_string = body.read().decode('utf-8')
old_df = pd.read_csv(StringIO(csv_string))

#convert old_df['date'] to dt
old_df['date'] = pd.to_datetime(old_df['date'])

#specifiy old data to remain unchanged
old_df_keep = old_df[(old_df['date'] < x)]

#combine old/new data
df_combined = old_df_keep.append(df_keep)

#Write to csv, renmae file path to reflect current data
df_combined.to_csv(".csv", index = False)

#Upload fiel to s3 bucket
s3.upload_file ('.csv','bucket','.csv')



