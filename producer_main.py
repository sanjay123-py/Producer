import os, sys
from src.kafka_logger import logging
from src.constants import DATA_PATH, SCHEMA_FILE_PATH, TOPIC
from src.kafka_producer.json_producer import produce_data

if __name__ == '__main__':
    produce_data(TOPIC, DATA_PATH, SCHEMA_FILE_PATH)