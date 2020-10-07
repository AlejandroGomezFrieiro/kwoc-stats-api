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

dataframe.fillna('', inplace=True)
# Create title for the new columns
# midevals_cleared_array = ['midevals_cleared']
# endevals_cleared_array = ['endevals_cleared']


midevals_cleared_array = [0] * (len(dataframe.index))
endevals_cleared_array = [0] * (len(dataframe.index))

dataframe['midevals_cleared'] = midevals_cleared_array
dataframe['endevals_cleared'] = endevals_cleared_array

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