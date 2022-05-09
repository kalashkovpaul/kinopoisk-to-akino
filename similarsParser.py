from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.related_film_request import RelatedFilmRequest
from movieParser import getSingleMovie

api_client = KinopoiskApiClient("b4aadb6a-b881-46ce-bacd-a25b8b5697e8")

def writeSimilarsHeader(file):
    file.write("INSERT INTO\n")
    file.write("    movies_movies (movie_id, relation_id)\n")
    file.write("VALUES\n")


def getSimilars(moviesIDs, actorsIDs):
    oldMoviesIDs = dict(moviesIDs)
    print("[ LOG ]: Downloading similars...")
    similarsFile = open("similars_init.sql", "w")
    writeSimilarsHeader(similarsFile)
    for kinopoiskId in oldMoviesIDs:
        request = RelatedFilmRequest(kinopoiskId)
        try:
            response = api_client.films.send_related_film_request(request)
        except Exception as e:
            pass
        i = 0
        for item in response.items:
            if i >= 3:
                break
            if item.film_id in moviesIDs:
                similarsFile.write("    ({},    {}),\n".format(moviesIDs[kinopoiskId], moviesIDs[item.film_id]))
                i += 1
            else:
                print("[ LOG ]: Related not found, downloading: ", item.film_id)
                moviesIDs, actorsIDs = getSingleMovie(item.film_id, len(moviesIDs) + 1, moviesIDs, actorsIDs)
                if item.film_id in moviesIDs:
                    similarsFile.write("    ({},    {}),\n".format(moviesIDs[kinopoiskId], moviesIDs[item.film_id]))
                    i += 1

    similarsFile.close()
    print("[ LOG ]: Similars downloaded!")
    return moviesIDs, actorsIDs







