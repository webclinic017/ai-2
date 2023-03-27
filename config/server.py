import dotenv
from fastapi import FastAPI
from mangum import Mangum
from api.v1.router import router as api_router

from config.database import shutdown_database, startup_database
from utilities.n3d1117_chatgpt_telegram_bot_bot.main import (
    main as chat_gpt_telegram_bot,
)

# Telegram Bot
dotenv.load_dotenv("config/.env")
chat_gpt_telegram_bot()

# FastAPI Server
app = FastAPI()


@app.on_event("startup")
async def startup_event():
    print("app is starting up")
    await startup_database(app)


@app.on_event("shutdown")
async def shutdown_event():
    print("app is shutting down")
    await shutdown_database(app)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(api_router, prefix="/api/v1")
handler = Mangum(app, lifespan="off")
