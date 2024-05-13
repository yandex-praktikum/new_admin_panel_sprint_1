import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class FilmType(models.TextChoices):
    movie = "movie", _("Movie")
    tv_show = "tv_show", _("TV-Show")


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(_("created"), auto_now_add=True)
    modified = models.DateTimeField(_("modified"), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True)

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_("full_name"), max_length=255, blank=False)

    class Meta:
        db_table = 'content"."person'
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")

    def __str__(self):
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    creation_date = models.DateField(_("creation_date"))
    rating = models.FloatField(
        _("rating"),
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    type = models.CharField(_("type"), max_length=7, choices=FilmType.choices, blank=False)
    genres = models.ManyToManyField(Genre, through="GenreFilmwork")
    persons = models.ManyToManyField(Person, through="PersonFilmwork")
    certificate = models.CharField(_("certificate"), max_length=512, blank=True)
    # Параметр upload_to указывает, в какой подпапке
    # будут храниться загружемые файлы.
    # Базовая папка указана в файле настроек как MEDIA_ROOT
    file_path = models.FileField(_("file"), blank=True, null=True, upload_to="movies/")

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _("Filmwork")
        verbose_name_plural = _("Filmworks")
        indexes = [
            models.Index(fields=["creation_date"], name="film_work_creation_date_idx"),
        ]

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey("Filmwork", on_delete=models.CASCADE, verbose_name=_("filmwork"))
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE, verbose_name=_("genre"))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        unique_together = [["film_work", "genre"]]

    def __str__(self):
        return self.genre.name


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey("Filmwork", on_delete=models.CASCADE, verbose_name=_("filmwork"))
    person = models.ForeignKey("Person", on_delete=models.CASCADE, verbose_name=_("person"))
    role = models.TextField(_("role"))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        unique_together = [["film_work", "person", "role"]]

    def __str__(self):
        return self.film_work.title
