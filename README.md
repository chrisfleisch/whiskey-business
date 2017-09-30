# Whiskey Business

[Data Studio Output](https://datastudio.google.com/reporting/0B0t--sHr40JpM0swak1STFBCd0k/page/gMTD)

![Data Studio image](https://github.com/chrisfleisch/whiskey-business/screenshots/whiskey_business_datastudio.png "Data Studio")

## Setup Instructions

Please run everything as the w205 user unless otherwise stated.

The user should already have hadoop and hive installed and running.

More specifically, if you're booting a UCB instance, you can use the following commands:

As root (update your dev to reflect where your EBS volume is):
```
mount /dev/xvdf /data
/data/start_postgres.sh
./start-hadoop.sh
su - w205
```

As w205 (Optional):
```
/data/start_metastore.sh
```


## Env setup

If you don't have anaconda installed already, please install it from:

https://www.continuum.io/downloads#linux

Setup conda env called "w205-project":

`conda env create -f environment.yml`

Activate env:

`source activate w205-project`

Update the env when activated if environment.yml is updated:

`conda env update -f environment.yml`

To remove the project:

`conda remove --name w205-project --all`

## Run all

Activate environment:

`source activate w205-project`

Add google docs credentials to:
`export_data/client_secret.json`

Run all scripts:
`./runAll.sh`


## Manual Data setup commands

Download data to data source:

`python data_get/download.py`

Transform data in data source:

`python data_get/transform.py`

Put data into HDFS:

`cd loading_and_modelling`

`./load_data_lake.sh`

Transform data in hive:

`cd ../transforming`

`./allTransforms.sh`

Pull final table down as CSV with headers:

`hive -e 'set hive.cli.print.header=true;select * from whiskey_business;' | sed 's/[\t]/,/g' | sed 's/whiskey_business\.//g' > export_data/data/whiskey_business.csv`

Export data from csv to google sheets:

`python export_data/spreadsheet.py`
