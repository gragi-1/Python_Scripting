from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
import joblib

# Load the iris dataset
iris = load_iris()

# Train a Random Forest classifier
model = RandomForestClassifier()
model.fit(iris.data, iris.target)

# Save the trained model to disk
joblib.dump(model, 'model.pkl')