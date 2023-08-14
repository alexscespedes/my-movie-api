from fastapi import FastAPI, Body
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "My Application with FastAPI"
app.version = "0.0.1"

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

@app.get('/movies', tags=['movies'])
def get_movies():
    return movies

@app.get('/movies/{id}', tags=['MoviesID'])
def get_movies(id: int):
    for item in movies:
        if item['id'] == id:
            return item
    raise HTTPException(status_code=404, detail="Movie not found")


@app.get('/movies/', tags=['filterMovies'])
def get_movies_by_category(category: str):
    return [movie for movie in movies if movie['category'] == category]

@app.post('/movies', tags=['movies'])
def create_movie(id:int = Body(), title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
    movies.append(
        {
            "id": id,
            "title": title,
            "overview": overview,
            "year": year,
            "rating": rating,
            "category": category
        }
    )
    return movies

@app.put('/movies/{id}', tags=['movies'])
def update_movie(id:int, title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
    for movie in movies:
        if movie['id'] == id:
            movie['title'] = title
            movie['overview'] = overview
            movie['year'] = year
            movie['rating'] = rating
            movie['category'] = category
            return movies
    raise HTTPException(status_code=404, detail="Movie not found")

@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id: int):
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
            return movies
    raise HTTPException(status_code=404, detail="Movie not found")