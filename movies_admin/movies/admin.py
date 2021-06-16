from django.contrib import admin
from .models import Genre, Person, Filmwork, User


class PersonInline(admin.TabularInline):
    model = Filmwork.persons.through
    extra = 0


class GenreInline(admin.TabularInline):
    model = Filmwork.genres.through
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'date_joined', 'is_staff')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_filter = ('first_name', 'last_name')
    list_display = ('first_name', 'last_name')
    pass


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    list_filter = ('type',)
    list_display = ('type', 'title', 'creation_date', 'age_rating',)

    inlines = [
        PersonInline,
        GenreInline
    ]

