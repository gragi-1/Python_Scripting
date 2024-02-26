# consumer.py

from confluent_kafka import Consumer
import joblib

# Load your trained machine learning model
# Make sure 'model.pkl' is in your current directory or provide the full path
model = joblib.load(r"C:\Users\Usuario\Desktop\Útiles\Proyectos\Python_Scripts\Even_more_difficult_scripts\Real-time recommendation system\model.pkl")

# Configure the Kafka consumer
c = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
})

# Subscribe to the 'user_behavior' topic
c.subscribe(['user_behavior'])

# Function to send recommendations
def send_recommendations(user_id, recommendations):
    # This is just a placeholder. Replace this with your actual implementation.
    print(f"Send recommendations {recommendations} to user {user_id}")

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

# Start generating recommendations
generate_recommendations()