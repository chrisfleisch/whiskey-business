#File lists can be given as an explicit list, or simply everything in the data directory. For this case, I think it's safe to use everything.
#FILELIST='data/Timely_and_Effective_Care_Hospital.csv data/HCAHPS_Hospital.csv data/Readmissions_and_Deaths_Hospital.csv data/Hospital_General_Information.csv data/Measure_Dates.csv'
HDFSDIR=/user/w205/whiskey
TEMPLATE=hive_base_ddl.sql
hdfs dfs -mkdir $HDFSDIR
FILELIST=`ls -l data/* | awk '{print $9}'`
echo "" > $TEMPLATE
for f in $FILELIST ; do
  FILENAME=`basename $f`
  DIRNAME=`echo "${FILENAME%%.*}_raw"`
  echo generating table $DIRNAME from file $FILENAME
  hdfs dfs -mkdir $HDFSDIR/$DIRNAME
  hdfs dfs -put $f $HDFSDIR/$DIRNAME/$FILENAME"_raw"
  printf "DROP TABLE $DIRNAME;\n" >> $TEMPLATE
  printf "CREATE EXTERNAL TABLE $DIRNAME (" >> $TEMPLATE
  HEADERS=`sed 's/,/ String,/g' headers/$FILENAME | sed 's/"//g' | sed '1s/^\xEF\xBB\xBF//' `
  printf "$HEADERS String)\nROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'\nWITH SERDEPROPERTIES(\n\"separatorChar\"=\",\",\n\"quoteChar\"=\"\\\\\"\",\n\"escapeChar\"=\'\\\\\\\\\'\n)\nSTORED AS TEXTFILE\nLOCATION \'$HDFSDIR/$DIRNAME\';\n\n" >> $TEMPLATE
done

