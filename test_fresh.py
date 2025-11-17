from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Fresh start - OK"}

@app.get("/telegram-test")
def telegram_test():
    return {"status": "fresh_test_works"}

if __name__ == "__main__":
    print("🚀 Starting fresh test server...")
    uvicorn.run(app, host="0.0.0.0", port=8003, log_level="info")