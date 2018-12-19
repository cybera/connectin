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
- go to migration_scripts directory
> cd connectin/migration_scripts

- add passwords and ip addresses for mssql host and influxdbhost  
(use `config.json` if running from influxdb host ,`config_from_remote.json` - if running remotely)


 - delete measurements from influxdb on influxdb host(to clean everything and start copying data from scratch):
>influx  
>USE net_speed_md  
>DROP SERIES FROM /.*/;  
>exit  

- remove state file(to clean everything and start copying data from scratch):
>
>cd /root/migration_scripts  
>rm state_file_FCT_PI  

- start script(1nce):
>python3 mssql_to_influx.py  
- start script(multiple iterations):
>./load_database.sh  


To view data in influxdb:
>influx  
>USE net_speed_md;  
>SHOW MEASUREMENTS;  
>SHOW FIELD KEYS FROM CONNTRACK;  
>SHOW TAG KEYS FROM CONNTRACK;   
>SELECT * FROM CONNTRACK WHERE PI_MAC='02-01-05-c0-c1-14';  
>SELECT * FROM CONNTRACK WHERE SK_PI='2';  

