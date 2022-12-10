import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TypeFilm(models.TextChoices):
        MOVIE = 'movie', (_('movie'))
        TV_SHOW = 'tv_show', (_('tv_show'))


class Role(models.TextChoices):
        ACTOR = 'actor', (_('actor'))
        WRITER = 'writer', (_('writer'))
        DIRECTOR = 'director', (_('director'))


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Filmwork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation_date'), blank=True)
    rating = models.FloatField(
        _('rating'), validators=[MinValueValidator(0), MaxValueValidator(100)]
        )
    type_film = models.CharField(
        _('type'), max_length=255, choices=TypeFilm.choices, db_column='type'
        )
    genres = models.ManyToManyField('Genre', through='GenreFilmwork')
    persons = models.ManyToManyField('Person', through='PersonFilmwork')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('film_production')
        verbose_name_plural = _('film_productions')
        indexes = [
            models.Index(
                fields=['creation_date'], name='film_work_creation_date_idx'
                ),
        ]


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        unique_together = ['film_work', 'genre']


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full_name'), max_length=255)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('participant')
        verbose_name_plural = _('participants')


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(_('role'), null=True, choices=Role.choices)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        unique_together = ['film_work', 'person', 'role']
