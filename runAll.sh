#!/bin/bash

# pull new data from web
python data_get/download.py

# transform the data before storing
python data_get/transform.py


cd loading_and_modelling
./load_data_lake.sh
cd ../transforming
./allTransforms.sh

cd ..
# export data from hive
hive -e 'set hive.cli.print.header=true;select * from whiskey_business;' | sed 's/[\t]/,/g' | sed 's/whiskey_business\.//g' > export_data/data/whiskey_business.csv
# export data from csv to google sheets
python export_data/spreadsheet.py
