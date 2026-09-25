import os

from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI(title="Prank Videos API")

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://asifm8702_db_user:4OLDtBQysg6veCf3@cluster0.jp2smkd.mongodb.net/prankVideos?retryWrites=true&w=majority",
)
PORT = int(os.getenv("PORT", "8000"))

try:
    client = MongoClient(MONGO_URI)
    db = client["prankVideos"]
    collection = db["videos"]
except Exception as exc:
    client = None
    db = None
    collection = None
    print(f"MongoDB connection error: {exc}")


@app.get("/")
def home():
    return {"message": "Prank Videos API is running"}


@app.get("/videos")
def get_videos():
    if collection is None:
        return {"videos": [], "error": "MongoDB connection not available"}

    documents = collection.find({}, {"_id": 0})
    videos = list(documents)

    return {"videos": videos}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
