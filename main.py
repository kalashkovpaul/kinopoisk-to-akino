from actorsParser import getActors
from genresParser import getGenres
from movieParser import getMovies
from moviesToActorsParser import getMoviesToActors
from similarsParser import getSimilars

moviesIDs, actorsIDs = getMovies()
moviesIDs, actorsIDs = getSimilars(moviesIDs, actorsIDs)
actorsIDs = getActors(actorsIDs)
getMoviesToActors(moviesIDs, actorsIDs)
getGenres(moviesIDs)