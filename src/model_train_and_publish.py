import os
import pandas as pd
import time
# import joblib
from minio import Minio
from minio.error import S3Error



# Configure the MinIO client with your MinIO server details
minio_client = Minio(
    os.environ.get('MINIO_ENDPOINT'),
    access_key=os.environ.get('MINIO_ACCESS_KEY_ID'),
    secret_key=os.environ.get('MINIO_SECRET_ACCESS_KEY'),
    secure=False,               
)


# Define the bucket name and object key for the data.csv file
bucket_name = os.environ.get('MINIO_BUCKET_NAME')


# For loading dataset/.csv files from MinIO Server

movies_csv_key = "datasets/movies.csv"
ratings_csv_key = "datasets/ratings.csv"

try:
    minio_client.fget_object(bucket_name, movies_csv_key, "movies.csv")
    print(f"Downloaded movies.csv from MinIO: s3://{bucket_name}/{movies_csv_key}")

    minio_client.fget_object(bucket_name, ratings_csv_key, "ratings.csv")
    print(f"Downloaded ratings.csv from MinIO: s3://{bucket_name}/{ratings_csv_key}")

except S3Error as e:
    print(f"Error downloading initial .csv dataset filesfrom MinIO: {e}")



# Reading data as pandas dataframe
ratings = pd.read_csv('ratings.csv')
movies = pd.read_csv('movies.csv')

# Data cleaning & manipulation
ratings = pd.merge(movies,ratings).drop(['genres','timestamp'],axis=1) 
user_ratings = ratings.pivot_table(index=['userId'],columns=['title'],values='rating')
user_ratings = user_ratings.dropna(thresh=10,axis=1).fillna(0)

# applying correlation algorithm
item_similarity_df = user_ratings.corr(method='pearson') 


# saving the trained recommendation model in .pkl file format
item_similarity_df.to_pickle('item_similarity_df.pkl')


# Define the object key for the trained recommendation model in MinIO
model_key = "models/item_similarity_df.pkl"


# uploading the trained recommendation model to MinIO
try:
    minio_client.fput_object(bucket_name, model_key, "item_similarity_df.pkl")
    print(f"Recommendation Model uploaded to MinIO: s3://{bucket_name}/{model_key}")
except S3Error as e:
    print(f"Error uploading recommendation model to MinIO: {e}")
