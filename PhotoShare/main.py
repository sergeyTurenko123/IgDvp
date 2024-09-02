import logging
from fastapi import FastAPI
#from .roles import router as roles_router

from src.routes import auth
from src.routes import photos
from src.routes import tags
from src.routes import users


logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

app.include_router(auth.router, prefix='/api')
app.include_router(tags.router, prefix='/api')
app.include_router(photos.router, prefix='/api')
app.include_router(users.router, prefix='/api')

@app.get("/")
def read_root():
    return {"message": "Hello World"}

