import json

import requests

from track import Track
from playlist import Playlist

class SpotifyClient:
    """ Perform actions to communicate with Spotify API """
    def __init__(self, authorization_token, spotify_id):
        """
        :param authorization_token (str): Spotify API token
        :param user_id (int): Spotify user id
        """
        self.authorization_token = authorization_token
        self.spotify_id = spotify_id

    def playlist_title_prompt(self):
        """
        Prompt the user for their playlist URI, we will extract the ID from that
        Example: spotify:playlist:6hzUZESozP9M7qKxJ8voKe
            slice off the 'spotify:playlist:'
            ID: 6hzUZESozP9M7qKxJ8voKe
        """
        print("Please retrieve your Spotify Playlist URI so we can recommend you songs!")
        print("*** How? ***\n > Right-click on your playlist in Spotify")
        print("\n > Share \n > Copy Spotify URI \n *** *** ***")

        spotify_uri = input("Paste Spotify URI here: ")
        self.spotify_id = spotify_uri[17:]
        return self.spotify_id

   # video uses the history instad of playlist... alter this for our project
    def get_playlist_tracks(self, limit = 10): #limit? come back to this
        """
        :param limit (int): number of tracks to get... should be less than X
        :param playlist_id (str): the Spotify Playlist ID extracted from user URI
        :return tracks (list of tracks): List of the playlist tracks
        """
        url = f"https://api.spotify.com/v1/playlists/{self.spotify_id}"
        response = self._place_get_api_request(url)

        response_json = response.json()
        print(response_json)
        #tracks = # Rachel how do i use json to access tracks and save them? See:
       
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
    def get_recommendations(self, seed_tracks, limit = 50):
        """
        """
        seed_tracks_url = ""
        for tracks in seed_tracks:
            seed_tracks_url += seed_tracks.id + ","
        seed_tracks_url = seed_tracks_url[:-1]
        url = f""
        response = self._place_get_api_request(url)
        response_json = response.json()
        #tracks = ...
        #return tracks

    def output_songs(self):
        """
        """
        #data = json.dumps()
        #print


class Track:
    """  """
    def __init__(self, name, id, artist):
        """
        :param name (str): Track name
        :param id (int): Spotify track id
        :param artist (str): Artist who created the track 
        """
        self.name = name
        self.id = id
        self.artist = artist

    # i dont think we need this since we are just outputtng a song not playlist
    def create_spotify_uri(self):
        return f"spotify:track:{self.id}"

    def __str__(self):
        return f"{self.name} by {self.artist}"