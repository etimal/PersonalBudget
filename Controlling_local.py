#generic/built-in
import os
import json
import logging
from os import scandir
from datetime import datetime

#installed libs
import numpy as np
import pandas as pd

#own modules
from log import logger_configuration
logger_configuration()

''' 
###### run mode ######
# mode 1 -> incremental refresh, 
# mode 2 -> full refresh
'''
run_mode = 2
EXPORT_TO_LOCAL = True

#setup variables
structure_filename = 'column_structure.json'
column_structure = os.path.join(os.getcwd(), structure_filename)
column_structure = json.load(open(column_structure))
STRUCTURE_INCOMES          = column_structure['Incomes']
STRUCTURE_EXPENSES         = column_structure['Expenses']
STRUCTURE_INVESTMENT       = column_structure['Investment']
STRUCTURE_INVESTMENT_YTD   = column_structure['InvestmentYTD']
STRUCTURE_ACCOUNTS         = column_structure['Accounts']
STRUCTURE_ACCOUNTS_BALANCE = column_structure['AccountsBalance']
STRUCTURE_CATEGORIES       = column_structure['Categories']
STRUCTURE_UPDATES          = []

def load_env_variables(file_path):
    from dotenv import load_dotenv
    load_dotenv(file_path)

def convert_date(timestamp):
    d = datetime.utcfromtimestamp(timestamp)
    formated_date = d.strftime('%d %b %Y  %H:%M:%S')
    return formated_date

def get_files(directory:str, run_mode:str):
    dir_entries = scandir(directory)
    files = []
    result = []
    for entry in dir_entries:
        if entry.is_file():
            # info = entry.stat()
            # print(f'{entry.name}\t Last Modified: {convert_date(info.st_mtime)}')
            files.append(entry.path)
            print(f' file collected: {entry.path}')
    files.sort()

    if run_mode == 'all_files':
        result = files
    elif run_mode == 'current_month':
        # year = entry.name.split('_')[0]
        # month = entry.name.split('_')[1]
        # file_month = date(int(year),int(month),1)
        # current_month = datetime.now().date().replace(day=1)
        # if file_month == current_month:
        #     files.append(entry.path)
        result.append(files[-1])
    else:
        raise Exception('run_mode invalid')
    return result

def check_data_integrity(df:object, check_col:str):
    integrity = False
    if df[check_col].isnull().values.any() == False:
        integrity = True
        # print(df.shape)
        # print('key column integrity cheked')
    else:
        print('check integrity')
    return integrity

def get_expenses(xlsx):
    df_expenses = pd.read_excel(xlsx,
            sheet_name='Expenses',
            header=2,
            usecols=lambda x: x in STRUCTURE_EXPENSES
            )

    if df_expenses.empty == True:
        raise Exception('df_expenses is empty')

    #Check colomuns integrity
    missing_columns = []
    for c in STRUCTURE_EXPENSES:
        if c not in df_expenses.columns:
            missing_columns.append(c)
    if len(missing_columns)>0:
        df_expenses = df_expenses.reindex(columns = df_expenses.columns.tolist() + missing_columns)
        # for c in missing_columns:
            # df_expenses[c] = None
        df_expenses = df_expenses[STRUCTURE_EXPENSES]

    #Rename columns to lower case
    df_expenses.columns = df_expenses.columns.str.lower()

    ############### FILTERS ###############
    # df = df['status'] != 'Total '
    # df = df[df['status'].isin(['paid', 'planned'])]
    df_expenses.dropna(
            subset=['date'],        #Colums to look for missing values
            thresh=1,               #Rows with at least 1 non-NA values  
            inplace=True)           #Keep df with valid entries in the same variable
    
    #Determine dtype automatically
    df_expenses = df_expenses.convert_dtypes()
    
    #Check data integrity of key column
    check_data_integrity(df=df_expenses, check_col='date')

    #Truncate date to month
    df_expenses['source_period'] = df_expenses['date'].dt.to_period(freq='M')

    #Add source's name
    df_expenses['source_name'] = str(xlsx.io).split('\\')[-1]
    return df_expenses

