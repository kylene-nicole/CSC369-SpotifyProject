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
        self.api_token = api_token;
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
        print(" > Click Share \n > Click Copy Spotify URI \n *** *** ***")

        spotify_uri = input("Paste Spotify URI here: ")
        self.spotify_id = spotify_uri[17:]

    def get_playlist_tracks(self):
        """
        :param limit (int): number of tracks to get... should be less than X
        :param playlist_id (str): the Spotify Playlist ID extracted from user URI
        :return tracks (list of tracks): List of the playlist tracks
        """
        print(self.spotify_id)
        
        #with or without requests.get.... ?
        url = f"https://api.spotify.com/v1/playlists/{self.spotify_id}"
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
        )

        # unsure how to grab the right data/format... 

        response_json = response.json()
        print(response_json)
        
        print('**************')
        
        results = response_json['tracks']['items']
        
        print(results)
       
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

    # not completed for comparison yet...
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
    SPOTIFY_AUTH_TOKEN = 'BQDbkW7L3YCgPtyJ3mq048rNzSprTNFAz25oYVgoXGO1bmizUHujpulYnS4L5o0dPl8H_wVp97iruUBbdifX3ioni9N9Nr442_1iCP9ykQpdLo08XkfEKs8QiHFzwWMshRp9LKqK2lC07a_4UdrJq40iiJlCghQ'
    sc = SpotifyClient(SPOTIFY_AUTH_TOKEN, "")
    
    sc.playlist_title_prompt()
    sc.get_playlist_tracks()
    
    #get recommendations...\
    #output song.
    #WEB API?

if __name__ == '__main__':
    main()