SELECT key, value, lat, lon
FROM (SELECT * FROM nodes_tags UNION ALL 
      SELECT * FROM ways_tags) tags
INNER JOIN nodes ON tags.id = nodes.id
WHERE value NOT LIKE '11%' AND (tags.key = 'postcode' OR tags.key = 'district')
LIMIT 15;