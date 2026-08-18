import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

client = AsyncIOMotorClient(MONGO_URL)

database = client.get_database(MONGO_DB_NAME)

productos_collection = database.get_collection("productos")
pedidos_collection = database.get_collection("pedidos")