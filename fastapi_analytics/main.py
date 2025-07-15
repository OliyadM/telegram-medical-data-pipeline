# fastapi_analytics/main.py
from fastapi import FastAPI, HTTPException
from typing import List
from fastapi_analytics import crud, schemas

app = FastAPI()

@app.get("/api/reports/top-products", response_model=List[schemas.TopProduct])
def top_products(limit: int = 10):
    try:
        return crud.get_top_products(limit)
    except Exception as e:
        print(f"ERROR in top_products: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/api/channels/{channel_name}/activity", response_model=schemas.ChannelActivity)
def channel_activity(channel_name: str):
    try:
        result = crud.get_channel_activity(channel_name)
        if not result:
            raise HTTPException(status_code=404, detail="Channel not found")
        return result
    except Exception as e:
        print(f"ERROR in channel_activity: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/api/search/messages", response_model=List[schemas.MessageSearchResult])
def search_messages(query: str):
    try:
        return crud.search_messages(query)
    except Exception as e:
        print(f"ERROR in search_messages: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
