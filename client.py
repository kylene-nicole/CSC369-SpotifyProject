import json

import requests

#from track import Track
from playlist import Playlist

class SpotifyClient:
    """ Perform actions to communicate with Spotify API """
    def __init__(self, api_token, spotify_id = ""):
        """
        :param authorization_token (str): Spotify API token
        :param user_id (int): Spotify user id
        """
        self.api_token = api_token
        self.spotify_id = spotify_id
        self.response_json = None

    def playlist_title_prompt(self):
        """
        Prompt the user for their playlist URI, we will extract the ID from that
        Example: spotify:playlist:6hzUZESozP9M7qKxJ8voKe
            slice off the 'spotify:playlist:'
            ID: 6hzUZESozP9M7qKxJ8voKe
        """
        print("Please retrieve your Spotify Playlist URI so we can recommend you songs!")
        print("*** How? ***\n > Right-click on your playlist in Spotify")
        print(" > Click Share \n > Click Copy Spotify URI \n *** *** ***")

        spotify_uri = input("Paste Spotify URI here: ")
        self.spotify_id = spotify_uri[17:]

    def get_playlist_tracks(self, offset):
        """
        :param limit (int): number of tracks to get... should be less than X
        :param playlist_id (str): the Spotify Playlist ID extracted from user URI
        :return tracks (list of tracks): List of the playlist tracks
        """
        print(self.spotify_id)
        
        #with or without requests.get.... ?
        url = f"https://api.spotify.com/v1/playlists/{self.spotify_id}/tracks"
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            },
            params={
                "offset": offset,
                "limit": 100
            }
        )
            

        self.response_json = response.json()
        print(self.response_json)
        
        print('**************')
        
        
        #results = response_json['tracks']['items']
        
        #print(results)
       
        """
        https://developer.spotify.com/documentation/web-api/reference/#object-playlistobject
        """
        #return tracks

    # checking out spotify api endpoint reference....  BROWSE ~ they have
    # all the metrics already listed...
    """
    https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-recommendations
    https://developer.spotify.com/documentation/web-api/reference/#category-browse
    """
    
    def get_playlist_tracks1(self, offset):
        """
        :param limit (int): number of tracks to get... should be less than X
        :param playlist_id (str): the Spotify Playlist ID extracted from user URI
        :return tracks (list of tracks): List of the playlist tracks
        """
        print(self.spotify_id)
        
        url = f"https://api.spotify.com/v1/playlists/{self.spotify_id}/tracks"
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            },
            params={
                "offset": offset,
                "limit": 100
            }
        )
        list_json = []
        list_json.append(response.json())
        while response.json()['next'] is not None:
            time.sleep(2)
            response = requests.get(
            response.json()['next'],
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
                }
            )
            list_json.append(response.json())

        return list_json
    
    def get_recommendations(self, seed_tracks):
        """
        """
        seed_tracks_url = ""
        for tracks in seed_tracks:
            seed_tracks_url += seed_tracks.id + ","
        seed_tracks_url = seed_tracks_url[:-1]
        url = f""
        response = requests.get(url)
        response_json = response.json()
        #tracks = ...
        #return tracks

    def output_songs(self):
        """
        """
        #data = json.dumps()
        #print

def main():
    # Normally would use an OS to store this but cant if we are working together...
    SPOTIFY_AUTH_TOKEN = 'BQAPzXQWJ_YdqlHrR6hX8JBv6cMvM2-kIrppEcDaJD3vMOHFoLx7KM44EeD9aWswFJU0-9IcYunHWk_9xOY'
    sc = SpotifyClient(SPOTIFY_AUTH_TOKEN, "")
    
    sc.playlist_title_prompt()
    sc.get_playlist_tracks(200)
    #sc.response_json
    
    
    
    #get recommendations...\
    #output song.
    #WEB API?

if __name__ == '__main__':
    main()

# +
import pandas as pd
import numpy as np
import dask.dataframe as dd
import dask.array as da
from pyspark.sql import SparkSession
import requests
import time

spark = SparkSession \
    .builder \
    .appName("Python Spark") \
    .getOrCreate()

sc = spark.sparkContext


# +
# To obtain client_id and client_secret, create an app on the Spotify developer dashboard
# https://developer.spotify.com/dashboard/login

def get_token(cli_id, cli_sec, auth):
    auth_response = requests.post(auth, {
    'grant_type': 'client_credentials',
    'client_id': cli_id,
    'client_secret': cli_sec,
    })
    return auth_response.json()['access_token']


# -

client_id = 'e9df33e64151423da7de01eaf0cb5864'
client_secret = 'bf57e0ad0c464dd08ddd9d071fa20fa7'
auth_url = 'https://accounts.spotify.com/api/token'

SPOTIFY_AUTH_TOKEN = get_token(client_id, client_secret, auth_url)
SPOTIFY_AUTH_TOKEN

# ----------------------------


