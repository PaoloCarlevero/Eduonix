-- This file has been create to be used in the sqlite command prompt

-- Dropping table and view in case of multiple use in the same session
DROP TABLE IF EXIST movie_metadata;
DROP TABLE IF EXIST movie_metadata_temp;
DROP TABLE IF EXIST movie;
DROP TABLE IF EXIST income_and_spend;
DROP TABLE IF EXIST reting;
DROP VIEW IF EXIST movie_and_rating;


-- 1. Insert the data that is provided in the spread for each of the tables.

-- Importing the data from the csv file
.mode csv
.import C:/sqlite/movie_metadata.csv movie_metadata

-- Checking how the imported table is strucured
.schema

-- To create a primary key we start by adding a new empty column called movie_ID
ALTER TABLE movie_metadata ADD movie_ID INTEGER;
ALTER TABLE movie_metadata RENAME TO movie_metadata_temp;

-- Creating a new schema with movie_ID as primary key
CREATE TABLE "movie_metadata"(
   "color" TEXT,
   "director_name" TEXT,
   "num_critic_for_reviews" TEXT,
   "duration" TEXT,
   "director_facebook_likes" TEXT,
   "actor_3_facebook_likes" TEXT,
   "actor_2_name" TEXT,
   "actor_1_facebook_likes" TEXT,
   "gross" TEXT,
   "genres" TEXT,
   "actor_1_name" TEXT,
   "movie_title" TEXT,
   "num_voted_users" TEXT,
   "cast_total_facebook_likes" TEXT,
   "actor_3_name" TEXT,
   "facenumber_in_poster" TEXT,
   "plot_keywords" TEXT,
   "movie_imdb_link" TEXT,
   "num_user_for_reviews" TEXT,
   "language" TEXT,
   "country" TEXT,
   "content_rating" TEXT,
   "budget" TEXT,
   "title_year" TEXT,
   "actor_2_facebook_likes" TEXT,
   "imdb_score" TEXT,
   "aspect_ratio" TEXT,
   "movie_facebook_likes" TEXT,
   "movie_ID" INTEGER,
   PRIMARY KEY("Movie_ID")
);

-- By importing the data on the new table SQLite will automaticaly insert value for movie-ID
INSERT INTO movie_metadata SELECT DISTINCT * FROM movie_metadata_temp;

-- Drop the original table that is no longer needed
DROP TABLE movie_metadata_temp;

-- 2. Create the Primary key on Movie ID in the movie table and join the income and rating table with foreign key

-- Creating the tables in wich splitting the database
CREATE TABLE movie (
   "movie_ID" INTEGER,
   "movie_title" TEXT,
   "genres" TEXT,
   "plot_keywords" TEXT,
   "language" TEXT,
   "country" TEXT,
   "duration" INTEGER,
   "title_year" INTEGER,
   "content_rating" TEXT,
   "director_name" TEXT,
   "actor_1_name" TEXT,
   "actor_2_name" TEXT,
   "actor_3_name" TEXT,
   "facenumber_in_poster" INTEGER,
   "color" TEXT,
   "aspect_ratio" REAL,
   "movie_imdb_link" TEXT,
   PRIMARY KEY (movie_ID),
   FOREIGN KEY (movie_ID) REFERENCES income_and_spend (movie_ID),
   FOREIGN KEY (movie_ID) REFERENCES rating (movie_ID)
);

CREATE TABLE income_and_spend (
   "movie_ID" INTEGER,
   "gross" INTEGER,
   "budget" INTEGER,
    PRIMARY KEY("movie_ID")
);

CREATE TABLE rating (
   "movie_ID" INTEGER,
   "imdb_score" REAL,
   "num_voted_users" INTEGER,
   "num_user_for_reviews" INTEGER,
   "num_critic_for_reviews" INTEGER,
   "movie_facebook_likes" INTEGER,
   "director_facebook_likes" INTEGER,
   "actor_1_facebook_likes" INTEGER,
   "actor_2_facebook_likes" INTEGER,
   "actor_3_facebook_likes" INTEGER,
   "cast_total_facebook_likes" INTEGER,
   PRIMARY KEY("movie_ID")
);

