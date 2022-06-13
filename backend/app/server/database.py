import motor.motor_asyncio
from bson.objectid import ObjectId
from bson import json_util
import json

MONGO_DETAILS = "mongodb+srv://rss_feed:rss_feed@cluster0.46sfz.mongodb.net/?retryWrites=true&w=majority"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.rss_feed

word_collection = database.get_collection("rss_feed_write")

def word_helper(word) -> dict:
    # word = json.dumps(word, indent=4, default=json_util.default)
    return {
        "id": str(word["_id"]),
        "word": word["word"],
        "count": int(word["count"]),
        "date": int(word["date"])
    }
    
async def retrieve_word():
    words = []
    async for word in word_collection.find():
        if int(word['count']) > 3:
            words.append(word_helper(word))
        # words.append(word["article_title"])
    return words

# Add a new word into to the database
async def add_word(word_data: dict) -> dict:
    word = await word_collection.insert_one(word_data)
    new_word = await word_collection.find_one({"_id": word.inserted_id})
    return word_helper(new_word)