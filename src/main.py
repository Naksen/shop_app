import logging
from fastapi import FastAPI

from item.router import router as router_items
from order.router import router as router_order
from pages.router import router as router_pages
from auth.router import router as router_user


logging.basicConfig(filename="app_log.log", level=logging.INFO)


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(router_user)
app.include_router(router_items)
app.include_router(router_order)
app.include_router(router_pages)
