import os
import uvicorn
import threading
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

# የ Cron Job ስህተትን ለመፍታት በጣም አጭር ምላሽ ("OK") ብቻ ይመልሳል


@app.get("/ping", response_class=PlainTextResponse)
async def ping():
    return "OK"


@app.get("/")
async def root():
    return {"message": "Bot Web Server is Running"}


def run():
    port = int(os.environ.get("PORT", 8000))
    # log_level="error" ማድረጋችን የሰርቨሩን ሎግ እንዳያጨናንቅ ይረዳናል
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="error")


def keep_alive():
    t = threading.Thread(target=run)
    t.start()
