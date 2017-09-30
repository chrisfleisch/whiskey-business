#!/bin/bash
./clean.sh
./0_downloadData.sh
./1_mangleFiles.sh
./2_hdfs.sh
hive -f hive_base_ddl.sql

