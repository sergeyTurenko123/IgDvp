from fastapi import FastAPI

from src.routes import photos, tags, users, auth, cloudinary

app = FastAPI()

app.include_router(auth.router, prefix='/api')
app.include_router(tags.router, prefix='/api')
app.include_router(photos.router, prefix='/api')
app.include_router(users.router, prefix='/api')
app.include_router(cloudinary.router, prefix='/api')

@app.get("/")
def read_root():
    return {"message": "Hello World"}

