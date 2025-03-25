import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

import database as db


app = FastAPI()

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

@app.get("/save_url")
def save_url(url):
    try:
        db.save_to_db(url)

        return {"message": "Url saved to database!", "url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while saving: {e}")

@app.get("/get_urls")
def get():
    try:
        data = db.get_all_from_db()
        df = pd.DataFrame(data)
        df.to_csv('urls.csv', index=False)
        print("Data saved to urls.csv")
        return {"message": "Data loaded successfully"}
    except Exception as e:
        raise Exception(e) 

if __name__ == "main":
    uvicorn.run(app, host="0.0.0.0", port=8000)
