import requests
import cloudinary
import cloudinary.uploader

from pymongo import MongoClient

MONGO_URI = "mongodb+srv://asifm8702_db_user:4OLDtBQysg6veCf3@cluster0.jp2smkd.mongodb.net/prankVideos?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)

db = client["prankVideos"]
collection = db["videos"]

cloudinary.config(
    cloud_name="dxao2uisw",
    api_key="752638974978329",
    api_secret="3DQvafVDCIdhMtse4IUgqxZ0C1E"
)

API_URL = "https://techinfortainment.com/downloader/api/v1/pranks"

response = requests.get(API_URL)
response.raise_for_status()

data = response.json()
items = data["items"]

for index, item in enumerate(items, start=1):

    video_urls = item.get("prankVideoUrl")

    if not video_urls:
        print(f"[{index}] No video: {item['id']}")
        continue

    url = video_urls

    print(f"\n[{index}/{len(items)}] {item['name']}")
    print(f"Source: {url}")

    try:

        result = cloudinary.uploader.upload(
            url,
            resource_type="video",
            folder="pranks",
            public_id=item["id"]
        )

        cloudinary_url = result["secure_url"]

        print("Uploaded!")
        print("Cloudinary URL:", cloudinary_url)

        mongo_data = item.copy()

        mongo_data["prankVideoUrl"] = cloudinary_url

        collection.update_one(
            {"id": item["id"]},
            {"$set": mongo_data},
            upsert=True
        )

        print("Saved to MongoDB!")

    except Exception as e:

        print("Upload failed:", e)


print("\nDone!")










# import requests
# import cloudinary
# import cloudinary.uploader

# cloudinary.config(
#     cloud_name="dxao2uisw",
#     api_key="752638974978329",
#     api_secret="3DQvafVDCIdhMtse4IUgqxZ0C1E"
# )

# API_URL = "https://techinfortainment.com/downloader/api/v1/pranks"

# response = requests.get(API_URL)
# response.raise_for_status()

# data = response.json()
# items = data["items"]

# print(f"Found {len(items)} items")


# for index, item in enumerate(items, start=1):

#     video_urls = item.get("prankVideoUrl")

#     if not video_urls:
#         print(f"[{index}] No video: {item['id']}")
#         continue

#     url = video_urls

#     print(f"\n[{index}/{len(items)}] {item['name']}")
#     print(f"Source: {url}")

#     try:
#         result = cloudinary.uploader.upload(
#             url,
#             resource_type="video",
#             folder="pranks"
#         )

#         print("Uploaded!")
#         print("Public ID:", result["public_id"])
#         print("Cloudinary URL:", result["secure_url"])

#     except Exception as e:
#         print("Upload failed:", e)

# print("\nDone!")













# import requests
# import os
# from urllib.parse import urlparse

# API_URL = "https://techinfortainment.com/downloader/api/v1/pranks"
# OUTPUT_DIR = "downloads"

# os.makedirs(OUTPUT_DIR, exist_ok=True)

# # Get JSON from API
# response = requests.get(API_URL)
# response.raise_for_status()

# data = response.json()

# items = data["items"]

# print(f"Found {len(items)} items to download.", items)

# for index, item in enumerate(items, start=1):
#     url = item["prankVideoUrl"]

#     filename = os.path.basename(urlparse(url).path)

#     if not filename:
#         filename = f"media_{index}"

#     filepath = os.path.join(OUTPUT_DIR, filename)

#     print(f"Downloading {index}: {url}")

#     media = requests.get(url, stream=True)
#     media.raise_for_status()

#     with open(filepath, "wb") as f:
#         for chunk in media.iter_content(chunk_size=8192):
#             f.write(chunk)

#     print(f"Saved → {filepath}")

# print("Done!")