from pymongo import MongoClient
from bson import ObjectId
import schemas as Schema
import random

def get_database():
 
   client = MongoClient("mongodb://localhost:27017/")

   db = client["spotify"]


   return db

def createartistwithalbums():

    releases = db["releases"]
    songs = db["songs"]
    artists = db["artists"]

    artist = Schema.artist()
    artistid = artists.insert_one(artist).inserted_id

    print(f"Artist, {artistid}, created...")

    release = Schema.release()

    numbersongs = random.randrange(1, 21)
    if numbersongs < 5:
        release["type"] = "Single/EP"
    else:
        release["type"] = "Album"
    release["artists"].append(ObjectId(artistid))
    releaseid = releases.insert_one(release).inserted_id

    print(f"Release, {release['title']}, created...")

    for i in range(numbersongs):
        song = Schema.song()
        song["releases"].append(ObjectId(releaseid))
        song["artists"].append(ObjectId(artistid))
        songid = songs.insert_one(song).inserted_id

        print(f"Song, {song['title']}, created...")
        releases.update_one({  "_id" : releaseid  }, { "$push": {  "songs" : ObjectId(songid)}})
    
    print(f"Songs added to {release['title']}...")

    artists.update_one({  "_id" : artistid  }, { "$push": {  "releases" : ObjectId(releaseid)}})

    print("Release added to Artist")

def getalbum(title):
    releases = db["releases"]
    songscollection = db["songs"]
    artistscollection = db["artists"]
    release = releases.find_one({ "title" : title})

    songs = release['songs']

    artist = artistscollection.find_one({ '_id' : release['artists'][0]})

    print(f"{release['title']} by {artist['name']}")

    for song in songs:
        foundsong = songscollection.find_one({ "_id" : song})
        minutes, seconds = divmod(foundsong["duration"], 60)
        print(f"\t{foundsong['title']} - {int(minutes)}:{int(seconds):02d}")

def createuser():
    users = db["users"]

    user = Schema.user()
    
    users.insert_one(user)

    print(f"User, {user['username']}, created...")

def usersfollowers():
    def generate_random_followers(user_ids, max_followers):
        num_followers = random.randint(5, max_followers)
        return random.sample(user_ids, num_followers)

    users_collection = db["users"]

    # Get all user IDs
    user_ids = [user['_id'] for user in users_collection.find({}, {'_id': 1})]

    # Update followers for each user
    for user_id in user_ids:
        followers = generate_random_followers(user_ids, max_followers=15)  # Adjust max_followers as needed
        users_collection.update_one({'_id': user_id}, {'$set': {'followers': followers}})

def usersfollowing():

    def generate_random_following(user_ids, max_following):
        num_following = random.randint(5, max_following)
        return random.sample(user_ids, num_following)

    users_collection = db["users"]  

    # Get all user IDs
    user_ids = [user['_id'] for user in users_collection.find({}, {'_id': 1})]

    # Update following for each user
    for user_id in user_ids:
        following = generate_random_following(user_ids, max_following=15)  # Adjust max_following as needed
        users_collection.update_one({'_id': user_id}, {'$set': {'following': following}})

def userslikemusic():

    def generate_random_songs(song_ids, minsongs, maxsongs):
        numsongs = random.randint(minsongs, maxsongs)
        return random.sample(song_ids, numsongs)

    songs_collection = db["songs"]
    users_collection = db["users"]
    release_collection = db["releases"]

    # Get all user IDs
    user_ids = [user['_id'] for user in users_collection.find({}, {'_id': 1})]
    song_ids = [song['_id'] for song in songs_collection.find({}, {'_id': 1})]
    release_ids = [release['_id'] for release in release_collection.find({}, {'_id': 1})]

    # Update songs for each user
    for user_id in user_ids:
        songs = generate_random_songs(song_ids, minsongs=20, maxsongs=300)  # Adjust max and min songs as needed
        releases = generate_random_songs(release_ids, minsongs=1, maxsongs=10)
        users_collection.update_one({'_id': user_id}, {'$set': { 'library': { 'releases': releases, 'songs': songs }}})

def createplaylistforusers():
    def generate_random_songs(song_ids, minsongs, maxsongs):
            numsongs = random.randint(minsongs, maxsongs)
            return random.sample(song_ids, numsongs)

    songs_collection = db["songs"]
    users_collection = db["users"]
    playlists = db["playlists"]

    user_ids = [user['_id'] for user in users_collection.find({}, {'_id': 1})]
    song_ids = [song['_id'] for song in songs_collection.find({}, {'_id': 1})]

    for user_id in user_ids:
        songs = generate_random_songs(song_ids, minsongs=3, maxsongs=40)
        playlist = Schema.playlist()
        playlist["user"] = user_id
        playlist["songs"] = songs
        
        playlistid = playlists.insert_one(playlist).inserted_id
        users_collection.update_one({  "_id" : user_id  }, { "$push": {  "playlists" : ObjectId(playlistid)}})

        print(f"Playlist {playlist['title']} created! Added to user {user_id}.")
    playlists = db["playlists"]
    playlistids = [user['_id'] for user in playlists.find({}, {'_id': 1})]
    for playlistid in playlistids:
        updatedplaylistdescription = Schema.playlist()["description"]
        playlists.update_one({ "_id": playlistid }, { "$set": { "description": updatedplaylistdescription }})

