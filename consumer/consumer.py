from kafka import KafkaConsumer
import json
import os

# Kafka configuration
kafka_topic = "scrape"
kafka_server = os.getenv('KAFKA_SERVER', 'kafka:9093')

# Initialize Kafka consumer
consumer = KafkaConsumer(
    kafka_topic,
    bootstrap_servers=[kafka_server],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print(f"Connected to Kafka server at {kafka_server}, consuming from topic: {kafka_topic}")

data_list = []

# Check if the directory exists
os.makedirs('/data', exist_ok=True)

# Consume messages and save them to a file
try:
    for message in consumer:
        print(f"Received message: {message.value}")
        data_list.append(message.value)
        with open('/data/outputfile.json', 'w') as f:
            json.dump(data_list, f)
except Exception as e:
    print(f"Unexpected event occurred while consuming data from Kafka: {e}")
finally:
    consumer.close()
