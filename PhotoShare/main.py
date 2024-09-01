from fastapi import FastAPI

from src.routes import photo, tags, user, auth, comments

app = FastAPI()

app.include_router(auth.router, prefix='/api')
app.include_router(tags.router, prefix='/api')
app.include_router(photo.router, prefix='/api')
app.include_router(user.router, prefix='/api')
app.include_router(comments.router, prefix='/api')


@app.get("/")
def read_root():
    return {"message": "Hello World"}

