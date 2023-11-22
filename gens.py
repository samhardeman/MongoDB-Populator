import random
from datetime import datetime

class Items:
    def firstname():
        firstnamesfile = open('firstnames.txt', 'r')
        firstnames = firstnamesfile.readlines()
        return firstnames[random.randrange(1, len(firstnames))].strip()
    
    def lastname():
        lastnamesfile = open('surnames.txt', 'r')
        lastnames = lastnamesfile.readlines()
        return lastnames[random.randrange(1, len(lastnames))].strip()
    
    def fullname():
        return f"{Items.firstname()} {Items.lastname()}"
    
    def teams():
        teamsfile = open('teams.txt', 'r')
        teams = teamsfile.readlines()
        return teams[random.randrange(1, len(teams))].strip()
    
    def objects():
        objectsfile = open('objects.txt', 'r')
        objects = objectsfile.readlines()
        return objects[random.randrange(1, len(objects))].strip()
    
    def predicates():
        predicatesfile = open('predicates.txt', 'r')
        predicates = predicatesfile.readlines()
        return predicates[random.randrange(1, len(predicates))].strip()
    
    def rand(lower, upper):
        return random.randrange(lower, upper+1)

    
class Artist:

    def artistname(self):

        thedecider = ""
        if random.randrange(0, 2) == 1:
            thedecider = "The "
        
        artistname = f"{thedecider}{Items.teams()} {Items.objects()}".title()

        if random.randrange(0, 2) == 1:
            artistname = Items.fullname()

        return artistname
    
    def biomaker(self, artistname):
        lorem = f"{artistname} dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. {artistname} sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. - {Items.fullname()}, Rovi"

        return lorem
    
    def __init__(self):
        self.name = self.artistname()
        self.followers = Items.rand(10, 10000)
        self.monthlyListeners = (self.followers*Items.rand(5, 10))+Items.rand(10, int(self.followers/10))
        self.bio = self.biomaker(self.name)
        self.link = "".join(self.name.split())

class User:
    def __init__(self):
        self.username = f"{Items.firstname()}{Items.rand(100, 999)}"
        self.email = f"{self.username}@email.com"
        self.accountCreated = datetime.now()

class Release:
    def __init__(self):
        self.title = title()
        self.label = self.label()
        self.type = self.releasetype()
        self.releaseDate = Items.rand(1990, 2023)
        self.saves = Items.rand(10, 10000)
        self.tags = tags()

    def label(self):
        return Items.objects().title()
    
    def releasetype(self):
        releasetype = "Album"
        if Items.rand(0, 1) == 1:
            releasetype = "Single/EP"

        return releasetype
    
    def releaseDate(self):
        return Items.rand(1990, 2023)
    
class Song:
    def __init__(self):
        self.title = title()
        self.plays = Items.rand(100, 10000000)
        self.duration = Items.rand(15, 600)
        self.saves = Items.rand(100, 100000)
        self.writers = peoplearray()
        self.producers = peoplearray()
        self.tags = tags()

def title():
    thedecider = ""

    if random.randrange(0, 2) == 1:
        thedecider = "The "

    return f"{thedecider}{Items.predicates()} {Items.objects()}".title()

def playlist():
    return Items.predicates().title()


def playsnumber():
    return random.randrange(1, 10000)

def email(username):
    return f"{username}{random.randrange(0, 1000)}@email.com"

def username():
    return f"{Items.predicates()}{Items.firstname()}{random.randrange(1, 1000)}".lower()

def tags():
    length = random.randrange(2, 10)
    tagsarray = []
    for i in range(length):
        tagsarray.append(Items.predicates())
    return tagsarray

def peoplearray():
    length = random.randrange(2, 4)
    peoplearray = []
    for i in range(length):
        peoplearray.append(Items.fullname())
    return peoplearray

def duration():
    return random.randrange(15, 600)

def item(item):
    filename = open(f'{item}.txt', 'r')
    lines = filename.readlines()
    return lines[random.randrange(1, len(lines))].strip()