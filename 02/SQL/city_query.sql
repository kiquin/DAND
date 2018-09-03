SELECT tags.value, COUNT(*) as count 
FROM (SELECT * FROM nodes_tags UNION ALL 
      SELECT * FROM ways_tags) tags
WHERE tags.key='city' and tags.value NOT LIKE 'bog%'
GROUP BY tags.value
ORDER BY count DESC
LIMIT 10;