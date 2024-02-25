# producer.py

from confluent_kafka import Producer

# Configure the Kafka producer
p = Producer({'bootstrap.servers': 'localhost:9092'})

# Function to send user behavior data to Kafka
def send_user_behavior(user_id, behavior):
    # The topic to send the data to
    topic = 'user_behavior'
    # The data to send
    data = {'user_id': user_id, 'behavior': behavior}
    # Send the data
    p.produce(topic, value=data)