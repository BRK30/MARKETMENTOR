from flask import Flask, jsonify, send_from_directory
from prediction_model import predict_stock
import os

app = Flask(__name__)

# Frontend folder is one level above backend
FRONTEND_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "frontend")
)


@app.route("/")
def home():
    return send_from_directory(FRONTEND_FOLDER, "index.html")


@app.route("/portfolio.html")
def portfolio():
    return send_from_directory(FRONTEND_FOLDER, "portfolio.html")


@app.route("/compare.html")
def compare():
    return send_from_directory(FRONTEND_FOLDER, "compare.html")


@app.route("/prediction.html")
def prediction_page():
    return send_from_directory(FRONTEND_FOLDER, "prediction.html")


@app.route("/api/prediction/<symbol>")
def prediction(symbol):
    result = predict_stock(symbol)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)