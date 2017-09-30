
DROP TABLE whiskey_business_stage;

CREATE TABLE whiskey_business_stage AS 
SELECT  
V.brand as `Name`,
V.altprice as `Price`, 
V.oz as `# of oz`, 
V.description as `Type`, 
sum(R.avg_rating)/count(avg_rating) as `Reddit score`, 
sum(M.MetaCritic)/count(M.MetaCritic) as `Critic's score`, 
sum(P.Rating)/count(P.Rating) as `Awards score`, 
sum(V.altprice)/sum(V.oz) as `VA Price/oz`,
Case 
when V.oz in (25.360113) AND sum(P.Price) > 0 then ((sum(R.altbottleprice) + sum(P.price))/2)/sum(V.oz)
when V.oz in (25.360113) AND sum(P.Price) IS NULL then sum(R.altbottleprice)/sum(V.oz) 
end as `Market Price/oz`
From vaprices V 
LEFT JOIN reddit_bottles  R on V.altbrand=R.altbrand 
LEFT JOIN metacritic M on V.altbrand=M.altbrand 
LEFT JOIN proof P on V.altbrand=P.altbrand
GROUP BY V.brand, V.altprice, V.oz, V.description;

DROP TABLE whiskey_business;

CREATE TABLE whiskey_business AS
SELECT   Name, Price, `# of oz`, `Type`,`Reddit score`, `Critic's score`,`Awards score`,`VA Price/oz`,`Market Price/oz`,
Case
WHEN `Market Price/oz` IS NULL THEN 'No'
ELSE 'Yes'
END `Price Benchmark?`
FROM whiskey_business_stage;


