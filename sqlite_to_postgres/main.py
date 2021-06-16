import os
import uuid

from moviesbd import MoviesDB
from transformdb import TransformDB, PersonRole, GenreName, FilmWork
from postgresdb import PostgresDB

FINAL_DBS = ['person', 'genre', 'film_work', 'film_work_person', 'film_work_genre']
PERSONS_ROLE = []
GENRE_NAME = []
FILM_WORK = []


def run():
    movies_db = MoviesDB('db.sqlite')
    transform_bd = TransformDB()
    postgres_db = PostgresDB()

    movie_table = movies_db.get_movie_table()
    for row_movies in movie_table:
        film_work_id = uuid.uuid4()
        for director_name in movies_db.make_director_to_list(row_movies[5]):
            PERSONS_ROLE.append(PersonRole(film_work_id, director_name, "director"))
        for director_name in movies_db.make_actors_names_to_list(row_movies[6]):
            PERSONS_ROLE.append(PersonRole(film_work_id, director_name, "actor"))
        for director_name in movies_db.make_writers_names_to_list(row_movies[7],
                                                                  movies_db.make_writers_to_list(row_movies[8])):
            PERSONS_ROLE.append(PersonRole(film_work_id, director_name, "writer"))
        for genre in row_movies[2].split(', '):
            GENRE_NAME.append(GenreName(film_work_id, genre))

        FILM_WORK.append(
            FilmWork(film_work_id, movies_db.get_text(row_movies[3]),
                     movies_db.get_text(row_movies[4]),
                     movies_db.make_imdb_rating_float(row_movies[1])))

    transform_bd.transfer_bd_to_csv(PERSONS_ROLE, GENRE_NAME, FILM_WORK)

    for db in FINAL_DBS:
        postgres_db.copy_db_from_csv(db)


if __name__ == '__main__':
    os.environ['DB_NAME'] = 'postgres'
    os.environ['DB_USER'] = 'postgres'
    os.environ['DB_HOST'] = 'localhost'
    os.environ['DB_PORT'] = '5432'
    os.environ['DB_OPTIONS'] = '-c search_path=content'
    os.environ['DB_PASSWORD'] = 'postgres'
    os.environ['DB_SECRET_KEY'] = '5bim(!=4f(8m=w6&k%sr)nptmap(cmterf5dojs$ogh)wg879s'
    run()
