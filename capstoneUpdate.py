import numpy as np
import pandas as pd
from pandas import json_normalize
import requests
import logging


class CapstoneUpdate():

    def __init__(self):
        self.filePath = 'filePath'
        logging.basicConfig(filename="webCapstones.log", level=logging.INFO, filemode='w')

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
        logging.info(self.df.columns)

    def sf(self):
        from credentials_connection import User
        matt = User('dev')
        matt.getCredentials()
        salesfoce_obj = matt.sf_login()
        self.sf = salesfoce_obj
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

    def match_capstone(self):
        for index, row in self.df.iterrows():
            resp = self.sf.query_all("SELECT Id FROM Capstone__c WHERE Capstone_Client__c LIKE '" + row['field_capstone_client'] + "' AND Title__c LIKE '" + row['title'] + "'")['records']
            if(len(resp)>0):
                logging.info(resp[0]['Id'])
            else:
                logging.info('create')
    #             'title', 'field_areas_of_impact', 'body', 'field_academic_year',
    #    'field_capstone_course', 'field_course_subject',
    #    'field_capstone_program', 'delta', 'field_capstone_client'],
                #self.sf.Capstone__c.create()
                self.sf.Capstone__c.create({'Body__c': row['body'],
                                            'Capstone_Client__c': row['field_capstone_client'],
                                            'field_capstone_program': row['Course_Subject__c'],
                })
