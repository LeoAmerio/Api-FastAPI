from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from utils.jwt_manager import create_token
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import router as MovieRouter
from routers.user import user_router as UserRouter


app = FastAPI()
app.title = "My First API"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(MovieRouter)
app.include_router(UserRouter)

Base.metadata.create_all(bind=engine)

movies = [
    {
        "id": 1,
        "title": "My Movie Title",
        "overview": "My Movie Description",
        "year": 2022,
        "rating": 7.8,
        "category": "Action"
    }, 
    {
        "id": 2,
        "title": "My Movie Title 2",
        "overview": "My Movie Description 2",
        "year": 2023,
        "rating": 8.8,
        "category": "Comedy"
    }
]



@app.get("/", tags=['Home'])
def message():
    return HTMLResponse('<h1>Welcome to my API</h1>')