def get_incomes(xlsx):
    df_incomes = pd.read_excel(xlsx,
        sheet_name='Income',
        header=2,
        usecols=lambda x: x in STRUCTURE_INCOMES
        ) 
    if df_incomes.empty == True:
        raise Exception('df_incomes is empty')

    #Check colomuns integrity
    missing_columns = []
    for c in STRUCTURE_INCOMES:
        if c not in df_incomes.columns:
            missing_columns.append(c)
    if len(missing_columns)>0:
        df_incomes = df_incomes.reindex(columns = df_incomes.columns.tolist() + missing_columns)
        df_incomes = df_incomes[STRUCTURE_INCOMES]

    #Rename columns to lower case
    df_incomes.columns = df_incomes.columns.str.lower()

    #Clean NaN rows
    df_incomes.dropna(
        subset=['date','account'],
        thresh=2,
        inplace=True)

    #Determine dtype automatically
    df_incomes = df_incomes.convert_dtypes()

    #Check data integrity of key column
    check_data_integrity(df=df_incomes, check_col='date')

    #Truncate date to month
    df_incomes['source_period'] = df_incomes['date'].dt.to_period(freq='M')

    #Add source's name
    df_incomes['source_name'] = str(xlsx.io).split('\\')[-1]   
    return df_incomes

def get_investment(xlsx):
    df_investment = pd.read_excel(xlsx,
        sheet_name='Investment',
        header=2,
        usecols=lambda x: x in STRUCTURE_INVESTMENT
        ) 
    if df_investment.empty == True:
        raise Exception('df_investment is empty')
    
    #Check colomuns integrity
    missing_columns = []
    for c in STRUCTURE_INVESTMENT:
        if c not in df_investment.columns:
            missing_columns.append(c)
    if len(missing_columns)>0:
        df_investment = df_investment.reindex(columns = df_investment.columns.tolist() + missing_columns)
        df_investment = df_investment[STRUCTURE_INVESTMENT]

    #Rename columns to lower case
    df_investment.columns = df_investment.columns.str.lower()

    #Clean NaN rows
    df_investment.dropna(
        subset=['date','account'],
        thresh=2,
        inplace=True)

    #Determine dtype automatically
    df_investment = df_investment.convert_dtypes()

    #Check data integrity of key column
    check_data_integrity(df=df_investment, check_col='date')

    #Truncate date to month
    df_investment['source_period'] = df_investment['date'].dt.to_period(freq='M')

    #Add source's name
    df_investment['source_name'] = str(xlsx.io).split('\\')[-1]
    return df_investment

def get_investment_ytd(xlsx):
    df_investment_ytd = pd.read_excel(xlsx,
        sheet_name='Total Investment',
        header=2,
        usecols=lambda x: x in STRUCTURE_INVESTMENT_YTD
        )
    if df_investment_ytd.empty == True:
        raise Exception('df_investment_ytd is empty')

    #Check colomuns integrity
    missing_columns = []
    for c in STRUCTURE_INVESTMENT_YTD:
        if c not in df_investment_ytd.columns:
            missing_columns.append(c)
    if len(missing_columns)>0:
        df_investment_ytd = df_investment_ytd.reindex(columns = df_investment_ytd.columns.tolist() + missing_columns)
        df_investment_ytd = df_investment_ytd[STRUCTURE_INVESTMENT_YTD]

    #Rename columns to lower case
    df_investment_ytd.columns = df_investment_ytd.columns.str.lower()

    #Clean NaN rows
    df_investment_ytd.dropna(
        subset=['date'],
        thresh=1,
        inplace=True)

    #Determine dtype automatically
    df_investment_ytd = df_investment_ytd.convert_dtypes()

    #Change column type to string
    df_investment_ytd['month']= df_investment_ytd['month'].astype('string')
    
    #Remove row with numbers
    df_investment_ytd = df_investment_ytd[~df_investment_ytd['month'].str.contains(r'[0-9]') ]

    #Reset index and drop old index enable
    df_investment_ytd.reset_index(drop=True, inplace=True)
  
    #Verify number of months
    if len(df_investment_ytd) != 12:
        print('Check data type')

    #Check data integrity of key column
    check_data_integrity(df=df_investment_ytd, check_col='date')

    #Truncate date to month
    source_name = str(xlsx.io).split('\\')[-1]
    period = source_name.split('_')[0] + '-' + source_name.split('_')[1]
    df_investment_ytd['source_period'] = pd.Period(period)

    #Add source's name
    df_investment_ytd['source_name'] = source_name
    return df_investment_ytd

