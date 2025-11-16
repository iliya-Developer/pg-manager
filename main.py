from fastapi import FastAPI
from api import router
import uvicorn
from bot import start_bot
import threading

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    threading.Thread(target=start_bot).start()
    uvicorn.run("main:app", host="0.0.0.0", port=9000)