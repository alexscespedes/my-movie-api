import datetime
from fastapi import FastAPI, Path, Query
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse,JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title = "My Application with FastAPI"
app.version = "0.0.1"

class Movie(BaseModel):
            id: Optional[int] = None
            title: str = Field(min_Length=5, max_Length=15)
            overview: str = Field(min_Length=15, max_Length=45)
            year: int = Field(le=datetime.date.today().year)
            rating: float = Field(ge=1, le=10)
            category: str = Field(min_length=3, max_length=10)

            model_config = {
                "json_schema_extra": {
                    "examples": [{
                        "id": 1,
                        "title": "Mi Pelicula",
                        "overview": "Descripcion de la pelicula",
                        "year": 2022,
                        "rating": 9.9,
                        "category": "Acción"
                        }]
                }
            }


movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': 2009,
        'rating': 7.8,
        'category': 'test'    
    } ,

        {
        'id': 2,
        'title': 'Black widow',
        'overview': "Natasha Romanoff confronts the darker parts of her ledger when a dangerous conspiracy with ties to her past arises.",
        'year': 2021,
        'rating': 6.7,
        'category': 'Aventura'    
    } 
]


@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Welcome to movies</h1>')



@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200)
def get_movies() -> List[Movie] :
    return JSONResponse(content=movies)

@app.get('/movies/{id}', tags=['MoviesID'], response_model=Movie)
def get_movies(id: int = Path(ge=1, le=500)) -> Movie:
    for item in movies:
        if item['id'] == id:
            return JSONResponse(status_code=200, content=item)
    raise HTTPException(status_code=404, detail="Movie not found")


@app.get('/movies/', tags=['filterMovies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    data = [movie for movie in movies if movie['category'] == category]
    return JSONResponse(content=data)


@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(status_code=201, content={"message":"Successfully added"})

@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id:int, movie: Movie) -> dict:
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return JSONResponse(status_code=200, content={"message":"Successfully modified"})
    raise HTTPException(status_code=404, detail="Movie not found")

@app.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
            return JSONResponse(status_code=200, content={"message":"Successfully deleted"})
    raise HTTPException(status_code=404, detail="Movie not found")