def get_accounts(xlsx):
    df_accounts = pd.read_excel(xlsx,
        sheet_name='Accounts',
        header=2,
        usecols=lambda x: x in STRUCTURE_ACCOUNTS
        )
    if df_accounts.empty == True:
        raise Exception('df_accounts is empty')

    #Check colomuns integrity
    missing_columns = []
    for c in STRUCTURE_ACCOUNTS:
        if c not in df_accounts.columns:
            missing_columns.append(c)
    if len(missing_columns)>0:
        df_accounts = df_accounts.reindex(columns = df_accounts.columns.tolist() + missing_columns)
        df_accounts = df_accounts[STRUCTURE_ACCOUNTS]

    #Rename columns to lower case
    df_accounts.columns = df_accounts.columns.str.lower()
    
    #Clean NaN rows
    df_accounts.dropna(
        subset=['account_id'],
        thresh=1,
        inplace=True)

    #Determine dtype automatically
    df_accounts = df_accounts.convert_dtypes()

    #Check data integrity of key column
    check_data_integrity(df=df_accounts, check_col='account_id')
    
    #Truncate date to month
    source_name = str(xlsx.io).split('\\')[-1]
    period = source_name.split('_')[0] + '-' + source_name.split('_')[1]
    df_accounts['source_period'] = pd.Period(period)

    #Add source's name
    df_accounts['source_name'] = source_name 

    num_accts = len(df_accounts['account_id'])
    return df_accounts, num_accts

def get_accounts_balance(xlsx, num_accts:int):
    df_balance = pd.read_excel(xlsx,
        sheet_name='Accounts Balance',
        header=2,
        usecols=lambda x: x in STRUCTURE_ACCOUNTS_BALANCE
        )
    if df_balance.empty == True:
        raise Exception('df_balance is empty')

    #Check colomuns integrity
    missing_columns = []
    for c in STRUCTURE_ACCOUNTS_BALANCE:
        if c not in df_balance.columns:
            missing_columns.append(c)
    if len(missing_columns)>0:
        df_balance = df_balance.reindex(columns = df_balance.columns.tolist() + missing_columns)
        df_balance = df_balance[STRUCTURE_ACCOUNTS_BALANCE]

    #Rename columns to lower case
    df_balance.columns = df_balance.columns.str.lower()
    
    #Select index rows (filter) based on number of acccounts
    df_balance = df_balance.loc[0:num_accts-1]

    #Determine dtype automatically
    df_balance = df_balance.convert_dtypes()

    #Check data integrity of key column
    check_data_integrity(df=df_balance, check_col='account')

    #Truncate date to month
    source_name = str(xlsx.io).split('\\')[-1]
    period = source_name.split('_')[0] + '-' + source_name.split('_')[1]
    df_balance['source_period'] = pd.Period(period)

    #Add source's name
    df_balance['source_name'] = source_name  
    return df_balance

def remove_spaces_from_columns(df:pd.DataFrame):
    new_columns_dict = {}

    rule_eval = [x for x in df.columns.to_list() if x.__contains__(' ') ]
    if len(rule_eval) > 0:
        new_columns = [x.replace(' ', '_') for x in rule_eval]
        #append new columns names to dict
        for i, col in enumerate(rule_eval):
            new_columns_dict[col] = new_columns[i]
        if len(new_columns_dict) == len(rule_eval):
            return True, new_columns_dict
    else:
        return False , new_columns_dict

def verify_column_type(df:pd.DataFrame, target_types:list):
    new_column_types = {}
    rule_eval = list(df.select_dtypes(include=target_types))
    
    dafault_type = str
    if len(rule_eval) > 0:
        for col in rule_eval:
            new_column_types[col] = dafault_type
        return True, new_column_types
    else:
        return False, new_column_types

