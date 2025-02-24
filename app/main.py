from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import router

app = FastAPI()

app.include_router(router)

# Static files configuration
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
