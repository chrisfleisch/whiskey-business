
DROP TABLE metacritic;
CREATE TABLE metacritic AS SELECT whisky, cast(metacritic as float) as metacritic, cast(stdev as float) as stdev, count, cast(Cost as float) as Cost, class, supercluster, cluster, country, type, altbrand FROM metacritic_raw;

DROP TABLE proof;
CREATE TABLE proof AS SELECT name, cast(Rating as int) as Rating, cast(Rabble as float) as Rabble, cast(Price as float) as Price, altbrand FROM proof_raw;

DROP TABLE redditarchive;
CREATE TABLE redditarchive AS SELECT timestamp, whiskyname, reviewerusername, link, cast(Rating as int) as Rating, style, bottleprice, reviewdate, altbrand, cast(altbottleprice as float) as altbottleprice FROM redditarchive_raw;

DROP TABLE vaprices;
CREATE TABLE vaprices AS SELECT description, code, brand, size, age, cast(Proof as float) as Proof, cast(Price as float) as Price, altbrand, cast(oz as float) as oz, cast(altprice as float) as altprice, cast(altage as float) as altage FROM vaprices_raw;


DROP TABLE reddit_bottles;
CREATE TABLE reddit_bottles AS SELECT altbrand, sum(Rating)/count(Rating) as avg_rating, count(Rating) as num_reviews, sum(altbottleprice)/count(altbottleprice) as altbottleprice FROM redditarchive WHERE rating > 0 GROUP BY altbrand;

