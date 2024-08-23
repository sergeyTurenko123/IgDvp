from fastapi import FastAPI

from src.routes import quote, tags, author

app = FastAPI()

app.include_router(tags.router, prefix='/api')
app.include_router(quote.router, prefix='/api')
app.include_router(author.router, prefix='/api')


@app.get("/")
def read_root():
    return {"message": "Hello World"}

