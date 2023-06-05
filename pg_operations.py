#generic/built-in
import os
import logging

#own modules
import pg_db
from log import logger_configuration
logger_configuration()

#load env variables
def load_env_variables(file_path):
    from dotenv import load_dotenv
    load_dotenv(file_path)

def main():
    ENV_NAME = 'dev'
    ENV_PATH = os.path.join(os.getcwd(), 'env', f'{ENV_NAME}.env')
    load_env_variables(file_path=ENV_PATH)
    logging.info(f'variables for {ENV_NAME} env loaded')

    db = pg_db.Database()
    db.create_connection()
    logging.info(f'db connection: {db.connection}')


    #create table
    query_name = 'accounts.sql'
    path_to_query = os.path.join('src','tables',query_name)
    db.create_table_from_file(path_to_query)


if __name__ == "__main__":
    main()