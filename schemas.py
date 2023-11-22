import gens as Gens
from bson import ObjectId
from datetime import datetime

def user():

    User = Gens.User()

    return {
        "username": User.username,
        "email": User.email,
        "accountCreated": User.accountCreated,
        "followers": [],
        "following": [],
        "playlists": [],
        "library": {
            "releases": [],
            "songs": []
        }
    }

def artist():

    Artist = Gens.Artist()

    return {
        "name": Artist.name,
        "followers": Artist.followers,
        "monthlyListeners": Artist.monthlyListeners,
        "bio": Artist.bio,
        "links": {
            "instagram": f"@{Artist.link}", 
            "twitter": f"@{Artist.link}",
            "soundcloud": f"@{Artist.link}",
            "bandcamp": f"@{Artist.link}",
            "youtube": f"@{Artist.link}",
            "website": f"https://{Artist.link}.com" 
        },
        "releases": [],
        "playlists": []
    }

def release():

    Release = Gens.Release()

    return {
        "title": Release.title,
        "type": Release.type,
        "releaseDate": Release.releaseDate,
        "label": Release.label,
        "saves": Release.saves,
        "tags": Release.tags,
        "artists": [],
        "songs": []
    }

def song():

    Song = Gens.Song()

    return {
        "title": Song.title,
        "artists": [],
        "plays": Song.plays,
        "duration": Song.duration,
        "saves": Song.saves,
        "releases": [],
        "metadata": {
            "performers": [],
            "writers": Song.writers,
            "producers": Song.producers
        },
        "tags": Song.tags
    }