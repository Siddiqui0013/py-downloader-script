import logging
import os

from fastapi import FastAPI
from pymongo import MongoClient

logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="Prank Videos API")

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://asifm8702_db_user:4OLDtBQysg6veCf3@cluster0.jp2smkd.mongodb.net/prankVideos?retryWrites=true&w=majority",
)
PORT = int(os.getenv("PORT", "8000"))

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client["prankVideos"]
    collection = db["videos"]
except Exception as exc:
    client = None
    db = None
    collection = None
    logger.warning("MongoDB connection error at startup: %s", exc)


@app.get("/")
def home():
    return {"message": "Prank Videos API is running"}


@app.get("/videos")
def get_videos():
    try:
        if collection is None:
            raise RuntimeError("MongoDB connection not available")

        documents = collection.find({}, {"_id": 0})
        videos = list(documents)
        return {"videos": videos}
    except Exception as exc:
        logger.exception("Failed to fetch videos from MongoDB")
        return {
            "videos": [],
            "error": "Could not load videos from MongoDB",
            "details": str(exc),
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
