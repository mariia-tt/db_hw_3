SELECT
name AS Name,
ROUND((duration * listen_count) / 3600) as Total_Duration  
From Composition
ORDER BY Total_duration DESC