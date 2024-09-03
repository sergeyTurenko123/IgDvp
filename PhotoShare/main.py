from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis


from src.routes import photos, users, cloudinary, comments, auth
from src.conf.config import config

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
# app.include_router(tags.router, prefix='/api')
app.include_router(photos.router, prefix='/api')
app.include_router(users.router, prefix='/api')
app.include_router(cloudinary.router, prefix='/api')
app.include_router(comments.router, prefix='/api')

# @app.on_event("startup")
# @asynccontextmanager
async def startup():
    r = await redis.Redis(
        host=config.REDIS_DOMAIN,
        port=config.REDIS_PORT,
        db=0,
        password=config.REDIS_PASSWORD,
    )
    await FastAPILimiter.init(r)





@app.get("/")
def read_root():
    return {"message": "Hello World"}

