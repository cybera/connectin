## ConnectIn project
### Set up
To connect to MS SQL database we are goint to use odbc driver.
ODBC is a specification for a database API.(https://docs.microsoft.com/en-us/sql/odbc/reference/what-is-odbc?view=sql-server-2017)

To install it on Ubuntu run:
* `sudo apt-get install unixodbc unixodbc-dev libodbc1 msodbcsql17 odbcinst odbcinst1debian2`
* Make sure driver file is created : `/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.2.so.0.1` 

To install it on MAC run(from here: https://community.exploratory.io/t/connecting-to-ms-sql-server-through-odbc-from-mac/339):
* Update homebrew to the latest first: `brew update`
* install libiodbc with homebrew:` brew install libiodbc`
* Install freetds with homebrew`brew: install freetds --with-odbc-wide`
* Make sure that freetds ODBC driver library file is successfully created:  `/usr/local/lib/libtdsodbc.so`

Install pyoddbc python package : `pip install pyodbc`

### Json files
  
Configuration for MS SQL/InfluxDB migration is stored in config.json
Configuration is based on https://docs.google.com/document/d/1BiW-_E4e5ICkvGwXt6fkfWzhn14OmG266gijRLK4AzE/edit
  
Another configuration file needs to be created to store passwords and host IP addresses - **credentials.json**:
>{   
>    "mssql_host"       : "Ip address of MS SQL host(1Password)",   
>    "mssql_password"   : "Password for MS SQL database(1Password)",   
>    "influxdb_host"    : "localhost if running locally on connectin VM or IP address or the connectin VM",     
>    "influxdb_password": "Password for influxdb database(1Password)"
>}  
  
To run migration scripts from Mac
 - driver needs to be installed: https://community.exploratory.io/t/connecting-to-ms-sql-server-through-odbc-from-mac/339  
 - path to the driver needs to be changed in config.json: 
>"driver"           : "/usr/local/lib/libtdsodbc.so",


### Migration scripts
`mssql_to_influx.py`   
This script  takes data from 3 msssql tables: FCT_PI, DIM_PI and FCT_SPEEDTEST  and inserts it into influx into 5 measurements: CONNTRACK, PING, SPEEDTEST_PING, SPEEDTEST_UPLOAD, SPEEDTEST_DOWNLOAD.  
Data is taken in blocks (currently 10000 rows, it can be changed in config.json:block_size). 
It writes down the latest timestamp into state files(state_file_FCT_PI and state_file_FCT_SPEEDTEST) and on the next run starts with this timestamp.

**To start migration from latest recorded timestamp**:
   
- start script(for one iteration):
>python3 mssql_to_influx.py  
- start script(for multiple iterations):
>./load_database.sh  5  (to copy 5 blocks of data(50000 points), with no parametres it will run 50 iterations)

**To start migration from scratch**:
   
- delete measurements from influxdb:
>influx  
>USE net_speed_md  
>DROP SERIES FROM /.*/;  
>exit  
  
- remove state files:  
>cd /root/connectin/data  
>rm state_file_FCT_PI  
>rm state_file_FCT_SPEEDTEST  
    
- start script(for one iteration):
>python3 mssql_to_influx.py  
- start script(for multiple iterations):
>./load_database.sh  5  (to copy 5 blocks of data(50000 points), with no parametres it will run 50 iterations)

### Backup scripts
`backup_to_csv.py`

This script takes input configuration for mssql/influx from json file: config.json similar to migration script. It connects to the MSSQL database and backups all the data from FCT_PI and FCT_SPEEDTEST tables to corresponding csv files.
It saves lates timestamps into state_file_csv_FCT_PI and state_file_csv_FCT_SPEEDTEST files.

`get_all_data.py`  
  
Run this script to get a backup of all the data from rest of the tables into corresponsding csv files. This can be run on need basis.

### Crontab 
Two shell scripts are added to crontab to run db backup and migration at 7:30 and 8:30 pm:   
>30 3 * * * /bin/bash /root/connectin/migration_backup/load_database.sh > /dev/null 2>&1  
>30 2 * * * /bin/bash /root/connectin/migration_backup/db_backup.sh > /dev/null 2>&1  

`db_backup.sh`  
Runs backup_to_csv.py python script to back up FCT_PI and FCT_SPEEDTEST tables into csv files.

`load_database.sh`   
Runs mssql_to_influx.py to to back up FCT_PI and FCT_SPEEDTEST tables into influxdb.

### Influxdb
Resources:
- https://influxdb-python.readthedocs.io/en/latest/examples.html
 - https://www.influxdata.com/blog/getting-started-python-influxdb/
 - https://influxdb-python.readthedocs.io/en/latest/resultset.html
 - https://influxdb-python.readthedocs.io/en/latest/api-documentation.html
 - https://docs.influxdata.com/influxdb/v1.0//query_language/functions
   
To view data in influxdb:
>influx  
>USE net_speed_md;  
>SHOW MEASUREMENTS;  
>SHOW FIELD KEYS FROM CONNTRACK;  
>SHOW TAG KEYS FROM CONNTRACK;   
>SELECT * FROM CONNTRACK WHERE PI_MAC='02-01-05-c0-c1-14';  
>SELECT * FROM CONNTRACK WHERE SK_PI='2';  