def DataCollection(paths:list):
    i = 0
    for file_path in paths:
        xlsx = pd.ExcelFile(file_path)
        expenses    = get_expenses(xlsx)
        incomes     = get_incomes(xlsx)
        investment  = get_investment(xlsx)
        investment_ytd      = get_investment_ytd(xlsx)
        accounts, num_accts = get_accounts(xlsx)
        accounts_balance    = get_accounts_balance(xlsx, num_accts)

        if i ==0:
            df_expenses     = expenses
            df_incomes      = incomes
            df_investment   = investment
            df_investment_ytd   = investment_ytd
            df_accounts         = accounts
            df_accounts_balance = accounts_balance
        else:
            df_expenses     = pd.concat([df_expenses, expenses], ignore_index=True)
            df_incomes      = pd.concat([df_incomes, incomes], ignore_index=True)
            df_investment   = pd.concat([df_investment, investment], ignore_index=True)
            df_investment_ytd   = pd.concat([df_investment_ytd, investment_ytd], ignore_index=True)
            df_accounts         = pd.concat([df_accounts, accounts], ignore_index=True)
            df_accounts_balance = pd.concat([df_accounts_balance, accounts_balance], ignore_index=True)
        i=+1
        # print('file %s compleated' % file_path.split('\\')[-1] )
    
    #Reset index and set index name
    index_name = 'id'
    df_expenses.reset_index(drop=True, inplace=True)
    df_expenses.rename_axis(index_name, inplace=True)
    rename_cols, names_dict = remove_spaces_from_columns(df=df_expenses)
    if rename_cols == True:
        df_expenses.rename(columns=names_dict, inplace=True)

    df_incomes.reset_index(drop=True, inplace=True)
    df_incomes.rename_axis(index_name, inplace=True)
    rename_cols, names_dict = remove_spaces_from_columns(df=df_incomes)
    if rename_cols == True:
        df_incomes.rename(columns=names_dict, inplace=True)

    df_investment.reset_index(drop=True, inplace=True)
    df_investment.rename_axis(index_name, inplace=True)
    rename_cols, names_dict = remove_spaces_from_columns(df=df_investment)
    if rename_cols == True:
        df_investment.rename(columns=names_dict, inplace=True)

    df_investment_ytd.reset_index(drop=True, inplace=True)
    df_investment_ytd.rename_axis(index_name, inplace=True)
    rename_cols, names_dict = remove_spaces_from_columns(df=df_investment_ytd)
    if rename_cols == True:
        df_investment_ytd.rename(columns=names_dict, inplace=True)

    df_accounts.reset_index(drop=True, inplace=True)
    df_accounts.rename_axis(index_name, inplace=True)
    rename_cols, names_dict = remove_spaces_from_columns(df=df_accounts)
    if rename_cols == True:
        df_accounts.rename(columns=names_dict, inplace=True)

    df_accounts_balance.reset_index(drop=True, inplace=True)
    df_accounts_balance.rename_axis(index_name, inplace=True)
    rename_cols, names_dict = remove_spaces_from_columns(df=df_accounts_balance)
    if rename_cols == True:
        df_accounts_balance.rename(columns=names_dict, inplace=True)

    #Set df names
    df_expenses.name = 'expenses'
    df_incomes.name = 'incomes'
    df_investment.name = 'investment'
    df_investment_ytd.name = 'investment_ytd'
    df_accounts.name = 'accounts'
    df_accounts_balance.name = 'accounts_balance'

    #Setting data format
    for df in [df_expenses, df_incomes, df_investment, df_investment_ytd, df_accounts, df_accounts_balance]:
        if df.name == 'expenses':
            df['date'] = df['date'].dt.strftime('%Y-%m-%d')
            df = df_expenses
        elif df.name == 'incomes':
            df['date'] = df['date'].dt.strftime('%Y-%m-%d')
            df = df_incomes
        elif df.name == 'investment':
            df['date'] = df['date'].dt.strftime('%Y-%m-%d')
            df = df_investment
        elif df.name == 'investment_ytd':
            df['date'] = df['date'].dt.strftime('%Y-%m-%d')
            df = df_investment_ytd
        elif df.name == 'accounts':
            pass
        elif df.name == 'accounts_balance':
            df['period'] = df['period'].dt.strftime('%Y-%m-%d')
            df['check_date'] = df['check_date'].dt.strftime('%Y-%m-%d')
            df = df_accounts_balance

    return df_expenses, df_incomes, df_investment, df_investment_ytd, df_accounts, df_accounts_balance

