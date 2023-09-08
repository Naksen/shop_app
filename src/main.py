from fastapi import FastAPI
from item.router import router as router_items

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(router_items)