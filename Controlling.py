import os
from os import scandir
from datetime import date, datetime

import pandas as pd
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

STRUCTURE_EXPENSES         = ['DATE','ACCOUNT','CATEGORY','DESCRIPTION','STATUS','AMOUNT']   #[each_string.upper() for each_string in STUCTURE_EXPENSES]
STRUCTURE_INCOMES          = ['DATE','ACCOUNT','DESCRIPTION','AMOUNT']
STRUCTURE_INVESTMENT       = ['DATE', 'ACCOUNT', 'AMOUNT', 'COMMENT']
STRUCTURE_INVESTMENT_YTD   = ['DATE', 'MONTH', 'AMOUNT', 'COMMENT']
STRUCTURE_ACCOUNTS         = ['ACCOUNT_ID', 'ACCOUNT', 'CURRENCY', 'COUNTRY','ITEM','TYPE','COMMENT']
STRUCTURE_ACCOUNTS_BALANCE = ['ACCOUNT', 'LAST BALANCE', 'PERIOD', 'ASSIGNMENT','INCOMES','TRANSFERS','AMOUNT','EXPENSES','TOTAL PERIOD','TOTAL ACCOUNT','NEW BALANCE','CHECK DATE']
STRUCTURE_CATEGORIES       = ['CATEGORY_ID', 'CATEGORY', 'TYPE', 'GROUP', 'COMMENT']
STRUCTURE_UPDATES          = []

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
            # print(entry.path)
            files.append(entry.path)
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

def get_expenses(xls):
    df_expenses = pd.read_excel(xls,
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
    df_expenses['source_name'] = str(xls.io).split('\\')[-1]
    return df_expenses

def get_incomes(xls):
    df_incomes = pd.read_excel(xls,
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
    df_incomes['source_name'] = str(xls.io).split('\\')[-1]   
    return df_incomes

def get_investment(xls):
    df_investment = pd.read_excel(xls,
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
    df_investment['source_name'] = str(xls.io).split('\\')[-1]
    return df_investment

def get_investment_ytd(xls):
    df_investment_ytd = pd.read_excel(xls,
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
    source_name = str(xls.io).split('\\')[-1]
    period = source_name.split('_')[0] + '-' + source_name.split('_')[1]
    df_investment_ytd['source_period'] = pd.Period(period)

    #Add source's name
    df_investment_ytd['source_name'] = source_name
    return df_investment_ytd

def get_accounts(xls):
    df_accounts = pd.read_excel(xls,
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
    source_name = str(xls.io).split('\\')[-1]
    period = source_name.split('_')[0] + '-' + source_name.split('_')[1]
    df_accounts['source_period'] = pd.Period(period)

    #Add source's name
    df_accounts['source_name'] = source_name 

    num_accts = len(df_accounts['account_id'])
    return df_accounts, num_accts

def get_accounts_balance(xls, num_accts:int):
    df_balance = pd.read_excel(xls,
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
    source_name = str(xls.io).split('\\')[-1]
    period = source_name.split('_')[0] + '-' + source_name.split('_')[1]
    df_balance['source_period'] = pd.Period(period)

    #Add source's name
    df_balance['source_name'] = source_name  
    return df_balance

def DataCollection(paths:list):
    i = 0
    for file_path in paths:
        xls = pd.ExcelFile(file_path)
        expenses = get_expenses(xls)
        incomes = get_incomes(xls)
        investment = get_investment(xls)
        investment_ytd =  get_investment_ytd(xls)
        accounts, num_accts = get_accounts(xls)
        accounts_balance = get_accounts_balance(xls, num_accts)

        if i ==0:
            df_expenses = expenses
            df_incomes = incomes
            df_investment = investment
            df_investment_ytd = investment_ytd
            df_accounts = accounts
            df_accounts_balance = accounts_balance
        else:
            df_expenses = df_expenses.append(expenses)
            df_incomes = df_incomes.append(incomes)
            df_investment = df_investment.append(investment)
            df_investment_ytd = df_investment_ytd.append(investment_ytd)
            df_accounts = df_accounts.append(accounts)
            df_accounts_balance = df_accounts_balance.append(accounts_balance)
        i=+1
        # print('file %s compleated' % file_path.split('\\')[-1] )
    
    #Reset index and set index name
    index_name = 'id'
    df_expenses.reset_index(drop=True, inplace=True)
    df_expenses.rename_axis(index_name, inplace=True)

    df_incomes.reset_index(drop=True, inplace=True)
    df_incomes.rename_axis(index_name, inplace=True)

    df_investment.reset_index(drop=True, inplace=True)
    df_investment.rename_axis(index_name, inplace=True)

    df_investment_ytd.reset_index(drop=True, inplace=True)
    df_investment_ytd.rename_axis(index_name, inplace=True)

    df_accounts.reset_index(drop=True, inplace=True)
    df_accounts.rename_axis(index_name, inplace=True)

    df_accounts_balance.reset_index(drop=True, inplace=True)
    df_accounts_balance.rename_axis(index_name, inplace=True)

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
            df['check date'] = df['check date'].dt.strftime('%Y-%m-%d')
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

            db = db.append(df)                                              #Adding new dataset
            db.reset_index(drop=True, inplace=True)
            db.rename_axis('id', inplace=True)
            db = db.drop(columns=['id'])
            db.to_csv(PATH_TO_DB,encoding='utf-8-sig', index=True)          #Save dataset
            print('DB name: %s updated' %df.name)

    elif run_mode == 2:
        for df in [expenses, incomes, investment, investment_ytd, accounts, accounts_balance]:
            PATH_TO_DB = os.path.join(os.getenv(r'DB_LOCATION'), '%s.csv') %df.name
            df[db_last_update] = now
            df[db_last_update] = df[db_last_update].dt.strftime('%Y-%m-%d %H:%M:%S')            
            df.to_csv(PATH_TO_DB, encoding='utf-8-sig')
            print('DB name: %s created' %df.name)



# 1: incremental refresh, 
# 2: full refresh
run_mode = 2
ReadSource(run_mode)


# https://realpython.com/working-with-files-in-python/#getting-file-attributes
# https://pythoslabs.medium.com/4-ways-to-filter-numeric-values-in-dataframes-using-pandas-f69ca3f33b05
# https://www.geeksforgeeks.org/pandas-remove-rows-with-special-characters/