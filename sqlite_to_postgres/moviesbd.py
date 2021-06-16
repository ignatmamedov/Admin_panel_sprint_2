import sqlite3
import json


class MoviesDB:
    WRITER_NAME_SQL_REQUEST = "SELECT name from writers where id is '{}'"
    REQUEST = """SELECT id, imdb_rating, genre, title, description, director, 
    group_concat(actors_names) as actors_names, writers_names, writers, '[' || group_concat(actors) || ']' as actors 
    from (
    SELECT DISTINCT movies.id, movies.genre, movies.director, writers.name as writers_names, movies.title, 
    movies.plot as description, movies.imdb_rating, movies.writers, actors, actors_names 
    from (
    SELECT movie_actors.movie_id, actors.name as actors_names, 
    ('{"id": "' || actors.id || '", "name": "'|| actors.name || '"}') as actors 
    from actors 
    JOIN movie_actors on movie_actors.actor_id = actors.id)
    Join movies on movies.id = movie_id
    LEFT JOIN writers On writers.id = movies.writer)
    WHERE 'N/A' not in (actors_names) 
    and 'N/A' not in (director)
    and 'N/A' not in (imdb_rating)
    and ('N/A' not in (writers_names) or writers_names is NULL)
    GROUP BY id
    """

    def __init__(self, db):
        self.db = db

    def send_request_to_bd(self, request):
        """
        Send any SQL request to SQLite DB.

        @param request: any SQL request
        @type request: str
        @return: List of tuples
        @rtype: list
        """
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute(request)
        request_result = cursor.fetchall()

        return request_result

    def get_movie_table(self):
        return self.send_request_to_bd(self.REQUEST)

    @staticmethod
    def make_imdb_rating_float(imdb_rating):
        if imdb_rating.upper() != 'N/A':
            return float(imdb_rating)

    @staticmethod
    def make_actors_to_list(actors):
        if actors:
            return [{"id": int(actors_dict["id"]), "name": actors_dict["name"]} for actors_dict in json.loads(actors)]
        else:
            return [{"id": None, "name": None}]

    def make_writers_to_list(self, writers):

        if not writers:
            return None

        writers_list = []
        id_list = []
        for elem in json.loads(writers):
            id_writer = elem.get("id")
            if id_writer in id_list:
                continue
            id_list.append(id_writer)
            writer = self.send_request_to_bd(self.WRITER_NAME_SQL_REQUEST.format(id_writer))
            elem = {"id": id_writer, "name": writer[0][0]}
            writers_list.append(elem)
        return writers_list

    @staticmethod
    def make_actors_names_to_list(actors_names):
        if actors_names:
            return actors_names.split(',')
        return actors_names

    @staticmethod
    def make_writers_names_to_list(writers_names, writers):
        if not writers_names:
            if writers:
                writers_names = [elem.get("name") for elem in writers]
        else:
            return [writers_names]

        return writers_names

    @staticmethod
    def make_director_to_list(director):
        if director:
            return director.split(', ')
        return director

    @staticmethod
    def get_text(text):
        if text.upper() != 'N/A':
            return text

