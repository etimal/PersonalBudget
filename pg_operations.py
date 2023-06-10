#generic/built-in
import os
import logging

#installed libs
import pandas as pd

#own modules
import pg_db
from log import logger_configuration
logger_configuration()

#load env variables
def load_env_variables(file_path):
    from dotenv import load_dotenv
    load_dotenv(file_path)

def scan_directory(dir:str):
    dir_entries = os.scandir(dir)
    files = {}
    for entry in dir_entries:
        if entry.is_file():
            files[entry.name] = entry.path
    logging.info(f'files on {dir}: {len(files)}')
    return files

def connect_to_db():
    db = pg_db.Database()
    db.create_connection()
    logging.info(f'db connection: {db.connection}')
    return db

def create_table():
    db = pg_db.Database()
    db.create_connection()
    logging.info(f'db connection: {db.connection}')
    query_name = 'accounts_balance.sql'
    path_to_query = os.path.join('src','tables',query_name)
    db.create_table_from_file(path_to_query)

def create_tables():
    db = pg_db.Database()
    db.create_connection()
    logging.info(f'db connection: {db.connection}')

    table_sql_files = scan_directory(dir=r'src\\tables')
    for table in table_sql_files:
        logging.info(f"execute 'create table' for {table}")
        path_to_query = table_sql_files.get(table)
        db.create_table_from_file(path_to_query)

def delete_tables():
    db = connect_to_db()
    table_sql_files = scan_directory(dir=r'src\\tables')
    for table in table_sql_files:
        logging.info(f"execute 'drop table' for {table}")
        table_name = table.split("\\")[-1].replace('.sql','')
        db.drop_table(table=table_name)

def insert_data_into_table():
    db = connect_to_db()
    db_path = os.getenv('DB_LOCATION')
    table_name = 'accounts'
    table_path = os.path.join(db_path, f'{table_name}.csv')
    df = pd.read_csv(table_path, encoding='utf-8-sig', delimiter=',')
    df.drop(columns=['id'], inplace=True)   #id will be placed automatically on postgre
    df = df.iloc[:5]
    db.insert_into_table(df=df, table=table_name)

def main():
    ENV_NAME = 'dev'
    ENV_PATH = os.path.join(os.getcwd(), 'env', f'{ENV_NAME}.env')
    load_env_variables(file_path=ENV_PATH)
    logging.info(f'variables for {ENV_NAME} env loaded')

    # execute operation
    # delete_tables()

if __name__ == "__main__":
    main()