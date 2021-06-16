import random
import factory
from . import models
from factory.fuzzy import FuzzyChoice, FuzzyInteger


class RandomFilmworkType(FuzzyChoice):
    def fuzz(self):
        if self.choices is None:
            self.choices = list(self.choices_generator)
        value = random.choices(self.choices, [6, 1])[0]
        if self.getter is None:
            return value
        return self.getter(value)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    id = factory.Faker('uuid4')
    email = factory.Faker('email')
    username = factory.Faker('user_name')
    password = factory.Faker('password')


class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Genre

    id = factory.Faker('uuid4')
    name = factory.Faker('word')
    description = factory.Faker('text')


class PersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Person

    id = factory.Faker('uuid4')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class FilmworkGenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.FilmworkGenre

    id = factory.Faker('uuid4')
    genre_id = factory.Faker('uuid4')
    filmwork_id = factory.Faker('uuid4')


class FilmworkPesrsonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.FilmworkPerson

    id = factory.Faker('uuid4')
    person_id = factory.Faker('uuid4')
    filmwork_id = factory.Faker('uuid4')
    role = FuzzyChoice(models.ProfessionType)


class FilmworkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Filmwork

    id = factory.Faker('uuid4')
    type = RandomFilmworkType(models.FilmworkType)
    title = factory.Faker('word')
    description = factory.Faker('text')
    creation_date = factory.Faker('date')
    age_rating = FuzzyInteger(0, 21)
    link = factory.Faker('url')


def generate_content():
    UserFactory()
    for genre_num in range(10):
        genre = GenreFactory()
        for person_num in range(12):
            person = PersonFactory()
            for filmwork_num in range(10):
                filmwork = FilmworkFactory()
                FilmworkGenreFactory(genre_id=genre, filmwork_id=filmwork)
                FilmworkPesrsonFactory(person_id=person, filmwork_id=filmwork)


if __name__ == "__main__":
    for user_num in range(1000):
        generate_content()
