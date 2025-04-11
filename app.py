from flask import Flask, request
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from mobile app

# MongoDB connection
client = MongoClient("mongodb+srv://krishnabk0803:keshika0803@cluster0.5jw6k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["database"]
collection = db["collection"]

@app.route("/")
def home():
    return "Bus Location API Running"

@app.route("/update_location", methods=["POST"])
def update_location():
    data = request.json
    print("Received:", data)

    # Save to MongoDB
    collection.update_one(
        {"bus_name": data["bus_name"]},
        {"$set": {"lat": data["lat"], "lng": data["lng"]}},
        upsert=True
    )
    return {"message": "Location updated"}, 200

@app.route("/get_location/<bus_name>", methods=["GET"])
def get_location(bus_name):
    result = collection.find_one({"bus_name": bus_name}, {"_id": 0})
    if result:
        return result
    else:
        return {"message": "Bus not found"}, 404

if __name__ == '__main__':
    app.run(debug=True)
