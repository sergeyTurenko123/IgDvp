from fastapi import FastAPI

from PhotoShare.src.routes import photo, user
from src.routes import tags

app = FastAPI()

app.include_router(tags.router, prefix='/api')
app.include_router(photo.router, prefix='/api')
app.include_router(user.router, prefix='/api')


@app.get("/")
def read_root():
    return {"message": "Hello World"}

