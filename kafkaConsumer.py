from kafka import KafkaConsumer
from json import loads
import json
from s3fs import S3FileSystem

# Initialize KafkaConsumer instance
consumer = KafkaConsumer(
    'binance_data',
    bootstrap_servers=['your public IP:9092'],
    value_deserializer=lambda x: loads(x.decode('utf-8')),
    api_version=(3, 7, 0)
)

# Initialize S3FileSystem instance for interacting with Amazon S3
s3 = S3FileSystem()

# Consume messages from Kafka and write them to S3
for count, i in enumerate(consumer):
    # Define the S3 file path and name based on the message count
    file_path = "s3://kafka-binance/crypto_data_{}.json".format(count)
    
    # Open the S3 file in write mode
    with s3.open(file_path, 'w') as file:
        # Write the message value to the S3 file in JSON format
        json.dump(i.value, file)
