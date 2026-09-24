SELECT movies.title, ratings.rating
FROM ratings INNER JOIN movies
ON movie_id = id
WHERE movies.year = 2010
ORDER BY rating DESC, title;