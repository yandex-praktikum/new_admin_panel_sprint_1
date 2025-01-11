from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator

class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Этот параметр указывает Django, что этот класс не является представлением таблицы
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

class Genre(UUIDMixin, TimeStampedMixin):
    # Типичная модель в Django использует число в качестве id. В таких ситуациях поле не описывается в модели.
    # Вам же придётся явно объявить primary key.
    # Первым аргументом обычно идёт человекочитаемое название поля
    name = models.CharField(_('name'), max_length=255) # перевод _('') name
    # blank=True делает поле необязательным для заполнения.
    description = models.TextField(_('description'), blank=True, null=True)
    # auto_now_add автоматически выставит дату создания записи 

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "content\".\"genre"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

class Filmwork(UUIDMixin, TimeStampedMixin):
    # Выбор жанра TextChoices movie, tv show, soap_opera, cartoon
    class Type(models.TextChoices):
        movie = ('movie', _('Фильм')) # Перевод Фильм
        tv_show = ('tv_show', _('Шоу')) # Перевод Тв Шоу
        soap_opera  = ('soap_opera', _('Сериал'))   # перевод Сериал
        cartoon = ('cartoon', _('Мультфильм'))  # перевод Мультфильм
    type = models.CharField(_('type'),
        max_length=10,
        choices=Type.choices,
        default=Type.movie
    ) 
    title = models.CharField(_('title'), max_length=255) 
    # Описание Фильма
    description = models.TextField(_('description'), blank=True, null=True)
    # Поле для хранения даты создания фильма
    creation_date = models.DateField(_('Дата создания'),  blank=True, null=True)
    # Выбор рейтинга от 0 до 100, по умолчанию равен 0
    rating = models.FloatField(_('rating'), blank=True, null=True, default=0,
             validators=[MinValueValidator(0),
             MaxValueValidator(100)])

    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "content\".\"film_work"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Кинопроизведение'
        verbose_name_plural = 'Кинопроизведения'


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"


class Person(UUIDMixin, TimeStampedMixin):
    full_name =  models.TextField(_('full_name'), blank=True) # перевод full_name
    persons  = models.ManyToManyField('Person', through='PersonFilmwork')
    class Meta:
        db_table = "content\".\"person"
    # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Участника'
        verbose_name_plural = 'Участники Кинопроизведения'



class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.CharField(_('role'), max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"

