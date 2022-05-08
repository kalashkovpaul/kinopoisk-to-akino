from actorsParser import getActors
from movieParser import getMovies
from moviesToActorsParser import getMoviesToActors

moviesIDs, actorsIDs = getMovies()
actorsIDs = getActors(actorsIDs)
getMoviesToActors(moviesIDs, actorsIDs)