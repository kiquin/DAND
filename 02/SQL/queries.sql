SELECT LENGTH(tags.value) as 'N_digits', COUNT(*) as count 
FROM (SELECT * FROM nodes_tags UNION ALL 
      SELECT * FROM ways_tags) tags
WHERE tags.key='postcode' and tags.value LIKE '11%'
GROUP BY LENGTH(tags.value)
ORDER BY count DESC;