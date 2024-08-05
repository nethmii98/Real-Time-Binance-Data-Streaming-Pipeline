# Real-Time-Binance-Data-Streaming-Pipeline
## What is Binance?
Binance is a leading cryptocurrency exchange platform where you can trade a wide range of cryptocurrencies. Binance provides a WebSocket API that allows you to receive real-time updates on market data, such as price changes and trading volume.

## What is WebSocket?
WebSockets are a protocol for full-duplex communication channels over a single TCP connection. Unlike HTTP, which operates on a request-response model, WebSockets enable continuous, real-time communication between a client (such as a Python script) and a server (such as Binance's WebSocket server). This is particularly beneficial for applications requiring live updates, such as trading platforms or data feeds.

## Download and Install Kafka on EC2
### Create an EC2 Instance
1. Launch an instance in Amazon EC2 (select Amazon Linux as the environment and create a key pair).
2. Save the downloaded key pair in a secure folder on your local machine.
3. Open a terminal and navigate to the folder containing the key pair.

### Connect to EC2 Instance

Connect to your EC2 instance using an SSH client with the following command:

```
ssh -i "your-key-pair.pem" ec2-user@<YOUR_PUBLIC_IP>
```

### Install Kafka

1. Download Kafka:

```
wget https://downloads.apache.org/kafka/3.7.0/kafka_2.13-3.7.0.tgz
```

2. Extract Kafka:

```
tar -xvf kafka_2.13-3.7.0.tgz
```

3. Verify Java Installation:

```
java -version
```

4. Install Java (if not already installed):

```
sudo yum install java-1.8.0-amazon-corretto.x86_64
```

5. Navigate to Kafka Directory:

```
cd kafka_2.13-3.7.0
```

## Start Zookeeper and Kafka Server

1. Start Zookeeper:

```
bin/zookeeper-server-start.sh config/zookeeper.properties
```

2. Start Kafka Server:

```
bin/kafka-server-start.sh config/server.properties
```

## Configure Kafka for Public IP

1. Edit server.properties:

```
sudo nano config/server.properties
```

2. Change ADVERTISED_LISTENERS to the public IP of your EC2 instance:

```
advertised.listeners=PLAINTEXT://<YOUR_PUBLIC_IP>:9092
```

## Create Kafka Topics

1. Create Topics:

```
bin/kafka-topics.sh --create --topic binance_data --bootstrap-server <YOUR_PUBLIC_IP>:9092 --replication-factor 1 --partitions 1
```

## Start Kafka Producer and Consumer

1. Start Producer:

```
bin/kafka-console-producer.sh --topic binance_data --bootstrap-server <YOUR_PUBLIC_IP>:9092

```

2. Start Consumer:

```
bin/kafka-console-consumer.sh --topic binance_data --bootstrap-server <YOUR_PUBLIC_IP>:9092

```

## Integrate with AWS S3 and Athena
### Create an S3 Bucket:

Create an S3 bucket via the AWS Management Console.
Provide the bucket path in the kafkaConsumer.py script to store Binance data in JSON format.

### Configure AWS on Your Local Machine:

Install AWS CLI and configure it with your credentials.

### Set Up AWS Glue Crawler:

Create an AWS Glue Crawler to automatically catalog the data in your S3 bucket.
Configure it to upload data to Athena from the S3 bucket.
Ensure that the IAM Role has the necessary permissions to access Glue, S3, and Athena. Assign administrator access when creating the IAM Role.

### Run the Scripts:

Start your EC2 instance and ensure Zookeeper and Kafka are running.
Execute kafkaProducer.py and kafkaConsumer.py scripts.
Refresh your S3 bucket to see the received data.
Refresh Athena to query the ingested data.

## Install Required Python Packages
pip install websocket-client
pip install kafka-python
pip install s3fs

## Notes
Replace <YOUR_PUBLIC_IP> with the actual public IP address of your EC2 instance.
Ensure network security groups and firewall rules allow traffic on port 9092.
