import pyodbc
import pandas as pd
import datetime
import json
import utils
import os

with open('/root/connectin/config.json', 'r') as f:

    main_config = json.load(f)

with open('/root/connectin/credentials.json', 'r') as f_credentials:
    credentials_config = json.load(f_credentials)

if __name__ == '__main__':
        data_not_empty = True
    
        mssql_tables = main_config['tables']
        state_file_prefix = main_config['state_file_path_csv']
        
        cnxn = utils.get_connection(driver=main_config['driver'],host=credentials_config['mssql_host'], 
                    port=main_config['mssql_port'], username=main_config['mssql_username'],
                    password=credentials_config['mssql_password'], db=main_config['mssql_database'])


        for table in mssql_tables:
            table_name = table['table_name']
            data_not_empty = True
            while data_not_empty:
                state_file = state_file_prefix + table_name 
                if (os.path.isfile(state_file)):
                       last_state_value = utils.file_read(state_file)
                else:
                       last_state_value = '0'   
                
                print("Selecting from table: {} starting from date: {}".format(table_name,last_state_value))
            
                sql = "SELECT TOP 10000 * FROM " + table_name + " WHERE " + table[
                    'unix_timestamp_column'] + " > " + last_state_value + " ORDER BY DATA_DATE"
                    
                data = utils.execute_sql(cnxn,sql)
                
                file_name = main_config['data_file_path']+table_name+".csv"
                with open(file_name, 'a') as f:
                    data.to_csv(f, encoding='utf-8', index=False)

                if len(data)>0:
                    timestamp = data['DATA_DATE'].iloc[-1]
                    max_auto_increment_value=timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                    print(max_auto_increment_value)
                    utils.file_write(state_file, 'w', "'" + str(max_auto_increment_value)+"'")
                else:
                    data_not_empty = False
