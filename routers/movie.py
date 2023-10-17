from fastapi import APIRouter
from fastapi import Path, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.movies import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from service.movie import MovieService
from schemas.movie import Movie

router = APIRouter()

@router.get("/movies", tags=['Movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@router.get("/movies/{movie_id}", tags=['Movies'], response_model=Movie)
def get_movie_by_id(movie_id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(movie_id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})
    
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
    # movie = movies[movie_id - 1]
    return JSONResponse(status_code=404, content=[])

@router.get('/movies/', tags=['Movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_Length=5, max_Length=15)) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies_by_category(category)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
    # movie_list = []
    # for item in movies:
    #     if item['category'] == category:
    #         movie_list.append(item)
    # return movie_list

@router.post('/movies', tags=['Movies'], response_model=dict, status_code=201)
def create_movies(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201, content={"message": "Movie created successfully"})

# async def cretate_movie(request: Request):
#     movie = await request.json()
#     movies.append(movie)
#     return movie

@router.put('/movies/{movie_id}', tags=['Movies'], response_model=dict, status_code=200)
def update_movie(movie_id: int, movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).get_movie(movie_id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})
    
    MovieService(db).update_movie(movie_id, movie)
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

@router.delete('/movies/{movie_id}', tags=['Movies'], response_model=dict, status_code=200)
def delete_movie(movie_id: int) -> dict:
    db = Session()
    result: MovieModel = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})
    MovieService(db).delete_movie(movie_id)
    return JSONResponse(status_code=200, content={"message": "Movie deleted successfully"})

