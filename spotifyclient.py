import json

import requests

from track import Track
from playlist import Playlist

class SpotifyClient:
    """ Perform actions to communicate with Spotify API """
    def __init__(self, authorization_token, user_id):
        """
        :param authorization_token (str): Spotify API token
        :param user_id (int): Spotify user id
        """
        self.authorization_token = authorization_token
        self.user_id = user_id

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
        spotify_id = spotify_uri[17:]
        return spotify_id

   # video uses the history instad of playlist... alter this for our project
    def get_playlist_tracks(self, playlist_id, limit = 10): #limit? come back to this
        """
        :param limit (int): number of tracks to get... should be less than X
        :param playlist_id (str): the Spotify Playlist ID extracted from user URI
        :return tracks (list of tracks): List of the playlist tracks
        """
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        response = self._place_get_api_request(url)
        response_json = response.json()
        tracks = # Rachel how do i use json to access tracks and save them? See:
        """
        https://developer.spotify.com/documentation/web-api/reference/#object-playlistobject
        """
        return tracks

    # checking out spotify api endpoint reference....  BROWSE ~ they have
    # all the metrics already listed...
    """
    https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-recommendations
    https://developer.spotify.com/documentation/web-api/reference/#category-browse
    """
