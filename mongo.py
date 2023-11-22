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

if __name__ == "__main__":   

    # Get the database
    db = get_database()

    users = db["users"]

    '''
    for i in range(5): 
        createartistwithalbums()
    '''

    #getalbum("Dirt Radio")

    usersfollowers()
    usersfollowing()

'''    for i in range(20):
        createuser()'''




    
