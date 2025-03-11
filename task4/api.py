import json

import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

import parser_script as parser
import database as db


app = FastAPI()

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

@app.get("/parse")
def parse(url):
    try:
        data = parser.parse_3_pages(url)
        # cars = [db.Car(**entry) for entry in data]
        # db.save_to_db([car.model_dump() for car in cars])
        db.save_to_db(data)

        return {"message": "Parsed successfully", "url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while parsing: {e}")

@app.get("/get_data")
def get():
    try:
        data = db.get_all_from_db()
        df = pd.DataFrame(data)
        df.to_csv('cars.csv', index=False)
        print("Data saved to cars.csv")
        return {"message": "Data loaded successfully"}
    except Exception as e:
        raise Exception(e) 
    

if __name__ == "main":
    uvicorn.run(app, host="0.0.0.0", port=8000)
