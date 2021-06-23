import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import PermissionsMixin, Permission
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager


class FilmworkType(models.TextChoices):
    MOVIE = 'movie', _('фильм')
    TV_SHOW = 'tv_show', _('сериал')


class ProfessionType(models.TextChoices):
    DIRECTOR = 'director', _('режиссер')
    ACTOR = 'actor', _('актер')
    WRITER = 'writer', _('сценарист')


class Genre(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('название'), max_length=255)
    description = models.TextField(_('описание'), blank=True)

    class Meta:
        verbose_name = _('жанр')
        verbose_name_plural = _('жанры')

    def __str__(self):
        return self.name


class Person(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(_('имя'), max_length=255)
    last_name = models.CharField(_('фамилия'), max_length=255)

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('persons')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Filmwork(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(_('тип'), max_length=20, choices=FilmworkType.choices)
    title = models.CharField(_('заголовок'), max_length=255)
    description = models.TextField(_('содержание'), blank=True)
    creation_date = models.DateField(_('дата создания'), blank=True)
    age_rating = models.TextField(_('возрастной ценз'), blank=True)
    rating = models.FloatField(_('рейтинг'), blank=True)
    genres = models.ManyToManyField(Genre, through='FilmworkGenre')
    link = models.URLField(_('ссылка на файл'), blank=True)
    persons = models.ManyToManyField(Person, through='FilmworkPerson')

    class Meta:
        verbose_name = _('кинопроизведение')
        verbose_name_plural = _('кинопроизведения')

    def __str__(self):
        return self.title


class FilmworkPerson(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person_id = models.ForeignKey(Person, to_field='id', on_delete=models.CASCADE)
    filmwork_id = models.ForeignKey(Filmwork, to_field='id', on_delete=models.CASCADE)
    role = models.CharField(_('тип'), max_length=20, choices=ProfessionType.choices)

    class Meta:
        unique_together = ('filmwork_id', 'person_id', 'role')

class FilmworkGenre(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    genre_id = models.ForeignKey(Genre, to_field='id', on_delete=models.CASCADE)
    filmwork_id = models.ForeignKey(Filmwork, to_field='id', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('filmwork_id', 'genre_id')


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('first name'), max_length=30, blank=True)
    password = models.CharField(_('password'), max_length=128)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="user_set",
        related_query_name="user",
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
