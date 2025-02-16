from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from .notification import router, get_subscriptions

templates = Jinja2Templates(directory="templates")


@router.get("/health")
def read_health():
    return {"status": "ok"}


@router.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    id = 1412  # Set a unique ID for each user
    subscription = get_subscriptions(id)
    is_subscribed = subscription is not None and subscription.get(
        "active", False)
    return templates.TemplateResponse("index.html", {"request": request, "title": "Home", "is_subscribed": is_subscribed})
