# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 22:26:47 2021

@author: weiha
"""

import snowflake.connector
import pandas as pd
    
# In[located mudule]:

class snowflake_connector:  
    def __init__(self, credential):
        try:
            self.acccount = credential['account']
            self.user = credential['user']
            self.password = credential['pwd']
            self.warehouse = credential['warehouse']      
        except:
            credential_example = {
                'account':'XXXXX',
                'user':'user_name',
                'pwd':'password',
                'warehouse':'XXXX',
                }
            raise ValueError(f"credential format is incorrect \n"
                             f"here is an example: \n"
                             f"{credential_example}"
                             )
            
    def query(self, db, query):
        # build connection
        connection = snowflake.connector.connect(
            account=self.acccount,
            user=self.user,
            password=self.password,
            warehouse=self.warehouse,
            database=db
            ) 
        # run query
        query_result_df = pd.read_sql(query, connection)
        return query_result_df
        