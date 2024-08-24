from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.routes import photo, user
from src.routes import tags

app = FastAPI()

app.include_router(tags.router, prefix='/api')
app.include_router(photo.router, prefix='/api')
app.include_router(user.router, prefix='/api')
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"message": "Hello World"}

