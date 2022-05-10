from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.film_request import FilmRequest
from kinopoisk_unofficial.request.films.filters_request import FiltersRequest

api_client = KinopoiskApiClient("b4aadb6a-b881-46ce-bacd-a25b8b5697e8")

def writeGenresHeader(file):
    file.write("INSERT INTO\n")
    file.write("    movies_genres (movie_id, genre)\n")
    file.write("VALUES\n")

def getGenresTable():
    genresTable = {}
    genresTable['боевик'] = "'action'"
    genresTable['приключения'] = "'adventure'"
    genresTable['aниме'] = "'anime'"
    genresTable['биография'] = "'biography'"
    genresTable['мультфильм'] = "'cartoons'"
    genresTable['комедия'] = "'comedy'"
    genresTable['криминал'] = "'criminal'"
    genresTable['детектив'] = "'detective'"
    genresTable['документальный'] = "'documental'"
    genresTable['драма'] = "'drama'"
    genresTable['семейный'] = "'family'"
    genresTable['фэнтези'] = "'fantasy'"
    genresTable['история'] = "'historical'"
    genresTable['ужасы'] = "'horror'"
    genresTable['мелодрама'] = "'melodrama'"
    genresTable['мюзикл'] = "'musical'"
    genresTable['короткометражка'] = "'short'"
    genresTable['спорт'] = "'sport'"
    genresTable['триллер'] = "'thriller'"
    genresTable['вестерн'] = "'western'"
    return genresTable

def getGenres(moviesIDs):
    print("[ LOG ]: Downloading genres...")
    genresFile = open("genres_init.sql", "w")
    writeGenresHeader(genresFile)
    genresTable = getGenresTable()
    for kinopoiskId in moviesIDs:
        request = FilmRequest(kinopoiskId)
        try:
            response = api_client.films.send_film_request(request)
        except Exception as e:
            pass
        for item in response.film.genres:
            if item.genre in genresTable:
                genresFile.write("    ({},    {}),\n".format(moviesIDs[kinopoiskId], genresTable[item.genre]))
    genresFile.close()
    print("[ LOG ]: Genres downloaded!")







