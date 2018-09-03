SELECT e.user, COUNT(*) as num, 
ROUND(100.0*COUNT(*)/(SELECT COUNT(*) FROM 
(SELECT user FROM nodes UNION ALL SELECT user FROM ways)),2)
as percent
FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
GROUP BY e.user
ORDER BY num DESC
LIMIT 10;