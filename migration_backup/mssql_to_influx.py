import pyodbc
import pandas as pd
from influxdb import InfluxDBClient
import datetime
import json
import math
import os.path
import utils

with open('/root/connectin/config.json', 'r') as f:
    main_config = json.load(f)

with open('/root/connectin/credentials.json', 'r') as f_credentials:
    credentials_config = json.load(f_credentials)

if __name__ == '__main__':
    
    mssql_tables = main_config['tables']
    state_file_prefix = main_config['state_file_path']
    block_size = main_config['block_size']

    cnxn = utils.get_connection(driver=main_config['driver'],host=credentials_config['mssql_host'], 
                    port=main_config['mssql_port'], username=main_config['mssql_username'],
                    password=credentials_config['mssql_password'], db=main_config['mssql_database'])

    for table in mssql_tables:
        table_name = table['table_name']
        state_file = state_file_prefix + table_name
        if (os.path.isfile(state_file)):
           last_state_value = utils.file_read(state_file)
        else:
           last_state_value = '0'
        print("Selecting {} rows from table: {} starting from date: {}".format(block_size,table_name,last_state_value))
        columns_list = [table['unix_timestamp_column']]
        for measurement in table['measurments']:
            for item in measurement['columns']:
                columns_list.append(item['column_name'])

        unique_columns_set=set(columns_list)
        columns_list = ','.join(str(s) for s in unique_columns_set)
            
        sql = "SELECT TOP " + block_size + " " + columns_list + " FROM " + table_name + ",DIM_PI WHERE " + table[
                'unix_timestamp_column'] + " >= " + last_state_value  + " AND SK_PI=PK_PI ORDER BY DATA_DATE"

        if table_name=="FCT_PI":
            sql = "SELECT TOP " + block_size + " " + columns_list + " FROM " + table_name + ",DIM_PI WHERE " + table[
                'unix_timestamp_column'] + " >= " + last_state_value  + " AND (PING IS NOT NULL OR PING_DROPRATE=100) AND SK_PI=PK_PI ORDER BY DATA_DATE" 
        data = utils.execute_sql(cnxn, sql)

        for measurement in table['measurments']:
            measurement_name = measurement['measurement_name']
            default_values = {}
            column_types = {}
            tags_list = []
            fields_list = []
            for item in measurement['columns']:  
                if item['type'] == 'string':           
                    default_values[item['column_name']] = ''
                    column_types[item['column_name']] = "string"
                if item['type'] == 'integer':            
                    default_values[item['column_name']] = 0
                    column_types[item['column_name']] = "integer"
                if item['type'] == 'float':             
                   default_values[item['column_name']] = 0.0
                   column_types[item['column_name']] = "float"           
                if item['is_tag']:            
                   tags_list.append(item['column_name'])
                else:
                   fields_list.append(item['column_name'])
            

            influxdb_data = []
            
            if len(data) > 0:
                
                influxdb_client = InfluxDBClient(credentials_config['influxdb_host'], main_config['influxdb_port'], '', '',
                                                main_config['influxdb_database'])
                
                for index, item in data.iterrows():
                    timestamp = 0
                    fields = {}
                    tags = {}
                    max_auto_increment_value = 0
                    
                    for key in data.columns:
                        
                        if key == table['unix_timestamp_column']:
                            timestamp =item[key]
                            max_auto_increment_value=timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                        else:
                            
                            if key in tags_list:             
                                tags[key] = item[key]
                            elif key in fields_list:
                                if (item[key]) and not(math.isnan(item[key])):
                                    if column_types[key]=="float":
                                        item[key]=float(item[key])
                                    if column_types[key]=="integer":
                                        item[key]=int(item[key])
                                    fields[key] = item[key]
                                else:
                                    fields[key] = default_values[key]
                    
                    data_point = {
                        "measurement": measurement_name,
                        "tags"       : tags,
                        "time"       : timestamp,
                        "fields"     : fields
                    }
                    
                    influxdb_data.append(data_point)
                influxdb_client.write_points(influxdb_data)
                utils.file_write(state_file, 'w', "'" + str(max_auto_increment_value)+"'")
                
                print('Written ' + str(len(data)) + ' points for measurment ' +measurement_name + '.')
        
        #else:
            
          #  print('No data retrieved from MySQL for table ' + table_name + '.')
