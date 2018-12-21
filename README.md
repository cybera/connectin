## ConnectIn project

### Migration scripts
`mssql_to_influx.py` 
This script takes input configuration for mssql/influx from json file: config.json.
Configuration is based on https://docs.google.com/document/d/1BiW-_E4e5ICkvGwXt6fkfWzhn14OmG266gijRLK4AzE/edit
It currently takes data from two  msssql tables: FCT_PI and DIM_PI and inserts it into influx into 4 measurements: CONNTRACK, ETH1, ETH2, ETH3, PING. (Table FCT_SPEEDTEST is empty, have not included it yet). 
Data is taken in blocks (currently 10000 rows, it can be changed in config.json:block_size). 
It writes down the lates timestamp it used into state file (state_file_FCT_PI) and on the next run starts with this timestamp.

(Script can be run from macOS(laptop) as well, use config config_from_remote.json)

To start migrating databases:
- clone git repo
- go to scripts directory
> cd connectin/scripts

- add passwords and ip addresses for mssql host and influxdbhost  
(use `config.json` if running from influxdb host ,`config_from_remote.json` - if running remotely)


 - delete measurements from influxdb on influxdb host(to clean everything and start copying data from scratch):
>influx  
>USE net_speed_md  
>DROP SERIES FROM /.*/;  
>exit  

- remove state file(to clean everything and start copying data from scratch):
>
>cd /root/connectin/data
>rm state_file_FCT_PI  

- start script(for one iteration):
>python3 mssql_to_influx.py  
- start script(for multiple iterations):
>./load_database.sh  5  (to copy 5 blocks of data(50000 points), with no parametrest will run 1000 iterations)


To view data in influxdb:
>influx  
>USE net_speed_md;  
>SHOW MEASUREMENTS;  
>SHOW FIELD KEYS FROM CONNTRACK;  
>SHOW TAG KEYS FROM CONNTRACK;   
>SELECT * FROM CONNTRACK WHERE PI_MAC='02-01-05-c0-c1-14';  
>SELECT * FROM CONNTRACK WHERE SK_PI='2';  

### Backup scripts

`backup_to_csv.py`

This script takes input configuration for mssql/influx from json file: config.json similar to migration script. It connects to the MSSQL database and backups all the data from FCT_PI and FCT_SPEEDTEST tables to corresponding csv files.

`db_backup.sh`
This has been added as a cron task to run every midnight to backup all the data from the MSSQL server.


`get_all_data.py`
Run this script to get a backup of all the data from rest of the tables into corresponsding csv files. This can be run on need basis.