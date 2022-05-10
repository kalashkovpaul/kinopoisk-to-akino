from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.box_office_request import BoxOfficeRequest
from kinopoisk_unofficial.request.films.film_request import FilmRequest
import requests
import os
import glob
from pathlib import Path
from PIL import Image

from kinopoisk_unofficial.request.films.film_video_request import FilmVideoRequest
from kinopoisk_unofficial.request.staff.person_request import PersonRequest
from kinopoisk_unofficial.request.staff.staff_request import StaffRequest

api_client = KinopoiskApiClient("b4aadb6a-b881-46ce-bacd-a25b8b5697e8")

class MovieInfo:
    def __init__(self):
        self.isEmpty = True
        self.id = 0
        self.poster = ""
        self.posterpreview = ""
        self.title = ""
        self.titleoriginal = ""
        self.rating = 0
        self.votesum = 0
        self.info = ""
        self.description = ""
        self.trailer = ""
        self.releaseyear = ""
        self.country = ""
        self.motto = ""
        self.director = ""
        self.budget = ""
        self.gross = ""
        self.duration = ""
    
    def getInfo(self, kinopoiskID, ID, actorsIDs):
        self.getMainInfo(kinopoiskID, ID)
        self.getTrailer(kinopoiskID)
        self.getStaff(kinopoiskID, actorsIDs)
        self.getBudgetAndGross(kinopoiskID)

    def getMainInfo(self, kinopoiskID, ID):
        request = FilmRequest(kinopoiskID)
        try:
            response = api_client.films.send_film_request(request)
        except Exception as e:
            self.isEmpty = True
            return
        self.id = ID
        self.poster = str(ID) + ".webp"
        saveImage(response.film.poster_url, self.poster)
        self.posterpreview = str(ID) + "_preview.webp"
        saveImage(response.film.poster_url_preview, self.posterpreview)
        self.title = response.film.name_ru
        self.titleoriginal = response.film.name_original
        self.rating = response.film.rating_kinopoisk
        self.votesum = response.film.rating_kinopoisk_vote_count
        self.info = str(response.film.year) + ", " + \
            response.film.countries[0].country + ", " + \
            response.film.genres[0].genre
        self.description = response.film.description.replace("'", "`")
        self.releaseyear = str(response.film.year)
        self.country = response.film.countries[0].country
        for country in response.film.countries[1 : ]:
            self.country += (", " + country.country)
        self.motto = response.film.slogan
        self.duration = str(response.film.film_length) + " мин."
        self.isEmpty = False
        return self

    def getTrailer(self, kinopoiskID):
        request = FilmVideoRequest(kinopoiskID)
        try:
            response = api_client.films.send_film_video_request(request)
        except Exception as e:
            self.isEmpty = True
            return
        for item in response.items:
            if item.site.name == "YOUTUBE":
                self.trailer = item.url
                return
        self.trailer = "https://www.youtube.com/"

    def getStaff(self, kinopoiskID, actorsIDs):
        request = StaffRequest(kinopoiskID)
        try:
            response = api_client.staff.send_staff_request(request)
        except Exception as e:
            self.isEmpty = True
            return
        actorsAmount = 0
        for item in response.items:
            if item.profession_key.value == "DIRECTOR":
                self.director = item.name_ru
                self.isEmpty = False
            elif actorsAmount < 30 and item.profession_key.value == "ACTOR":
                if not item.staff_id in actorsIDs:
                    actorsIDs[item.staff_id] = len(actorsIDs)
                    actorsAmount += 1
        

    def getBudgetAndGross(self, kinopoiskID):
        request = BoxOfficeRequest(kinopoiskID)

        try:
            response = api_client.films.send_box_office_request(request)
        except Exception as e:
            self.isEmpty = True
            return
        for item in response.items:
            if item.type == 'BUDGET':
                self.budget = str(item.amount) + " " + item.symbol
            elif item.type == "WORLD":
                self.gross = str(item.amount) + " " + item.symbol

        if not self.budget or not self.gross:
            self.isEmpty = True
        else:
            self.isEmpty = False
    
    def processFields(self):
        try:
            self.poster = self.poster.replace("'", "`")
            self.title = self.title.replace("'", "`")
            self.titleoriginal = self.titleoriginal.replace("'", "`")
            self.info = self.info.replace("'", "`")
            self.description = self.description.replace("'", "`")
            self.country = self.country.replace("'", "`")
            self.motto = self.motto.replace("'", "`")
            self.director = self.director.replace("'", "`")

        except Exception as e:
            print(str(e))
    def writeToFile(self, file, last=False):
        self.processFields()
        file.write("    (\n")
        file.write("        {},\n".format(self.id))
        file.write("        '{}',\n".format(self.poster))
        file.write("        '{}',\n".format(self.title))
        file.write("        '{}',\n".format(self.titleoriginal))
        file.write("        {},\n".format(self.rating))
        file.write("        {},\n".format(self.votesum))
        file.write("        '{}',\n".format(self.info))
        file.write("        '{}',\n".format(self.description))
        file.write("        '{}',\n".format(self.trailer))
        file.write("        '{}',\n".format(self.releaseyear))
        file.write("        '{}',\n".format(self.country))
        file.write("        '{}',\n".format(self.motto))
        file.write("        '{}',\n".format(self.director))
        file.write("        '{}',\n".format(self.budget))
        file.write("        '{}',\n".format(self.gross))
        file.write("        '{}'\n".format(self.duration))
        if last:
            file.write("    );\n")
        else:
            file.write("    ),\n")

