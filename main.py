from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()

MONGO_URI = "mongodb+srv://asifm8702_db_user:4OLDtBQysg6veCf3@cluster0.jp2smkd.mongodb.net/prankVideos?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)

db = client["prankVideos"]
collection = db["videos"]

@app.get("/videos")
def get_videos():

    documents = collection.find(
        {},
        {"_id": 0}  # Don't return MongoDB's internal _id
    )

    videos = list(documents)

    return {
        "videos": videos
    }