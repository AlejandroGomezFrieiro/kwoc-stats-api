import copy
import csv
import os
import json
import requests
import sys 
import time
import pandas as pd
import gspread as gs
import numpy as np

# Email to share the worksheet with. Client email
to_share_email = 'target_email@gmail.com'

# Create a pandas dataframe with the csv file
dataframe = pd.read_csv('students_.csv')

# Fix problems with inadequate inputs (empty input in csv file gives a NaN on pandas)
dataframe.fillna('', inplace=True)

# Set extra columns
midevals_cleared_array = [0] * (len(dataframe.index))
endevals_cleared_array = [0] * (len(dataframe.index))
feedback = [''] * (len(dataframe.index))

dataframe['midevals_cleared'] = midevals_cleared_array
dataframe['endevals_cleared'] = endevals_cleared_array
dataframe['feedback'] = feedback

# Connect to your account using credentials. Obtain credentials following this guide "https://gspread.readthedocs.io/en/latest/oauth2.html#enable-api-access-for-a-project"
gc = gs.service_account(filename='./env/api_credentials.json')

# Create a new spreadsheet
sh = gc.create('kwoc-stats-api')

# Create worksheet with name Students
worksheet = sh.add_worksheet(title="Students", rows=str(len(dataframe.index)), cols="5")

# Populate worksheet with pandas dataframe
worksheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())

# Share account with email
sh.share(to_share_email, perm_type='user', role='writer')
