import logging
from fastapi import FastAPI, Query
from src import MovieInput, MovieResponse

app = FastAPI(title="Movie API")


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
datefmt="%H:%M:%S")

logger = logging.getLogger(__name__)

movies = {
    1: {"id":1, "title": "Movie A", "release_year": 2020},
    2: {"id":2, "title": "Movie B", "release_year": 2021}
}
@app.get("/movies", response_model=list[MovieResponse])
def list_movies(limit: int = Query(default=2, ge=1)):
    records = list(movies.values())
    result = records[:limit]
    logger.info(f"Returned {len(result)} movies")
    return result


@app.post("/movies", response_model=MovieResponse)
def add_movie(movie: MovieInput):
    movie_id = len(movies) + 1
    record = movie.model_dump()
    record["id"] = movie_id
    movies[movie_id] = record
    logger.info(f"Movie added, ID:{movie_id}")
    return record

@app.get("/health")
def health_check():
    return{"status": "ok"}

@app.get("/demo/movies/{movie_id}")
def demo_get_movie(movie_id: int):
    return {"requested_id": movie_id}

@app.get("/demo/movies")
def demo_list_movies(limit: int = Query(default= 2, ge=1)):
    return{"requested_limit": limit}

@app.post("/demo/movies")
def demo_add_movie(movie: MovieInput):
    return movie.model_dump()

demo_movie_examples = []


@app.post("/demo/movie-examples", response_model=MovieResponse)
def demo_add_movie_example(movie: MovieInput):
    movie_id = len(demo_movie_examples) + 1
    record = movie.model_dump()
    record["id"] = movie_id
    demo_movie_examples.append(record)
    return record