# for rachel!
# Normally would use an OS to store this but cant if we are working together...SPOTIFY_AUTH_TOKEN = 'BQBdDRxg2FxcZ2AoSp9DUJQTi5NcX1uRWnwLmst0nHypW0-YMw_WGvSm00j4AHMTGZf-Z6VcE51PqXeLb0vYpSZ8zpDDCbKzq4_q94KVac1wlGk3_egC8cydo5LXEyEHvCXOXjEpzjIt2Pb7UuWrRH-MDZk-sGA'
spotC = SpotifyClient(SPOTIFY_AUTH_TOKEN, "")

# Run script 
spotC.playlist_title_prompt()
spotC.get_playlist_tracks(0)
playlist_json = spotC.response_json
spotC.response_json

# Playlists with >100 songs
spotC.playlist_title_prompt()
all_songs = spotC.get_playlist_tracks1(0)

# +
# create initial data set (don't use after first run)
first = pd.DataFrame()
l_a = []
for i in playlist_json['items']:
    song = i['track']
    l_a.append([song['artists'][0]['name'], song['name'], song['id'],  spotC.spotify_id, 1])
    
temp = pd.DataFrame(l_a)
first = first.append(temp, ignore_index = True)
first.columns = ['artist', 'song', 'song_id', 'playlist_id', 'rating']
first.to_csv(r'data.txt', index=None, sep=',')
first


# -

# PANDAS
# update dataset
def update_pandas(file, json_datas, spotify_client):
    initial_pd = pd.read_csv(file)
    list_add = []
    for json_data in json_datas:
        for i in json_data['items']:
            song = i['track']
            if song['id'] is not None:
                list_add.append([song['artists'][0]['name'], song['name'], song['id'],  spotify_client.spotify_id, 1])
    new_pd = pd.DataFrame(list_add, columns = ['artist', 'song', 'song_id',  'playlist_id', 'rating'])
    new_pd.astype({'rating' : initial_pd['rating'].dtype.name})
    final_pd = pd.concat([initial_pd, new_pd], ignore_index = True).drop_duplicates().reset_index(drop=True)
    existing_rows = initial_pd.shape[0]
    new_rows = final_pd.shape[0]
    if existing_rows < new_rows:
        final_pd.loc[existing_rows:].to_csv('data.txt', index=None, sep=',',mode='a', header = False)
        return final_pd
    return "No new songs to add"


start = time.time()
update_pandas("data.txt", all_songs, spotC)
end = time.time()
print(end - start)


# DASK update dataset
def update_dask(file, json_datas, spotify_client, chunk = 200):
    start = time.time()
    initial_dd = dd.read_csv(file)
    list_dd = []
    for json_data in json_datas:
        for i in json_data['items']:
            song = i['track']
            if song['id'] is not None:
                list_dd.append([song['artists'][0]['name'], song['name'], song['id'],  spotify_client.spotify_id, 1])
    end = time.time()
    print(end - start)

    new_pd = pd.DataFrame(list_dd, columns = ['artist', 'song', 'song_id', 'playlist_id', 'rating'])
    new_pd.astype({'rating' : 'int64'})
    new_dd = dd.from_pandas(new_pd, chunksize = chunk)
    final_dd = dd.concat([initial_dd, new_dd], axis=0,interleave_partitions=True).drop_duplicates().reset_index(drop=True)
    
    end = time.time()
    print(end - start)

    existing_rows = initial_dd.shape[0]
    new_rows = final_dd.shape[0]
    if existing_rows.compute() < new_rows.compute():
        final_dd.loc[existing_rows:].to_csv('data.txt', index=None, sep=',',mode='a', header = False)
        
        end = time.time()
        print(end - start)
        return final_dd
    return "No new songs to add"

# start = time.time()
update_dask("data.txt", all_songs, spotC)
# end = time.time()
# print(end - start)

# SPARK update dataset
# notes: method cannot specify saved file name
def update_spark(file, json_data, spotify_client):
    initial_spark = spark.read.csv(file, header = True, quote = "\"", escape = "\"")
    list_spark = []
    for i in json_data['items']:
        song = i['track']
        list_spark.append([song['artists'][0]['name'], song['name'], song['id'],  spotify_client.spotify_id, 1])

    spark_rdd = sc.parallelize(list_spark)
    new_spark = spark_rdd.toDF(['artist', 'song', 'song_id', 'playlist_id', 'rating'])
    final_spark = new_spark.subtract(initial_spark)

    if final_spark.count() > 0:
        final_spark.write.csv('/home/jupyter-joshan@calpoly.edu-0e478/CSC369-SpotifyProject/', sep=',',mode='append')
        return final_spark
    final_spark.write.csv('/home/jupyter-joshan@calpoly.edu-0e478/CSC369-SpotifyProject/', sep=',',mode='append')
    return "No new songs to add"


update_spark("data.txt", playlist_json, spotC)

# get recommendations...\
# output song.
# WEB API?

# notes
['tracks']['items']
spotify:playlist:1GN4sQhsGhAOfxIaURcC9c
        
        songid
        artist
        name
        artist id
        popular id
        > ALS jonathan

# +
# 1. Saving and writing into csv or txt file. Optimally this would be implemented with distributed computing
# 2. (Optional) Implement multi-hundreds
# 3. Find public URLs and add them to our data set
# 4. Implement PySpark ALS fucntion
# 5. (Optional) Print images
