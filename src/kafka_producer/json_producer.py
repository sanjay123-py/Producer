import os, sys
import time
import pandas as pd
import numpy as np
from typing import List
from uuid import uuid4
from src.kafka_config import sasl_config, schema_config
from src.entity.generic import Generic, instance_to_dict
from src.kafka_logger import logging
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer

def delivery_report(err, msg):

    if err is not None:
        logging.info("Delivery failed for User record {}: {}".format(msg.key(), err))
        return
    logging.info('User record {} successfully produced to {} [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))

def produce_data(topic:str, file_path:str,schema_path:str):
    logging.info(f"Topic: {topic} file_path:{file_path}")
    schema_str = Generic.get_schema(schema_path)
    schema_registry_conf = schema_config()
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)
    string_serializer = StringSerializer("utf-8")
    json_serializer = JSONSerializer(schema_str, schema_registry_client, instance_to_dict)
    producer = Producer(sasl_config())

    print(f"Producing user data for Topic-{topic}")
    producer.poll(1.0)

    try:
        c = 0
        s3Client = Generic.s3_obj()
        for instance in Generic.get_object(file_path,s3Client):
            logging.info(f"Topic: {topic} file_path:{instance.to_dict()}")
            producer.produce(topic=topic,
                             key=string_serializer(str(uuid4()), instance.to_dict()),
                             value=json_serializer(instance, SerializationContext(topic, MessageField.VALUE)),
                             on_delivery=delivery_report
                             )
            if c % 10 == 0:
                print(instance.to_dict())
                print("Producer Flushing...")
                producer.flush()
                time.sleep(2)


    except KeyboardInterrupt as e:
        logging.info(e)




