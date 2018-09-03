# Project: Wrangle OpenStreetMap Data
## Map Area
Bogotá, Distrito Capital, Colombia.
* https://www.openstreetmap.org/relation/1387968

Downloaded from the OpenStreetMap website with the following boundaries: 

Direction | Value
--- | ---:
North | 4.8378
West | -74.2710
East | -74.0073
South | 4.5018

This is a map of the city where I live in since 2005. It’s quite a complex city with a unique street naming system. I’m also interested in seeing how well maintained is the map, given it’s in Latin America and probably doesn’t get much attention.
## Problems encountered in the map
I sampled the .osm file I downloaded and then looked at the tags using the code written during the OSM case-study. After poking around for a while in Spyder, I found issues with the data including, but not limited to, these:
* Abbreviated street names (“Av” instead of “Avenida”, “crr” instead of “Carrera”).
* Mistyped street names (“carera” instead of “Carrera”).
* Few and incorrect postal codes (longer than 6 digits, some don’t start with 11 and they should all start with it).
* Incomplete data. Tags like ‘postcode’, ‘district’ and ‘neighborhood’ are mostly empty. The ‘city’ tag sometimes says Bogota, sometimes the district.
### Abbreviated and mistyped street names
Street names in this city depend on the orientation (north to south, east to west, diagonals, etc.) and are quite simple, they all begin with the type. For example, ‘Carrera 7’ or ‘Avenida Calle 82’. To deal with the abbreviated and mistyped names I opted to use regular expressions, iterating over a mapping for each street name, as some of the abbreviations could appear twice. I created a function in the streets.py file that updates the names using the mappings made by exploring the names and looking for the most common errors:
```python
def update_name(name, mapping):

    for key, value in mapping.items():
        if key in name:
            name = re.sub(r'\b'+key+r'\b', value, name)
            break
        
    return name
```
This updated all the strings with the correct, capitalized names and managed to fix cases like ‘Av Cll 80’ to ‘Avenida Calle 80’, since the regular expression looks for complete words.
### Postal codes (or lack, thereof)
Postal codes are a recent development in Bogotá, so once I had the data on an SQL database I wanted to check exactly how many postal codes we have in total. Using the following query, I found out that we only have 272 tagged postal codes:
```sql
SELECT COUNT(DISTINCT(tags.id)) as count 
FROM (SELECT * FROM nodes_tags 
      UNION ALL 
      SELECT * FROM ways_tags) tags
WHERE tags.key='postcode';
```
Afterwards, I wanted to see how many of those were acceptable. In Bogotá, all postal codes must begin with 11, as that is the city code. The following 2 digits correspond to the district. Of these 272 postal codes, I found that a total of 52 do not begin with 11 using this query:
```sql
SELECT COUNT(DISTINCT(tags.id)) as count 
FROM (SELECT * FROM nodes_tags 
      UNION ALL 
      SELECT * FROM ways_tags) tags
WHERE tags.key='postcode' and tags.value NOT LIKE '11%';
```
Finally, of the codes that begin with 11, I wanted to find out if the lengths were correct. To do this, I used a query that counted the codes beginning with 11 and grouped them by their lengths. Correct codes are 6 digits:
```sql
SELECT LENGTH(tags.value) as 'N_digits', COUNT(*) as count 
FROM (SELECT * FROM nodes_tags 
      UNION ALL 
      SELECT * FROM ways_tags) tags
WHERE tags.key='postcode' and tags.value LIKE '11%'
GROUP BY LENGTH(tags.value)
ORDER BY count DESC;
```
N_digits | count
--- | --- 
6	| 178
9	| 19
7	| 14
5	| 5
8	| 4

This is quite the problem, as not only we have very few postal codes, but a considerable portion are plainly wrong. Further ahead I will elaborate on how I believe this problem can be solved.
### Districts in the wrong place
Looking through the data, I realized some information is misplaced. For instance, inside the city tag I found many other values that aren’t some variation of Bogota. Using this SQL query, I grouped them and returned the 10 most popular ones:
```sql
SELECT tags.value, COUNT(*) as count 
FROM (SELECT * FROM nodes_tags UNION ALL 
      SELECT * FROM ways_tags) tags
WHERE tags.key='city' and tags.value NOT LIKE 'bog%'
GROUP BY tags.value
ORDER BY count DESC
LIMIT 10;
```

value | count
--- | ---
Barrios Unidos | 1272
Chapinero | 217
Suba | 81
Funza | 56
Usaquén | 56
Antonio Nariño | 48
Engativá | 37
Kennedy | 28
Cota | 22
Puente Aranda | 22

 
All these 10 values are the names of the districts or neighborhoods those addresses belong to, which are in turn related to the postal codes they might not have. This information should be under different tags, such as ‘district’ or ‘neighborhood’, yet those are unused.
## Data overview and ideas
Here I compute a statistical overview of the data and show the queries used:
### File Sizes
 
#### Number of unique users
```sql
SELECT COUNT(DISTINCT(nodes_ways.uid))          
FROM (SELECT uid FROM nodes
UNION ALL SELECT uid FROM ways) nodes_ways;
```
2370
#### Number of nodes
 ```sql
 SELECT COUNT(*) FROM nodes;
 ```
