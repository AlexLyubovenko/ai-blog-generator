from fastapi import FastAPI
import uvicorn
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Debug API Works!"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/telegram-test")
def telegram_test():
    return {"status": "test", "message": "Telegram test endpoint works"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)