from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.staff.staff_request import StaffRequest

api_client = KinopoiskApiClient("b4aadb6a-b881-46ce-bacd-a25b8b5697e8")

def writeMovieToActorsHeader(file):
    file.write("INSERT INTO\n")
    file.write("    movies_actors (movie_id, actor_id)\n")
    file.write("VALUES\n")

def getMoviesToActors(moviesIDs, actorsIDs):
    print("[ LOG ]: Downloading movies-to-actors...")
    movieToActorsFile = open("movies_to_actors_init.sql", "w")
    writeMovieToActorsHeader(movieToActorsFile)
    
    i = 0
    for kinopoiskId in moviesIDs:
        request = StaffRequest(kinopoiskId)
        try:
            response = api_client.staff.send_staff_request(request)
        except Exception as e:
            pass
        j = 0
        for item in response.items:
            if item.profession_key.name == "ACTOR" \
                and item.staff_id in actorsIDs:
                if i == len(moviesIDs) - 1 and j == len(response.items) - 1:
                    movieToActorsFile.write("    ({}, {});\n".format(kinopoiskId, actorsIDs[item.staff_id]))
                else:
                    movieToActorsFile.write("    ({}, {}),\n".format(kinopoiskId, actorsIDs[item.staff_id]))
            j += 1
        i += 1
    movieToActorsFile.close()
    print("[ LOG ]: Movies to actors downloaded!")
    return moviesIDs, actorsIDs