572518
#### Number of ways
 ```sql
 SELECT COUNT(*) FROM ways;
 ```
138382
#### Top 10 contributors and percentage of contributions
 ```sql
 SELECT e.user, COUNT(*) as num, 
ROUND(100.0*COUNT(*)/(SELECT COUNT(*) FROM 
(SELECT user FROM nodes UNION ALL SELECT user FROM ways)),2)
as percent
FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
GROUP BY e.user
ORDER BY num DESC
LIMIT 10;
```
usercnum | percent (%)
--- | --- | ---
SirWeigel | 41437 | 5.83
Baconcrisp | 39834 | 5.6
Penelope86 | 29760 | 4.19
Oscarín Orbitus | 24902 | 3.5
Corban8 | 9648 | 2.76
carciofo | 19299 | 2.71
Federico Explorador | 18836 | 2.65
Vidal de la Blache | 8109 | 2.55
fredw | 17318 | 2.44
AngocA | 14888 | 2.09

 
Top user SirWeigel did 5.83% of the contributions to the map, so it clearly isn’t a one or two-person job.
## Other ideas about the dataset
### On fixing the postcodes and districts
As I mentioned before, postcodes and districts are related. In Bogotá, all postal codes must begin with 11, as that is the city code, and the following two digits correspond to the ‘localidad’ or district, and it goes from 00 to 20. I believe that it’s possible to devise a function that assigns the correct postal code by looking at the coordinates. If a location falls within a specific area or fence, then the correct postal code and district could be assigned.
In this data, locations with incorrect codes or without any at all, still have their coordinates, as shown in the following query. That is why I think it’s possible, but may not be easy:

 ```sql
 SELECT key, value, lat, lon
FROM (SELECT * FROM nodes_tags UNION ALL 
      SELECT * FROM ways_tags) tags
INNER JOIN nodes ON tags.id = nodes.id
WHERE value NOT LIKE '11%' AND (tags.key = 'postcode' OR tags.key = 'district')
LIMIT 15;
```
key | value | lat | lon
--- | --- | --- | ---
postcode | 250070 | 	4.5290678	 | -74.2365389
postcode | 250070	 | 4.526645	 | -74.231747
postcode | 250070	 | 4.5062768 | 	-74.2433541
postcode | Cra 4 # 66 - 66 | 	4.6461547 | 	-74.0562616
postcode | 57 | 	4.6175263 | 	-74.0758996
postcode | 3394949EXT. 2482	 | 4.6016861	 | -74.0644734
postcode | 3394949 | 	4.6016317 | 	-74.0661177
postcode | tel. 3394949 EXT. 2525 | 	4.601129 | 	-74.0662089
postcode | 3394949 EXT. 2860 | 	4.6024684	 | -74.0646774
postcode | 3394949 EXT. 2830 | 	4.6030566 | 	-74.0648356
postcode | 3394949 EXT. 2830 | 	4.6030914 | 	-74.0648732
postcode | 3394949 EXT.	 | 4.6027145 | 	-74.0644977
postcode | 3394949 EXT. 2900	 | 4.6026957 | 	-74.0651334
postcode | 3394949 EXT. 3095 | 	4.6027572	 | -74.0650985
postcode | 3394949 EXT. 2501 | 	4.6024819 | 	-74.0666138

However, I think there could be some issues with this approach. First, with the data we have right now, there is no way to verify if the coordinates are correct; it isn’t uncommon to find that points of interests are poorly placed. Second, where are we supposed to get the region data? To ensure the integrity of the map, geofences cannot be drawn by hand, which means this information should come from a reputable source and wouldn’t be cheap or easy to implement.

To carry out this job it is necessary to get the required information from the local government. Once that is done, it’s possible to program geofencing that can assign postal codes and district data based on location data. Finally, to validate the data, we’ll require help from the map users, as it might not be right to compare data with other mapping solutions, as to avoid data licensing issues.

 
## Additional queries
### Top 10 places of leisure
 ```sql
 SELECT value, COUNT(*) as num
FROM nodes_tags
WHERE key='leisure'
GROUP BY value
ORDER BY num DESC
LIMIT 10;
```
 value | num
 --- | ---
playground | 134
fitness_centre | 	87
park | 	86
sports_centre	 | 44
pitch | 	33
sport	 | 16
adult_gaming_centre | 	9
dance | 9
fitness_station | 	8
swimming_pool | 	8

### Top 10 amenities
 ```sql
 SELECT value, COUNT(*) as num
FROM nodes_tags
WHERE key='amenity'
GROUP BY value
ORDER BY num DESC
LIMIT 10;
```
value	 | num
--- | ---
restaurant | 	2730
pharmacy | 	1065
cafe | 	915
fast_food | 	814
bank | 	593
bar	 | 477
parking | 	444
school | 	440
dentist	 | 311
place_of_worship | 	262

 
## Conclusions
After inspecting the data using queries, it’s clear that Bogotá is incomplete and quite messy. However, just like I did with the street names, many of the shortcomings can be addressed programmatically. Postal codes are a recent development, so it’s not surprising that it’s not implemented yet in here. Using the GPS coordinates can be helpful in making the data more complete, since information like locations, neighborhoods and postal codes are all related to it.
