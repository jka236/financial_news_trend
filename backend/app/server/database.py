import motor.motor_asyncio
from bson.objectid import ObjectId
from bson import json_util
import json
import spacy
import os
from dotenv import load_dotenv
from os.path import join, dirname
import datetime

nlp = spacy.load("en_core_web_sm")

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGO_DETAILS = os.environ.get("MONGO_DETAILS")

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
    
async def retrieve_noun():
    words = []
    print(MONGO_DETAILS)
    async for word in word_collection.find():
        doc = nlp(word['word'])
        if int(word['count']) > 3 and doc[0].tag_ == 'NNP':
            words.append(word_helper(word))
    return words

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

# Add a new word into to the database
async def delete_old_word() -> None:
    print("Clean up start...")
    epoch_day = (datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).days -7
    word = await word_collection.delete_many({'date': {'$lt': epoch_day}})
    return