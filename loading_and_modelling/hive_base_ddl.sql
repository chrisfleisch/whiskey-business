
DROP TABLE metacritic_raw;
CREATE EXTERNAL TABLE metacritic_raw (whisky String,metacritic String,stdev String,count String,cost String,class String,supercluster String,cluster String,country String,type String,altbrand String)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES(
"separatorChar"=",",
"quoteChar"="\"",
"escapeChar"='\\'
)
STORED AS TEXTFILE
LOCATION '/user/w205/whiskey/metacritic_raw';

DROP TABLE proof_raw;
CREATE EXTERNAL TABLE proof_raw (name String,rating String,rabble String,price String,altbrand String)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES(
"separatorChar"=",",
"quoteChar"="\"",
"escapeChar"='\\'
)
STORED AS TEXTFILE
LOCATION '/user/w205/whiskey/proof_raw';

DROP TABLE redditarchive_raw;
CREATE EXTERNAL TABLE redditarchive_raw (timestamp String,whiskyname String,reviewerusername String,link String,rating String,style String,bottleprice String,reviewdate String,altbrand String,altbottleprice String)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES(
"separatorChar"=",",
"quoteChar"="\"",
"escapeChar"='\\'
)
STORED AS TEXTFILE
LOCATION '/user/w205/whiskey/redditarchive_raw';

DROP TABLE vaprices_raw;
CREATE EXTERNAL TABLE vaprices_raw (description String,code String,brand String,size String,age String,proof String,price String,altbrand String,oz String,altprice String,altage String)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES(
"separatorChar"=",",
"quoteChar"="\"",
"escapeChar"='\\'
)
STORED AS TEXTFILE
LOCATION '/user/w205/whiskey/vaprices_raw';