def convertToWebp(name, oldName):
    destSource = Path('./webp/{name}'.format(name=name))
    destination = destSource.with_suffix(".webp")
    image = Image.open(Path('./img/{}'.format(oldName)))
    image.save(destination, format="webp")
    return destination

def saveImage(imageUrl, name):
    imgName = getNameFromUrl(imageUrl)
    imgData = requests.get(imageUrl).content
    with open('./img/{}'.format(imgName), 'wb') as handler:
        handler.write(imgData)
    convertToWebp(name, imgName)


def getNameFromUrl(imageUrl, preview=False):
    name = imageUrl[imageUrl.rindex("/") + 1 : ]
    return name

def cleanImages():
    files = glob.glob('./img/*')
    for f in files:
        os.remove(f)
    files = glob.glob('./webp/*')
    for f in files:
        os.remove(f)

def writeMoviesHeader(file):
    file.write("INSERT INTO\n")
    file.write("    movies (\n")
    file.write("        id,\n")
    file.write("        poster,\n")
    file.write("        title,\n")
    file.write("        titleoriginal,\n")
    file.write("        rating,\n")
    file.write("        votesnum,\n")
    file.write("        info,\n")
    file.write("        description,\n")
    file.write("        trailer,\n")
    file.write("        releaseyear,\n")
    file.write("        country,\n")
    file.write("        motto,\n")
    file.write("        director,\n")
    file.write("        budget,\n")
    file.write("        gross,\n")
    file.write("        duration\n")
    file.write("    )\n")
    file.write("VALUES\n")

def getMovies():
    print("[ LOG ]: Downloadinig movies...")
    id = 1
    moviesIDs = {}
    actorsIDs = {}
    cleanImages()
    moviesFile = open("movies_init.sql", "w")
    writeMoviesHeader(moviesFile)
    for kinopoiskId in range(300, 600):
        movieInfo = MovieInfo()
        movieInfo.getInfo(kinopoiskId, id, actorsIDs)
        if not movieInfo.isEmpty:
            print("[ DOWLOADED ]: KinoPoiskID =", kinopoiskId, ", ourID =", id)
            moviesIDs[kinopoiskId] = id
            id += 1
            movieInfo.writeToFile(moviesFile)
        else:
            print("[ EMPTY ]")
    
    moviesFile.close()
    print("[ LOG ]: Movies downloaded!")
    return moviesIDs, actorsIDs

def getSingleMovie(kinopoiskId, id, moviesIDs, actorsIDs):
    print("[ LOG ]: Downloadinig single movie...")
    moviesFile = open("movies_init.sql", "a")
    movieInfo = MovieInfo()
    movieInfo.getInfo(kinopoiskId, id, actorsIDs)
    if not movieInfo.isEmpty:
        print("[ DOWLOADED ]: KinoPoiskID =", kinopoiskId, ", ourID =", id)
        movieInfo.writeToFile(moviesFile)
        moviesIDs[kinopoiskId] = id
    else:
        print("[ EMPTY ]")
    moviesFile.close()
    print("[ LOG ]: Single movie downloaded!")
    return moviesIDs, actorsIDs