-- Inserting the data in the new table
INSERT INTO
   movie (movie_ID, movie_title, genres, plot_keywords, language, country, duration, title_year, content_rating, director_name, actor_1_name, actor_2_name, actor_3_name, facenumber_in_poster, color, aspect_ratio, movie_imdb_link)
SELECT
   movie_ID,
   movie_title,
   genres,
   plot_keywords,
   language,
   country,
   duration,
   title_year,
   content_rating,
   director_name,
   actor_1_name,
   actor_2_name,
   actor_3_name,
   facenumber_in_poster,
   color,
   aspect_ratio,
   movie_imdb_link
FROM
   movie_metadata
;

INSERT INTO
   income_and_spend
SELECT
   movie_id,
   gross,
   budget
FROM
   movie_metadata
;

INSERT INTO
   rating
SELECT
   movie_id,
   imdb_score,
   num_voted_users,
   num_user_for_reviews,
   num_critic_for_reviews,
   movie_facebook_likes,
   cast_total_facebook_likes,
   director_facebook_likes,
   actor_1_facebook_likes,
   actor_2_facebook_likes,
   actor_3_facebook_likes
FROM
   movie_metadata
;

-- 3. Select the movies for their actor names, director, and gross revenue in descending order
SELECT
   m.movie_title AS movie_title,
   m.actor_1_name AS actor_1_name,
   m.actor_2_name AS actor_2_name,
   m.actor_3_name AS actor_3_name,
   m.director_name AS director_name,
   i.gross AS gross
FROM
   movie m 
      LEFT JOIN income_and_spend i ON m.movie_ID = i.movie_ID
ORDER BY
   gross DESC
;

-- 4. Select the top 3 highest-grossing movies by name
SELECT
   m.movie_title AS movie_title,
   i.gross AS gross
FROM
   movie m
      LEFT JOIN income_and_spend i ON m.movie_ID = i.movie_ID
WHERE
   gross IS NOT ""
ORDER BY
   gross DESC
LIMIT 3
;


-- 5. Which movies have the IMBD scoring between 6 and 7.
SELECT
   m.movie_title AS movie_title,
   r.imdb_score AS imdb_score
FROM
   movie m
      LEFT JOIN rating r ON m.movie_ID = r.movie_ID
WHERE
   imdb_score BETWEEN 6 AND 7
;

-- 6. Update the Facebook likes to 7500 for movie id 5
UPDATE
   rating
SET
   movie_facebook_likes = 7500
WHERE
   movie_ID = 5
;

-- 7. Start the transaction and update the Facebook likes to 4700 for movie id 7 and then rollback the changes
BEGIN TRANSACTION;
UPDATE
   rating
SET
   movie_facebook_likes = 4700
WHERE
   movie_ID = 7
;
SELECT * FROM rating WHERE movie_ID = 7;
ROLLBACK;
SELECT * FROM rating WHERE movie_ID = 7;

-- 8. Create a view to combining the rating data with movies data
CREATE VIEW movie_and_rating AS
   SELECT
      m.*,
      r.*
   FROM
      movie m
         LEFT JOIN rating r ON m.movie_ID = r.movie_ID
;

-- 9. What is the average budget and average income of all movies together
SELECT
   avg(gross) AS avg_gross,
   avg(budget) AS avg_budget
FROM
   income_and_spend
;

-- 10. What are those movies which have IMDB ratings more than 7 and Facebook likes less than 20000
SELECT
   m.movie_title AS movie_title,
   r.imdb_score AS imdb_score,
   r.movie_facebook_likes AS movie_facebbok_likes
FROM
   movie m
      LEFT JOIN rating r ON m.movie_ID = r.movie_ID
WHERE
   r.imdb_score > 7 AND r.movie_facebook_likes < 2000
;