def createplaylistsforexistingartists():
    def generate_random_songs(song_ids, minsongs, maxsongs):
            numsongs = random.randint(minsongs, maxsongs)
            return random.sample(song_ids, numsongs)

    songs = db["songs"]
    artists = db["artists"]
    playlists = db["playlists"]

    artist_ids = [artist['_id'] for artist in artists.find({}, {'_id': 1})]
    song_ids = [song['_id'] for song in songs.find({}, {'_id': 1})]

    for artist_id in artist_ids:
        songs = generate_random_songs(song_ids, minsongs=3, maxsongs=40)
        playlist = Schema.artistplaylist()
        playlist["artist"] = artist_id
        playlist["songs"] = songs
        
        playlistid = playlists.insert_one(playlist).inserted_id
        artists.update_one({  "_id" : artist_id  }, { "$push": {  "playlists" : ObjectId(playlistid)}})

        print(f"Playlist {playlist['title']} created! Added to user {artist_id}.")

def createreleasesforexistingartists():

    songs = db["songs"]
    artists = db["artists"]
    releases = db["releases"]

    artist_ids = [artist['_id'] for artist in artists.find({}, {'_id': 1})]

    for artist_id in artist_ids:
        
        release = Schema.release()

        numbersongs = random.randrange(1, 21)
        if numbersongs < 5:
            release["type"] = "Single/EP"
        else:
            release["type"] = "Album"

        release["artists"].append(ObjectId(artist_id))
        releaseid = releases.insert_one(release).inserted_id

        print(f"Release, {release['title']}, created...")

        for i in range(numbersongs):
            song = Schema.song()
            song["releases"].append(ObjectId(releaseid))
            song["artists"].append(ObjectId(artist_id))
            songid = songs.insert_one(song).inserted_id

            print(f"Song, {song['title']}, created...")
            releases.update_one({  "_id" : releaseid  }, { "$push": {  "songs" : ObjectId(songid)}})
        
        print(f"Songs added to {release['title']}...")

        artists.update_one({  "_id" : artist_id  }, { "$push": {  "releases" : ObjectId(releaseid)}})

        print("Release added to Artist")

def fixsongs():
        # Access the 'songs' collection
    songs_collection = db['songs']

    # Find documents where the 'artist' attribute is an empty array
    songs_to_update = songs_collection.find({'artists': []})

    print(songs_to_update)

    # Iterate through the matching documents
    for song in songs_to_update:
        # Access the first ObjectID in the 'releases' array
        if 'releases' in song and song['releases']:
            first_release_id = song['releases'][0]

            print(f"Release {first_release_id}")

            # Find the associated release
            release = db['releases'].find_one({'_id': ObjectId(first_release_id)})

            if release:
                # Access the ObjectID in the release's 'artist' array
                if 'artists' in release:
                    artist_id = release['artists'][0]


                    # Find the associated artist
                    artist = db['artists'].find_one({'_id': ObjectId(artist_id)})
                    print(f"Artists {artist}")

                    if artist:
                        # Append the artist's ObjectID to the 'artists' array in the song
                        songs_collection.update_one(
                            {'_id': song['_id']},
                            {'$push': {'artists': artist['_id']}}
                        )


if __name__ == "__main__":   

    # Get the database for the functions to use
    db = get_database()

    # Creates songs for releases and releases for artists (each run creates 5 artists, 1 release per artist created (so 5 new releases))    
    #[createartistwithalbums() for _ in range(5)]

    # Call the function to update songs
    fixsongs()

    # Adds existing songs and releases to user's libraries
    # userslikemusic()

    # Creates playlists with songs for all users 3 times
    # [createplaylistforusers() for _ in range(3)]

    # Creates playlists with songs for all artists 8 times
    # [createplaylistsforexistingartists() for _ in range(8)]

    # Creates releases with songs for all artists 3 times
    # [createreleasesforexistingartists() for _ in range(3)]

    # Searchs for an album based on a string
    # getalbum("Dirt Radio")

    # Sets all user's following and follower lists
    # usersfollowers()
    # usersfollowing()

    # Creates 20 new users.
    # [createuser() for _ in range(20)]




    
