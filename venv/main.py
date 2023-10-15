from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    } 
]

app = FastAPI()
app.title = "My First API"
app.version = "0.0.1"

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credentials not valid")
    
    
class User(BaseModel):
    email: str
    password: str

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5 ,max_length=15)
    overview: str = Field(min_length=15 ,max_length=50)
    year: int = Field(le=2022)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=5 ,max_length=15)
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "My Movie Title",
                    "overview": "My Movie Description",
                    "year": 2022,
                    "rating": 7.8,
                    "category": "Action"
                }
            ]
        }
    }

@app.get("/", tags=['Home'])
def message():
    return HTMLResponse('<h1>Welcome to my API</h1>')

@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token = create_token(user.dict())
        return JSONResponse(status_code=200, content={"token": token})

@app.get("/movies", tags=['Movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)

@app.get("/movies/{movie_id}", tags=['Movies'], response_model=Movie)
def get_movie_by_id(movie_id: int = Path(ge=1, le=2000)) -> Movie:
    for item in movies:
        if item['id'] == movie_id:
            return JSONResponse(content=item)
    # movie = movies[movie_id - 1]
    return JSONResponse(status_code=404, content=[])

@app.get('/movies/', tags=['Movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_Length=5, max_Length=15)) -> List[Movie]:
    data = [item for item in movies if item['category'] == category and item['year'] == year]
    return JSONResponse(content=data)
    # movie_list = []
    # for item in movies:
    #     if item['category'] == category:
    #         movie_list.append(item)
    # return movie_list

@app.post('/movies', tags=['Movies'], response_model=dict, status_code=201)
def create_movies(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(status_code=201, content={"message": "Movie created successfully"})
# async def cretate_movie(request: Request):
#     movie = await request.json()
#     movies.append(movie)
#     return movie

@app.put('/movies/{movie_id}', tags=['Movies'], response_model=dict, status_code=200)
def update_movie(movie_id: int, movie: Movie) -> dict:
    for item in  movies:
        if item['id'] == movie_id:
            item['title'] == movie.title
            item['overview'] == movie.overview
            item['year'] == movie.year
            item['rating'] == movie.rating
            item['category'] == movie.category
            
            return JSONResponse(status_code=200, content={"message": "Movie updated successfully"})

# def update_movie(movie_id: int, movie: dict = Body({
#     "id": int,
#     "title": str,
#     "overview": str,
#     "year": int,
#     "rating": float,
#     "category": str
# })):
#     for item in  movies:
#         if item['id'] == movie_id:
#             item.update(movie)
#             return item

@app.delete('/movies/{movie_id}', tags=['Movies'], response_model=dict, status_code=200)
def delete_movie(movie_id: int) -> dict:
    for item in movies:
        if item['id'] == movie_id:
            movies.remove(item)
            return JSONResponse(status_code=200, content={"message": "Movie deleted successfully"})

