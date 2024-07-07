import numpy as np
import pandas as pd

class CapstoneUpdate():

    def __init__(self, filePath):
        self.filePath = filePath

    def import_file(self):
        self.df = pd.read_csv('dataFiles/cap23-24.csv')
        print(self.df.columns)

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
