from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from movieParser import saveImage
from kinopoisk_unofficial.request.staff.person_request import PersonRequest

api_client = KinopoiskApiClient("b4aadb6a-b881-46ce-bacd-a25b8b5697e8")

class ActorInfo:
    def __init__(self):
        self.isEmpty = True
        self.id = 0
        self.imgsrc = ""
        self.name = ""
        self.nameoriginal = ""
        self.career = ""
        self.height = 0
        self.birthday = 0
        self.birthplace = ""
        self.total = ""
    
    def getInfo(self, kinopoiskID, ID, newActorsIDs):
        self.getMainInfo(kinopoiskID, ID, newActorsIDs)

    def getMainInfo(self, kinopoiskID, ID, newActorsIDs):
        request = PersonRequest(kinopoiskID)
        try:
            response = api_client.staff.send_person_request(request)
        except Exception as e:
            self.isEmpty = True
            return
        self.id = ID
        newActorsIDs[kinopoiskID] = ID
        self.imgsrc = str(ID) + "_actor.webp"
        saveImage(response.posterUrl, self.imgsrc)
        self.name = response.nameRu
        self.nameoriginal = response.nameEn
        self.career = response.profession
        self.height = str(response.growth) + " см"
        self.birthday = response.birthday
        self.birthplace = response.birthplace
        self.total = len(response.films)
        self.isEmpty = False
        
    def writeToFile(self, file, last=False):
        file.write("    (\n")
        file.write("        {},\n".format(self.id))
        file.write("        '{}',\n".format(self.imgsrc.replace("'", "`")))
        file.write("        '{}',\n".format(self.name.replace("'", "`")))
        file.write("        '{}',\n".format(self.nameoriginal.replace("'", "`")))
        file.write("        '{}',\n".format(self.career.replace("'", "`")))
        file.write("        '{}',\n".format(self.height.replace("'", "`")))
        file.write("        '{}',\n".format(self.birthday.replace("'", "`")))
        file.write("        '{}',\n".format(self.birthplace.replace("'", "`")))
        file.write("        {}\n".format(self.total))
        if last:
            file.write("    );\n")
        else:
            file.write("    ),\n")

def writeActorsHeader(file):
    file.write("INSERT INTO\n")
    file.write("    actors (\n")
    file.write("        id,\n")
    file.write("        imgsrc,\n")
    file.write("        name,\n")
    file.write("        nameoriginal,\n")
    file.write("        career,\n")
    file.write("        height,\n")
    file.write("        birthday,\n")
    file.write("        birthplace,\n")
    file.write("        total\n")
    file.write("    )\n")
    file.write("VALUES\n")

def getActors(actorsIDs):
    newActorsIDs = {}
    id = 1
    print("[ LOG ]: Donwloading persons for movies...")
    moviesFile = open("actors_init.sql", "w")
    writeActorsHeader(moviesFile)
    i = 0
    for kinopoiskId in actorsIDs:
        actorInfo = ActorInfo()
        actorInfo.getInfo(kinopoiskId, actorsIDs[kinopoiskId], newActorsIDs)
        if not actorInfo.isEmpty:
            print("[ DOWLOADED ]: KinoPoiskID =", kinopoiskId, ", ourID =", actorsIDs[kinopoiskId])
            if i == len(actorsIDs) - 1:
                actorInfo.writeToFile(moviesFile, True)
            else:
                actorInfo.writeToFile(moviesFile)
        else:
            print("[ EMPTY ]: KinoPoiskID = ", kinopoiskId)
        i += 1
    print("[ LOG ]: Actors for movies are downloaded!")
    # print("[ LOG ]: Downloading remaining persons...")
    # id = len(actorsIDs)
    # for kinopoiskId in range(0, 700):
    #     if (kinopoiskId in actorsIDs):
    #         continue
    #     actorInfo = ActorInfo()
    #     actorInfo.getInfo(kinopoiskId, id)
    #     if not actorInfo.isEmpty:
    #         print("[ DOWLOADED ]: KinoPoiskID =", kinopoiskId, ", ourID =", id)
    #         if kinopoiskId == 699:
    #             actorInfo.writeToFile(moviesFile, True)
    #         else:
    #             actorInfo.writeToFile(moviesFile)
    #         id += 1
    #     else:
    #         print("[ EMPTY ]: KinoPoiskID = ", kinopoiskId)
    moviesFile.close()
    print("[ LOG ]: Persons are downloaded!")
    return newActorsIDs

