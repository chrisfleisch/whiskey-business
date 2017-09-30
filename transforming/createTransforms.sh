#Done. proof.price should be a float, after removing "$"
#Done. proof_raw.rating is an integer, except for the "Unrated"
#Done. proof_raw.rabble is a float, except for the "Unrated"
#redditwhiskynetworkreviewarchivereviewarchive_raw.reviewerrating is an int, except for the " "
#redditwhiskynetworkreviewarchivereviewarchive_raw.fullbottlepricepaid is an float, but needs to have "$" removed, and converted into USD 
#vapricelist_raw.age is an integer after removing "YR" and the null rows
#vapricelist_raw.price is a float after removing "$"
#vapricelist_raw.size is a float that needs to be converted to ounces

FLOATVARS='metacritic stdev Rabble FullBottlePricePaid Proof Cost oz altprice altage altbottleprice Price'
INTVARS='Number ReviewerRating Rating'
LOADINGDIR='../loading_and_modelling'
DATADIR="$LOADINGDIR/data"
HEADERSDIR="$LOADINGDIR/headers"
FILELIST=`ls -l $DATADIR/* | awk '{print $9}'`
TEMPLATE=transforms.sql
RAWSUFFIX='_raw'

#Make basic file
echo "" > $TEMPLATE
for f in $FILELIST; do
  FILENAME=`basename $f`
  TABLENAME=`echo "${FILENAME%%.*}"`
  HEADERS=`sed 's/"//g' $HEADERSDIR/$FILENAME | sed 's/,/, /g' | sed '1s/^\xEF\xBB\xBF//' `
  printf "DROP TABLE $TABLENAME;\n" >> $TEMPLATE
  printf "CREATE TABLE $TABLENAME AS SELECT " >> $TEMPLATE
  printf "$HEADERS FROM $TABLENAME$RAWSUFFIX;\n\n" >> $TEMPLATE
done

#Update fields with right types
for column in $INTVARS; do
  sed -i "s/ $column,/ cast\($column as int\) as $column,/Ig" $TEMPLATE
  sed -i "s/ $column FROM/ cast\($column as int\) as $column FROM/Ig" $TEMPLATE
done

for column in $FLOATVARS; do
  sed -i "s/ $column,/ cast\($column as float\) as $column,/Ig" $TEMPLATE
  sed -i "s/ $column FROM/ cast\($column as float\) as $column FROM/Ig" $TEMPLATE
done

# Add reddit_bottles
printf "\nDROP TABLE reddit_bottles;\n" >> $TEMPLATE
printf "CREATE TABLE reddit_bottles AS SELECT altbrand, sum(Rating)/count(Rating) as avg_rating, count(Rating) as num_reviews, sum(altbottleprice)/count(altbottleprice) as altbottleprice FROM redditarchive WHERE rating > 0 GROUP BY altbrand;\n\n"  >> $TEMPLATE

