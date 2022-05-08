from urllib import response
from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.model.box_office import BoxOffice
from kinopoisk_unofficial.request.films.box_office_request import BoxOfficeRequest
from kinopoisk_unofficial.request.films.distributions_request import DistributionsRequest
from kinopoisk_unofficial.request.films.film_request import FilmRequest
import requests
import os
import glob
from pathlib import Path
from PIL import Image

from kinopoisk_unofficial.request.films.film_video_request import FilmVideoRequest
from kinopoisk_unofficial.request.staff.staff_request import StaffRequest

api_client = KinopoiskApiClient("b4aadb6a-b881-46ce-bacd-a25b8b5697e8")

class MovieInfo:
    def __init__(self):
        self.isEmpty = True
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
    
    def getInfo(self, kinopoiskID, ID):
        self.getKinoPoiskMovieInfo(kinopoiskID, ID)
        self.getTrailer(kinopoiskID)
        self.getDirector(kinopoiskID)
        self.getBudgetAndGross(kinopoiskID)

    def getKinoPoiskMovieInfo(self, kinopoiskID, ID):
        request = FilmRequest(kinopoiskID)
        try:
            response = api_client.films.send_film_request(request)
        except Exception as e:
            self.isEmpty = True
            return
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
        self.description = response.film.description
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

    def getDirector(self, kinopoiskID):
        request = StaffRequest(kinopoiskID)
        try:
            response = api_client.staff.send_staff_request(request)
        except Exception as e:
            self.isEmpty = True
            return
        for item in response.items:
            if item.profession_key.value == "DIRECTOR":
                self.director = item.name_ru
                self.isEmpty = False
                return
        
        self.director = ""
        self.isEmpty = True

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
    
    def writeToFile(self, file):
        file.write("\t(\n")
        file.write("\t\t\'{}\',\n".format(self.poster))
        file.write("\t\t\'{}\',\n".format(self.title))
        file.write("\t\t\'{}\',\n".format(self.titleoriginal))
        file.write("\t\t{},\n".format(self.rating))
        file.write("\t\t{},\n".format(self.votesum))
        file.write("\t\t\'{}\',\n".format(self.info))
        file.write("\t\t\'{}\',\n".format(self.description))
        file.write("\t\t\'{}\',\n".format(self.trailer))
        file.write("\t\t\'{}\',\n".format(self.releaseyear))
        file.write("\t\t\'{}\',\n".format(self.country))
        file.write("\t\t\'{}\',\n".format(self.motto))
        file.write("\t\t\'{}\',\n".format(self.director))
        file.write("\t\t\'{}\',\n".format(self.budget))
        file.write("\t\t\'{}\',\n".format(self.gross))
        file.write("\t\t\'{}\',\n".format(self.duration))
        file.write("\t),\n")

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

id = 1
cleanImages()
moviesFile = open("movies_init.sql", "w")
for kinopoiskId in range(300, 500):
    movieInfo = MovieInfo()
    movieInfo.getInfo(kinopoiskId, id)
    if not movieInfo.isEmpty:
        print("[ DOWLOADED ]: KinoPoiskID =", kinopoiskId, ", ourID =", id)
        movieInfo.writeToFile(moviesFile)
        id += 1
    else:
        print("[ EMPTY ]")
moviesFile.close()

