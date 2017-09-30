HDFSDIR=/user/w205/whiskey

rm -rf data/
rm -rf headers/
hdfs dfs -rm -r -f $HDFSDIR
