#Remove spaces from filenames
for f in data/*\ *; do mv "$f" "${f// /_}" ; done

#I don't like numbers in filenames either.
for f in `find data/ -regex 'data\/.*[0-9]+.*'` ; do mv $f "${f//[0-9]*.csv/}.csv" ; done

#Remove annoying _-_ from filename. There's nothing wrong with it, I just think it's ugly.
for f in data/*_-_*; do mv "$f" "${f//_-_/_}" ; done

#Remove annoying - from filename. This actually threw an error during hive load time.
for f in data/*-*; do mv "$f" "${f//-/}" ; done

#I've decided underscores are annoying and unnecessary.
for f in data/*_*; do mv "$f" "${f//_/}" ; done

#The VA price list stinks and includes an additional line at the top of their CSV... Cmon guys. What is this amateur hour?
#VAFILE=data/VAPriceList.csv
#tail -n +2  $VAFILE > $VAFILE"_" ; mv $VAFILE"_" $VAFILE

#Strip out non-ascii characters which for some reason exist in some of these files.
sed -i 's/[\d128-\d255]//g' data/*.csv
sed -i '1s/^\xEF\xBB\xBF//' data/*.csv

#Replace "Unrated" entries with -1 so they can fit as integers.
sed -i "s/,Unrated,/,-1,/g" data/*.csv

#Replace dollar amounts with strickly floats in proof66.csv
sed -r 's/,\$([0-9\.]+)/,\1/g' -i data/proof*.csv

#Generate headers into separate files
mkdir headers
for f in data/*.csv; do NEWFILE=headers/`basename ${f%.*}`".csv"; head -n 1 $f | sed 's/ //g' | sed 's/\///g' | sed 's/-//g' | sed 's/_//g' | sed 's///' > $NEWFILE;  done

#Get those nasty quotes out of the headers
sed -i "s/'//g" headers/*

#Get those potentially treacherous hashbrowns out of the headers
sed -i "s/#/Number/g" headers/*
#sed -i "s/Cluster/Clust/g" headers/*
#sed -i "s/Type/Class/g" headers/*
#sed -i 's/"//g' headers/*

#Strip headers from files
for f in data/*.csv; do tail -n +2 $f > $f"_" ; mv $f"_" $f ; done
