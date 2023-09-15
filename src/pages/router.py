from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from item.router import get_page
from database import get_async_session

router = APIRouter(prefix="/pages", tags=["Pages"])

templates = Jinja2Templates(directory="templates")


@router.get("/base")
def get_base_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@router.get("/search/")
def get_search_page(request: Request, items=Depends(get_page)):
    return templates.TemplateResponse("search.html", {"request": request, "items": items})
