from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as catalog_router
app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(
        "mongodb+srv://catalogue:catalogue12@cataloguedb.baqy2.mongodb.net/test")
    app.database = app.mongodb_client["catalog"]


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(catalog_router, tags=["catalog"], prefix="/catalog")
