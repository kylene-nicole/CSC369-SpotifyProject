import json

import requests

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
        self.song_recs = None

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
    
    def get_recommendations(self, file):
        """
        """
        spark_df = spark.read.csv(file, header = True, quote = "\"", escape = "\"")
        
        # Make sure rating is numeric
        spark_df = spark_df.withColumn('rating_numeric', spark_df['rating'].cast('double'))
        
        # Generate numeric IDs from song_id
        song_indexer = StringIndexer(inputCol='song_id', outputCol='song_id_numeric')
        temp = song_indexer.fit(spark_df).transform(spark_df)
        
        # Generate numeric IDs from playlist_id
        pl_indexer = StringIndexer(inputCol='playlist_id', outputCol='playlist_id_numeric')
        final_df = pl_indexer.fit(temp).transform(temp)
        
        (training, test) = final_df.randomSplit([0.8, 0.2])
        # The ALS function only takes numeric values from ids
        als = ALS(maxIter=10, regParam=0.1, userCol="playlist_id_numeric", itemCol="song_id_numeric", 
                  ratingCol="rating_numeric", coldStartStrategy="drop", implicitPrefs=False)
        model = als.fit(training)
        
        # build and evaluate model
        predictions = model.transform(test)
        evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating_numeric",
                                    predictionCol="prediction")
        rmse = evaluator.evaluate(predictions)
        
        # Recommendations are formatted playlist_id_numeric : [song_id_numeric]
        # Need to get the actual song names instead of IDs
        playlist_df = final_df.select(final_df["playlist_id"],final_df["playlist_id_numeric"]).drop_duplicates()
        song_df = final_df.select(final_df["song_id_numeric"], final_df["song"], final_df["artist"]).drop_duplicates()
        
        # Generate top 200 song recs for every playlist
        plRecs = model.recommendForAllUsers(200)
        
        # find recs for a given playlist
        recs = plRecs.join(playlist_df, plRecs.playlist_id_numeric == playlist_df.playlist_id_numeric)\
                .filter(playlist_df.playlist_id  == self.spotify_id)\
                .select(plRecs.recommendations)
        
        # The ALS function does not prevent songs already in the playlist from being recommended
        # We must manually remove all songs that are already in the playlist
        recommends = spark.createDataFrame(recs.head()[0])
        already_in = final_df.filter(final_df.playlist_id  == self.spotify_id)
        filtered_recs = recommends.join(already_in, on=['song_id_numeric'], how='left_anti')
        
        # convert recs from dataframe to rdd and find their song names by joining with song_df
        # Grab top 25 suggestions and output them
        rec_rdd = filtered_recs.rdd.map(lambda line: tuple([x for x in line]))
        song_names = song_df.rdd.map(lambda line: (line[0], (line[1], line[2]))).join(rec_rdd)\
                            .sortBy(lambda z: z[1][1]).take(25)
        
        print("Here are some song suggestions for your playlist:")
        [print(x[1][0][0] + " by " + x[1][0][1]) for x in song_names]

        self.song_recs = song_names
        

    def output_songs(self):
        """
        """
        #data = json.dumps()
        #print

def main():
    # Normally would use an OS to store this but cant if we are working together...
    spotC = SpotifyClient(SPOTIFY_AUTH_TOKEN, "")
    spotC.playlist_title_prompt()
    all_songs = spotC.get_playlist_tracks1(0)
    update_dask("data.txt", all_songs, spotC)

    spotC.get_recommendations('data.txt')
if __name__ == '__main__':
    main()

# # Imports and API Access 

# +
import pandas as pd
import numpy as np
import dask.dataframe as dd
import dask.array as da
from pyspark.sql import SparkSession
import requests
import time
import os
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.sql import Row
from pyspark.sql.functions import col, row_number
from pyspark.sql.window import Window
from pyspark.ml.feature import StringIndexer

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

# # Create initial data file


# create inital data file
def create_dataset(file):
    if os.path.isfile(file):
        print ("File already exists")
        return
    else:
        f = open(file,"w+")
        f.write("artist,song,song_id,playlist_id,rating\n")
        f.close()
        return


# # PANDAS update dataset

def update_pandas(file, json_datas, spotify_client):
    initial_pd = pd.read_csv(file, header = 0)
    initial_pd
    list_add = []
    for json_data in json_datas:
        for i in json_data['items']:
            song = i['track']
            if song is not None:
                if song['id'] is not None:
                    list_add.append([song['artists'][0]['name'], song['name'], song['id'],  spotify_client.spotify_id, 1])
    new_pd = pd.DataFrame(list_add, columns = ['artist', 'song', 'song_id',  'playlist_id', 'rating'])
    if len(initial_pd) > 0:
        new_pd.astype({'rating' : initial_pd['rating'].dtype.name})
    final_pd = pd.concat([initial_pd, new_pd], ignore_index = True).drop_duplicates().reset_index(drop=True)
    existing_rows = initial_pd.shape[0]
    new_rows = final_pd.shape[0]
    if existing_rows < new_rows:
        final_pd.loc[existing_rows:].to_csv('data.txt', index=None, sep=',',mode='a', header = False)
        return final_pd
    return "No new songs to add"


# # DASK update dataset

def update_dask(file, json_datas, spotify_client, chunk = 200):
    start = time.time()
    initial_dd = dd.read_csv(file)
    list_dd = []
    for json_data in json_datas:
        for i in json_data['items']:
            song = i['track']
            if song is not None:
                if song['id'] is not None:
                    list_dd.append([song['artists'][0]['name'], song['name'], song['id'],  spotify_client.spotify_id, 1])
    end = time.time()
#     print(end - start)

    new_pd = pd.DataFrame(list_dd, columns = ['artist', 'song', 'song_id', 'playlist_id', 'rating'])
    new_pd.astype({'rating' : 'int64'})
    new_dd = dd.from_pandas(new_pd, chunksize = chunk)
    final_dd = dd.concat([initial_dd, new_dd], axis=0,interleave_partitions=True).drop_duplicates().reset_index(drop=True)
    
    end = time.time()
#     print(end - start)

    existing_rows = initial_dd.shape[0]
    new_rows = final_dd.shape[0]
    if existing_rows.compute() < new_rows.compute():
        final_dd.loc[existing_rows:].to_csv('data.txt', index=None, sep=',',mode='a', header = False)
        
        end = time.time()
#         print(end - start)
        return final_dd
    return "No new songs to add"

# # SPARK update dataset

# notes: method cannot specify saved file name
def update_spark(file, json_data, spotify_client):
    initial_spark = spark.read.csv(file, header = True, quote = "\"", escape = "\"")
    list_spark = []
    for i in json_data['items']:
        song = i['track']
        if song is not None:
                if song['id'] is not None:
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

# # Generate Predictions

# +
spotC = SpotifyClient(get_token(client_id, client_secret, auth_url), "")
spotC.playlist_title_prompt()
all_songs = spotC.get_playlist_tracks1(0)
update_dask("data.txt", all_songs, spotC)

spotC.get_recommendations('data.txt')
# -


