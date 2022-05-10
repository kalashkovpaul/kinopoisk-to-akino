CREATE TABLE movies_genres (
    movie_id                            BIGINT REFERENCES movies (id),
    genre                               VARCHAR(50) REFERENCES genres (genre),
    CONSTRAINT movies_genres_id         PRIMARY KEY (movie_id, genre)
);

INSERT INTO
    movies_genres (movie_id, genre)
VALUES
    (1000001, 'anime'),
    (1000001, 'action'),
    (1000002, 'anime'),
    (1000002, 'drama'),
    (1000002, 'horror'),
    (1000002, 'thriller'),
    (1000003, 'comedy'),
    (1000004, 'action'),
    (1000004, 'thriller'),
    (1000005, 'anime'),
    (1000005, 'fantasy'),
    (1000005, 'horror');