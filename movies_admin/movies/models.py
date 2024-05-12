import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    """ Абстрактная модель
    Дабавляет поля с дотой и временем создания и изменения в модели
    наследующие этот класс.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    """ Абстрактная модель
    Дабавляет поля id в модели наследующие этот класс.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    """ Модель с жанрами для кинокартин."""
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Filmwork(UUIDMixin, TimeStampedMixin):
    """ Модель кинокартин."""
    class TypeChoices(models.TextChoices):
        MOVIE = 'movie', _('movie')
        TV_SHOW = 'tv show', _('tv show')

    title = models.CharField(_('title'), max_length=255,
                             null=False)
    description = models.TextField(_('description'), blank=False, null=True)
    premiere_date = models.DateField(_('premiere date'), blank=True,
                                     null=True)
    type = models.CharField(
        _('type'),
        null=False,
        max_length=10,
        choices=TypeChoices.choices,
        default=TypeChoices.MOVIE
        )
    rating = models.FloatField(_('rating'), blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)], null=True)
    file_path = models.CharField(_('file path'), max_length=255, blank=True,
                                 null=True)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')

    class Meta:
        db_table = "content\".\"filmwork"
        verbose_name = 'Кинопроизведения'
        verbose_name_plural = 'Кинопроизведения'

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    """ Модель связывает жанр с кинопроизведением"""
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = 'Жанры'
        verbose_name_plural = 'Жанры'


class Person(UUIDMixin, TimeStampedMixin):
    """ Модель с описанием персону, участника кинопроизведения """
    class Gender(models.TextChoices):
        MALE = 'male', _('male')
        FEMALE = 'female', _('female')

    full_name = models.CharField(_('full name'), max_length=255, blank=False)
    gender = models.TextField(_('gender'), choices=Gender.choices, null=True)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = 'Персонажи'
        verbose_name_plural = 'Персонажи'

    def __str__(self):
        return self.full_name


class PersonFilmwork(UUIDMixin):
    """ Модель связывает персону с кинопроизведением"""
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.CharField(_('role'), max_length=20, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = 'Учасники'
        verbose_name_plural = 'Учасники'
