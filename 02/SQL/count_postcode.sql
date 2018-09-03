SELECT COUNT(DISTINCT(tags.id)) as count 
FROM (SELECT * FROM nodes_tags 
	  UNION ALL 
      SELECT * FROM ways_tags) tags
WHERE tags.key='postcode' and tags.value NOT LIKE '11%';