import numpy as np
import pandas as pd
from pandas import json_normalize
import requests
import logging


class CapstoneUpdate():

    def __init__(self):
        self.filePath = 'filePath'
        logging.basicConfig(filename="webCapstones.log", level=logging.INFO)

    def import_file(self):
        self.df = pd.read_csv('dataFiles/cap23-24.csv')
        print(self.df.columns)

    def rest_import(self):
        url = "https://wagner.nyu.edu/api/capstone_salesforce"

        payload = {}
        headers = {
        'Authorization': 'Basic bnl1ODE6dHJhdj1scGxhbm49cjEu',
        'Cookie': 'NO_CACHE=1; SimpleSAMLSessionID=f23d0c7cde1e3cce33f80be51e1ce007'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        #print(response.text)
        dat = response.json()
        self.df = pd.json_normalize(dat)
        logging.info(self.df.head())

    def sf(self):
        from credentials_connection import User
        matt = User('dev')
        matt.getCredentials()
        salesfoce_obj = matt.sf_login()
        return salesfoce_obj

    def format_focus_areas(self):
        for index, row in self.df.iterrows():
            try:
                self.df.at[index, 'Focus Areas'] = row['Focus Areas'].replace(',', ';')
            except:
                print('No Focus Area')
        return self.df
    
    def update_columns(self):
        # TO DO
        # Add Correct Column Names
        self.df.rename(columns = {'Client': 'AccountName', 'Capstone Program': 'Course__c', 'Focus Areas': 'FocusAreas__c'})

    def preview_df(self):
        print(self.df)
