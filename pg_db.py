#generic/built-in
import os
import logging

#installed libs
import psycopg
import pandas as pd

class Database:
    def __init__(self):
        self.client = None
        self.connection = None
        
    def create_connection(self):
        try:
            logging.info("Establish connection to PostgreSQL database")
            keepalive_kwargs = {
            "keepalives": 1,
            "keepalives_idle": 60,
            "keepalives_interval": 10,
            "keepalives_count": 5
            }
            sql_client = psycopg.connect(
                host     ='%s' %os.getenv('DB_HOST'),
                dbname   ='%s' %os.getenv('DB_NAME'),
                user     ='%s' %os.getenv('DB_USER'),
                password ='%s' %os.getenv('DB_PASS'),
                port     ='%s' %os.getenv('DB_PORT'),
                **keepalive_kwargs
            )
        except (Exception, psycopg.DatabaseError) as error:
            logging.error(error)
            raise ValueError(error)
        else:
            self.client = sql_client
            self.connection = True
            logging.info("Connection to PostgreSQL succeeded")
    
    def create_table(self, query:str):
        try:
            resp = self.client.execute(query)
        except Exception as e:
            logging.error(e)
            self.client.rollback()
            return False
        
        # Make the changes to the database persistent
        self.client.commit()
        return True

    def create_table_from_file(self, file_name:str):
        query = open(file_name,'r', encoding='utf-8').read()
        resp = self.create_table(query)
        if resp == True:
            table_name = file_name.split("\\")[-1].replace('.sql','')
            logging.info(f'table {table_name} was created successfully')
    
    def insert_into_table(self, df:pd.DataFrame, table):
        rows = [tuple(x) for x in df.to_numpy()]
        cols = ','.join(list(df.columns.str.lower()))
        placeholders  = ','.join(['%s'] * len(df.columns))

        #query to execute
        query = "INSERT INTO %s (%s) VALUES (%s)" %(table, cols, placeholders)
        try:
            cursor = self.client.cursor()
            cursor.executemany(query, rows)
        except (Exception, psycopg.DatabaseError) as error:
            logging.error(error)
            self.client.rollback()
            cursor.close()
            raise ValueError(error)
        else:
            self.client.commit()
            cursor.close()
            logging.info(f'{len(df)} rows were inserted into table {table}')
    
    def drop_table(self, table:str):
        try:
            query = "DROP TABLE IF EXISTS %s CASCADE" %(table)            
            resp = self.client.execute(query)
        except Exception as e:
            logging.error(e)
            self.client.rollback()
            return False
        else:
            self.client.commit()
            return True