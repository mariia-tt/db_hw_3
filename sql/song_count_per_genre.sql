SELECT Genre.name AS Genre_name, SUM(Album.song_count) as Song_count
FROM Album_Genre
JOIN Genre ON Album_Genre.genre_identifier = Genre.genre_identifier
JOIN Album ON Album_Genre.album_identifier = Album.album_identifier
GROUP BY Genre.name
ORDER BY Song_count DESC
