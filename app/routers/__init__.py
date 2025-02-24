from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .notification import router

templates = Jinja2Templates(directory="templates")


@router.get("/health")
def read_health():
    return {"status": "ok"}


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Home"})
