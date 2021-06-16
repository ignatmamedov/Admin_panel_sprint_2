import csv
import uuid
from dataclasses import dataclass, field, asdict


@dataclass
class Person:
    name: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class PersonRole:
    film_work_id: uuid.UUID
    name: str
    role: str


@dataclass
class FilmWorkPerson:
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class GenreName:
    film_work_id: uuid.UUID
    name: str


@dataclass
class Genre:
    name: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class FilmWorkGenre:
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class FilmWork:
    id: str
    title: str
    description: str
    rating: float


class TransformDB:
    def __init__(self,
                 film_work_list=None,
                 film_work_genre_list=None,
                 film_work_person_list=None,
                 genres_list=None,
                 person_list=None):

        self.film_work_list = film_work_list
        self.film_work_genre_list = film_work_genre_list
        self.film_work_person_list = film_work_person_list
        self.genres_list = genres_list
        self.person_list = person_list

    def get_uuid(self, named_list):
        name_to_uuid = {}
        for name in named_list:
            name_to_uuid.update({name.name: name.id})
        return name_to_uuid

    def get_person_list(self, persons_list):
        unique_persons = set([person.name for person in persons_list])
        self.person_list = [Person(person_name) for person_name in unique_persons]
        return self.person_list

    def get_film_work_person_list(self, persons_list):
        person_uuid = self.get_uuid(self.person_list)
        self.film_work_person_list = [FilmWorkPerson(person.film_work_id, person_uuid.get(person.name), person.role) for person in persons_list]
        return self.film_work_person_list

    def get_genres_list(self, genres_list):
        unique_genres = set([genre.name for genre in genres_list])
        self.genres_list = [Genre(genre_name) for genre_name in unique_genres]
        return self.genres_list

    def get_film_work_genre_list(self, genres_list):
        genre_uuid = self.get_uuid(self.genres_list)
        self.film_work_genre_list = [FilmWorkGenre(genre.film_work_id, genre_uuid.get(genre.name)) for genre in genres_list]
        return self.film_work_genre_list

    def prep_for_migration(self, persons_role, genre_name, film_work_list):
        self.get_person_list(persons_role)
        self.get_film_work_person_list(persons_role)
        self.get_genres_list(genre_name)
        self.get_film_work_genre_list(genre_name)
        self.film_work_list = film_work_list

    @staticmethod
    def write_to_csv(filename, columns, table):
        csv_table = [asdict(row) for row in table]
        with open(filename, "w", newline="", encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=columns, delimiter="|")
            writer.writeheader()
            writer.writerows(csv_table)

    def transfer_bd_to_csv(self, persons_role, genre_name, film_work_list):
        self.prep_for_migration(persons_role, genre_name, film_work_list)

        columns = ["id", "title", "description", "rating"]
        self.write_to_csv('film_work.csv', columns, self.film_work_list)

        columns = ["id", "film_work_id", "genre_id"]
        self.write_to_csv('film_work_genre.csv', columns, self.film_work_genre_list)

        columns = ["id", "film_work_id", "person_id", "role"]
        self.write_to_csv('film_work_person.csv', columns, self.film_work_person_list)

        columns = ["id", "name"]
        self.write_to_csv('genre.csv', columns, self.genres_list)

        columns = ["id", "name"]
        self.write_to_csv('person.csv', columns, self.person_list)


