from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import photos, tags, users, auth, cloudinary

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix='/api')
app.include_router(tags.router, prefix='/api')
app.include_router(photos.router, prefix='/api')
app.include_router(users.router, prefix='/api')
app.include_router(cloudinary.router, prefix='/api')

@app.get("/")
def read_root():
    return {"message": "Hello World"}

