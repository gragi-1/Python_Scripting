# consumer.py

from confluent_kafka import Consumer
from sklearn.externals import joblib

# Load your trained machine learning model
model = joblib.load('model.pkl')

# Configure the Kafka consumer
c = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
})

# Subscribe to the 'user_behavior' topic
c.subscribe(['user_behavior'])

# Function to generate recommendations based on user behavior
def generate_recommendations():
    while True:
        # Receive user behavior data from Kafka
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue

        # Get the user behavior data
        data = msg.value()

        # Generate recommendations using your machine learning model
        recommendations = model.predict(data['behavior'])

        # Send the recommendations back to your website or app
        send_recommendations(data['user_id'], recommendations)