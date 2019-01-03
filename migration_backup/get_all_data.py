import pyodbc
import csv
import utils
import json
import pandas as pd

with open('../config.json', 'r') as f:
    main_config = json.load(f)

with open('../credentials.json', 'r') as f_credentials:
    credentials_config = json.load(f_credentials)

if __name__ == '__main__':
	
	cnxn = utils.get_connection(driver=main_config['driver'],host=credentials_config['mssql_host'], 
                    port=main_config['mssql_port'], username=main_config['mssql_username'],
                    password=credentials_config['mssql_password'], db=main_config['mssql_database'])


	tables = ["DIM_PI", "DIM_FILE_COL_MAP", "DIM_FILE_LOAD_LOG", "DIM_FILE_PATTERN", "DIM_FILE_PROCESS_TYPE", "LOG_EVENT", "LOG_EXECUTION", 
		"STG_EPOCH_RXTX","STG_EPOCH_VALUE", "STG_SPEEDTEST"]
	

for table in tables:
	
	sql = "SELECT * FROM " + table + "";""
	
	data = utils.execute_sql(cnxn,sql)

	file_name = main_config['data_file_path']+table+".csv"

	with open(file_name, 'a') as f:
		data.to_csv(f, encoding='utf-8', index=False)
