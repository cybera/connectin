# ConnectIn project

## Set up

This is the analysis portion of the project. It assumes that devices are set up, collecting data and saving it to MS SQL database.

### Credentials
Copy creds.env.example to creds.env:

> cp creds.env.example creds.env

Update creds.env with your MS SQL host ip address, database name, user and password:

>MSSQL_HOST=    
>MSSQL_DATABASE=   
>MSSQL_USER=   
>MSSQL_PASSWORD=   
 
Update INFLUXDB_ADMIN_PASSWORD, INFLUXDB_READ_USER_PASSWORD and DASH_PASSWORD from default values.

### Docker

Run **docker-compose up** to install all the components in Docker containers.   :
It will create 4 containers:

- **Influxdb**: timeseries database to store data locally, database and two uesrs will be created to write and read data.
- **Cronjobs**: container to run scripts every night to update influxdb with new data from MS SQL and upload MS SQL tables into csv files to "data" dir.
(First scripts will run when the conatiner is built and then every day at 21:30 and 20:30 UTC)
- **Jupyter**: container to run jupyter notebook service, it will be accessible at http://localhost:8888/ with token from docker-compose output
- **Dash**: container to run the dashboard, it will be available at http://localhost:8050/ and updated with data within 5 mins after docker-compose is finished

### Notebooks
Jupyter notebook service be accessible at http://localhost:8888/ with token from docker-compose output.

#### Interactive notebooks
Notebooks with interactive graphs organized by area of interest:

-  **Raw data, number of datapoints and monitoring intervals.ipynb** - shows raw data timeseries graphs by device for the entire time and for all the devices over last 6 months (speedtest and iperf test types)
-  **Aggregated data by year, month, day, hour.ipynb** - shows aggregated data (by month, year, hour, day of the week) graphs by device for the entire time and for all the devices over last 6 months (speedtest and iperf test types)
-  **Speedtest data by test server and service provider.ipynb** - shows datapoints by test server and service provider by device for the entire time  and for all the devices over last 6 months (speedtest test type)
-  **Statistics and map.ipynb** - shows statistice by device for last month, 6 months or the entire time  and  map and statistics for all the devices for last month, 6 months or the entire time (speedtest and iperf test types)


#### Original notebooks

First iteration of the project, exploration notebooks organized by stages with summary on each stage 


### Location data

To be able to show devices on the map (on the dashboard and in some of the notebooks) - coordinates of the devices should be saved as `data_analysis/coordinates2.csv`.  
Copy example file into  coordinates2.csv and add coordinates to csv directly or use notebook `data_analysis/Interactive_notebooks/Coordinates helper.ipynb` to add them interactively

> cp data_analysis/coordinates2.csv.example  data_analysis/coordinates2.csv

Coordinates used for the project are [here](https://docs.google.com/spreadsheets/d/19uYQM8fbDngLbV8RckWXQ0sQemg92XAid6gV_bHRQDw/edit#gid=975122863) (access restricted) 
 
### Timezones

Common timezone for all the devices is set in config.json 

If some of the devices have different timezone - it can be specified by device number in `data_analysis/timezone_by_device.csv`:  copy example file into `timezone_by_device.csv` and add timezones manually: 

>cp data_analysis/timezone_by_device.csv.example data_analysis/timezone_by_device.csv

## Dashboard 

Dashboard is accessible at http://localhost:8050/. It has basic authentication enabled. (Credentials are stored in creds.env file)

In order to use it - select metric (Upload/Download/Ping) and  time interval. When you press "Get  data"  - data will be selected from the database and stored in browser cache. Then plots on all the tabs will be populated with cached data.
In order to get another metric/time interval from database - press "Get data" button again.

**Note:** Dashboard works faster when running it locally as opposed to hosting it on the web. When hosted - cached data need to be transported over the web and it slows it down.

## InfluxDb structure
[InfluxDB](https://docs.influxdata.com/influxdb/v1.7/) is a timeseries database storing everything in measurements (tables) as tags(metagata)  and fields(values).

InfluxDB scheme used for the project is stored in config.json.
There are separate measurements for Ping, Upload and Download data. Both iperf and speedtest test results are stored in single measurement with different meatadata.

### Metadata 

Following metadata is stored for every measurement :
 - Provider - ISP for speedtest tests, "iperf" for iperf tests
 - IP - IP address of the device,
 - Test Server - name of the test server,
 - Province - province for speedtest tests,"iperf" for iperf tests
 - SK_PI - device number,
 - PI_MAC - device mac address


## Collectd data

Another set of tests is stored in MS SQL database - metrics coming from collectd. These metrics are collected every 5 seconds and have ping latency, ping droprate and lots of others. These metrics were not used in the analysis. If you want to use them - please replace config.json with config_full.json and recreate docker containers. It will import 3 additonal metrics from MS SQL - ping latency, ping droprate and conntrack.  They are not included in the dashboard - but some of the original jupyter notebooks analyze these metrics.

