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
 
Update INFLUXDB_ADMIN_PASSWORD and INFLUXDB_READ_USER_PASSWORD from default values.

### Docker

Run **docker-compose up** to install all the components in Docker containers.   
It will create 4 containers:

- **Influxdb**: timeseries database to store data locally, database and two uesrs will be created to write and read data.
- **Cronjobs**: container to run scripts every night to update influxdb with new data from MS SQL and upload MS SQL tables into csv files to "data" dir.
(First scripts will run when the conatiner is built and then every day at 21:30 and 20:30 UTC)
- **Jupyter**: container to run jupyter notebook service, it will be accessible at http://localhost:8888/ with token from docker-compose output
- **Dash**: container to run the dashboard, it will be available at http://localhost:8050/ and updated with data within 5 mins after docker-compose is finished

