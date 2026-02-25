from fastapi import FastAPI
import random

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Retail AI API running"}

@app.get("/risk")
def get_risk():
    score = random.uniform(0, 1)
    return {"behavior_score": score}
