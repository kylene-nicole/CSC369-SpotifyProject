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
        self.num_songs = 0

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
#         self.num_songs = int(input("Number of songs in this playlist: "))

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

import pandas as pd
import numpy as np
import dask.dataframe as dd
import dask.array as da

SPOTIFY_AUTH_TOKEN = 'BQA22Pjmblpb57wnSHEtxVhy__JW_ejfbUkAXicEiSbs21APAFXCcT3cw_pfb_7WhhO3NJ8ruWmIhZCr-JY'

# ----------------------------


# for rachel!
# Normally would use an OS to store this but cant if we are working together...SPOTIFY_AUTH_TOKEN = 'BQBdDRxg2FxcZ2AoSp9DUJQTi5NcX1uRWnwLmst0nHypW0-YMw_WGvSm00j4AHMTGZf-Z6VcE51PqXeLb0vYpSZ8zpDDCbKzq4_q94KVac1wlGk3_egC8cydo5LXEyEHvCXOXjEpzjIt2Pb7UuWrRH-MDZk-sGA'
spotC = SpotifyClient(SPOTIFY_AUTH_TOKEN, "")

# Run script 
spotC.playlist_title_prompt()
spotC.get_playlist_tracks(0)
playlist_json = spotC.response_json
spotC.response_json

# +
# create initial data set (don't use after first run)
first = pd.DataFrame()
l_a = []
for i in playlist_json['items']:
    song = i['track']
    l_a.append([song['artists'][0]['name'], song['name'], song['id'], i['added_by']['id'], spotC.spotify_id, 1])
    
temp = pd.DataFrame(l_a)
first = first.append(temp, ignore_index = True)
first.columns = ['artist', 'song', 'song_id', 'user_id', 'playlist_id', 'rating']
first.to_csv(r'data.txt', index=None, sep=',')
first

# +
# append to dataset

initial_pd = pd.read_csv("data.txt")
list_add = []
for i in playlist_json['items']:
    song = i['track']
    list_add.append([song['artists'][0]['name'], song['name'], song['id'], int(i['added_by']['id']), spotC.spotify_id, 1])
new_pd = pd.DataFrame(list_add, columns = ['artist', 'song', 'song_id', 'user_id', 'playlist_id', 'rating'])
new_pd.astype({'user_id' : initial_pd['user_id'].dtype.name})
final_pd = pd.concat([initial_pd, new_pd], ignore_index = True).drop_duplicates().reset_index(drop=True)
final_pd.to_csv(r'data.txt', index=None, sep=',')
final_pd


# -

initial_dd = dd.read_csv("data.txt")
list_dd = []
for i in playlist_json['items']:
    song = i['track']
    list_dd.append([song['artists'][0]['name'], song['name'], song['id'], int(i['added_by']['id']), spotC.spotify_id, 1])
new_pd = pd.DataFrame(list_add, columns = ['artist', 'song', 'song_id', 'user_id', 'playlist_id', 'rating'])
new_pd.astype({'user_id' : initial_pd['user_id'].dtype.name})
new_dd = dd.from_pandas(new_pd, chunksize = 50)
final_dd = dd.concat([initial_pd, new_pd], axis=0,interleave_partitions=True).drop_duplicates().reset_index(drop=True)
# final_pd.to_csv(r'data.txt', index=None, sep=',')
# final_pd.drop_duplicates()
final_dd.head()
initial_df = dd.read_csv("data.txt")
initial_df.head()


l_a = pd.Series(dtype = 'object')

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
