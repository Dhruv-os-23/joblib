from flask import Flask, request, jsonify
import requests
import joblib
from io import BytesIO
import pandas as pd

app = Flask(__name__)

loaded_model = joblib.load("model.joblib")

@app.route('/')
def hello():
    return "Hello! Welcome to my Flask app."

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    FeedData = data["FeedData"]
    image_url = data.get("image_url", None)

    feature_names = [
        "% Iron Feed",
        "% Silica Feed",
        "Starch Flow",
        "Amina Flow",
        "Ore Pulp Flow",
        "Ore Pulp pH",
        "Ore Pulp Density",
    ]
    df = pd.DataFrame(FeedData, columns=feature_names)

    predictions = loaded_model.predict(df)

    return jsonify({
        "feed_data": FeedData,
        "predictions": predictions.tolist(),
    })

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
        )
