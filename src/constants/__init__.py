import os
from pathlib import Path
SCHEMA_FILE_PATH = '/producer/sample_data/movie_analytics_data/schema_structure.txt'
# SCHEMA_FILE_PATH = '/Users/sanjay/Desktop/producer/sample_data/movie_analytics_data/schema_structure.txt'
DATA_PATH = 'movie_analytics_data/ratings.dat'
BUCKET_NAME = 'rds-movie-analytics'
REGION = 'ap-south-1'
TOPIC = 'RDS_MOVIE_TOPIC'