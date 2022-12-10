from django.contrib import admin

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)
    list_display = ('title', 'type_film', 'creation_date', 'rating',)
    list_filter = ('type_film', 'creation_date',)
    search_fields = ('title', 'description', 'id',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
    search_fields = ('full_name', 'id',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    search_fields = ('name', 'description', 'id')