def ReadSource(run_mode:int):
    source_mode = None
    DIRECTORY = os.getenv(r'DIRECTORY_LOCATION')
    
    if run_mode == 1:
        source_mode = 'current_month'
    elif run_mode == 2:
        source_mode = 'all_files'

    files = get_files(DIRECTORY,source_mode)
    expenses, incomes, investment, investment_ytd, accounts, accounts_balance = DataCollection(paths=files)

    #Overview
    column_a = 'Dataset'
    column_b = 'Shape'
    column_c = 'N° Files'
    column_d = 'LastSourcePeriod'

    data = {column_a : [expenses.name, incomes.name, investment.name, investment_ytd.name, accounts.name, accounts_balance.name],
            column_b : [expenses.shape, incomes.shape, investment.shape, investment_ytd.shape, accounts.shape, accounts_balance.shape],
            column_c : [len(expenses['source_name'].unique()),
                        len(incomes['source_name'].unique()),
                        len(investment['source_name'].unique()),
                        len(investment_ytd['source_name'].unique()),
                        len(accounts['source_name'].unique()),
                        len(accounts_balance['source_name'].unique())],
            column_d : [
                        max(expenses['source_period']),
                        max(incomes['source_period']), 
                        max(investment['source_period']),
                        max(investment_ytd['source_period']),
                        max(accounts['source_period']),
                        max(accounts_balance['source_period'])]
            }
    data = pd.DataFrame(data)
    print(data)

    #Export to db
    '''
        Use pd.Timestamp.now() to get local time
        Use pd.Timestamp.utcnow() or pd.to_datetime('now') to get UTC time
        reference: https://pandas.pydata.org/docs/reference/api/pandas.Timestamp.html
    '''
    now = pd.Timestamp.now()
    db_last_update = 'db_update'

    if run_mode == 1:
        DB_DIRECTORY = os.getenv(r'DB_LOCATION')
        db_mode = 'all_files'
        paths = get_files(DB_DIRECTORY,db_mode)
        if len(paths) == 0:
            raise Exception('No databases founded')

        for df in [expenses, incomes, investment, investment_ytd, accounts, accounts_balance]:
            PATH_TO_DB = os.path.join(os.getenv(r'DB_LOCATION'), '%s.csv') %df.name
            df[db_last_update] = now
            df[db_last_update] = df[db_last_update].dt.strftime('%Y-%m-%d %H:%M:%S')

            db = pd.read_csv(PATH_TO_DB)
            if df.name == 'accounts':
                db = db.astype({db_last_update: "datetime64[ns]"})
                db[db_last_update] = db[db_last_update].dt.strftime('%Y-%m-%d %H:%M:%S')
            elif df.name == 'accounts_balance':
                db = db.astype({"check date": "datetime64[ns]", db_last_update: "datetime64[ns]"})
                db['check date'] = db['check date'].dt.strftime('%Y-%m-%d')
                db[db_last_update] = db[db_last_update].dt.strftime('%Y-%m-%d %H:%M:%S')
            else:
                db = db.astype({"date": "datetime64[ns]", db_last_update: "datetime64[ns]"})
                db['date'] = db['date'].dt.strftime('%Y-%m-%d')
                db[db_last_update] = db[db_last_update].dt.strftime('%Y-%m-%d %H:%M:%S') 
     
            MAX_DB_PERIOD = pd.Period(max(db['source_period'].unique()))    #Get last dataset
            MAX_SOURCE_PERIOD = max(df['source_period'].unique())

            if MAX_SOURCE_PERIOD == MAX_DB_PERIOD:
                db = db[ db['source_period'] != str(MAX_DB_PERIOD)]         #Remove last dataset

            elif MAX_SOURCE_PERIOD < MAX_DB_PERIOD:
                raise Exception('db period is higher than source')

            db = pd.concat([db,df], ignore_index=True)                      #Adding new dataset
            db.reset_index(drop=True, inplace=True)
            db.rename_axis('id', inplace=True)
            db = db.drop(columns=['id'])
            if EXPORT_TO_LOCAL == True:
                db.to_csv(PATH_TO_DB,encoding='utf-8-sig', index=True)      #Save dataset
                print('DB name: %s updated' %df.name)
            else:
                print(f'DB to update: {df.name}')

    elif run_mode == 2:
        for df in [expenses, incomes, investment, investment_ytd, accounts, accounts_balance]:
            PATH_TO_DB = os.path.join(os.getenv(r'DB_LOCATION'), '%s.csv') %df.name
            df_name = df.name
            df[db_last_update] = now
            df[db_last_update] = df[db_last_update].dt.strftime('%Y-%m-%d %H:%M:%S')            
            
            if EXPORT_TO_LOCAL == True:
                df.to_csv(PATH_TO_DB, encoding='utf-8-sig')
                print('DB name: %s created' %df_name)
            else:
                print(f'DB to create: {df_name}')


if __name__ == "__main__":
    ENV_NAME = 'dev'
    ENV_PATH = os.path.join(os.getcwd(), 'env', f'{ENV_NAME}.env')
    load_env_variables(file_path=ENV_PATH)
    logging.info(f'variables for {ENV_NAME} env loaded')

    ReadSource(run_mode)