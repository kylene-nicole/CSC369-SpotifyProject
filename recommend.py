# # This file is to test the Evaluator
# # no implemention in this file

# +
from pyspark.sql import SparkSession
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
# -

spark_df = spark.read.csv('data.txt', header = True, quote = "\"", escape = "\"")

spark_df = spark_df.withColumn('rating_numeric', spark_df['rating'].cast('double'))

# Generate numeric IDs from song_id
song_indexer = StringIndexer(inputCol='song_id', outputCol='song_id_numeric')
temp = song_indexer.fit(spark_df).transform(spark_df)

# Generate numeric IDs from playlist_id
pl_indexer = StringIndexer(inputCol='playlist_id', outputCol='playlist_id_numeric')
final_df = pl_indexer.fit(temp).transform(temp)

(training, test) = final_df.randomSplit([0.9, 0.1])

# The ALS function only takes numeric values from ids
als = ALS(maxIter=10, regParam=0.01, userCol="playlist_id_numeric", itemCol="song_id_numeric", ratingCol="rating_numeric",
          coldStartStrategy="drop", implicitPrefs=False)
model = als.fit(training)

predictions = model.transform(test)
evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating_numeric",
                                predictionCol="prediction")
rmse = evaluator.evaluate(predictions)
print("Root-mean-square error = " + str(rmse))


# Generate top 10 song recs for every playlist
plRecs = model.recommendForAllUsers(100)
# Generate top 10 playlist recs for each song
songRecs = model.recommendForAllItems(10)

final_df.select(final_df["playlist_id"],final_df["playlist_id_numeric"]).filter(final_df.playlist_id  == "4LtjJ8L0V3Vc0blNiBe7s7").drop_duplicates().collect()

playlist_df = final_df.select(final_df["playlist_id"],final_df["playlist_id_numeric"]).drop_duplicates()
song_df = final_df.select(final_df["song_id_numeric"], final_df["song"], final_df["artist"]).drop_duplicates()

plRecs.show()

a = plRecs.join(playlist_df, plRecs.playlist_id_numeric == playlist_df.playlist_id_numeric)\
    .filter(playlist_df.playlist_id  == "4LtjJ8L0V3Vc0blNiBe7s7")\
    .select(plRecs.recommendations)


c = spark.createDataFrame(a.head()[0])

b = final_df.filter(final_df.playlist_id  == "4LtjJ8L0V3Vc0blNiBe7s7")

c.join(b, on=['song_id_numeric'], how='left_anti').show()

final_df.filter(final_df.song_id_numeric == 6).show()

b.filter(b.song_id_numeric == 7).show()

song_df.filter(song_df.song_id_numeric == 53).show()

df.as("table1").join(
  df2.as("table2"),
  $"table1.name" === $"table2.name" && $"table1.age" === $"table2.howold",
  "leftanti"
)

song_df.rdd.map(lambda line: tuple([x for x in line])).collect()



songs = song_df.rdd.map(lambda line: (line[0], (line[1], line[2]))).join(rdd).sortBy(lambda z: z[1]).collect()
songs

rdd = sc.parallelize(a.head()[0]).map(lambda line: tuple([x for x in line]))
rdd.collect()

print_songs = [x[1][0][0] + ": " + x[1][0][1] for x in songs]
print_songs

song_df.filter(song_df.artist == "Giveon").show()
