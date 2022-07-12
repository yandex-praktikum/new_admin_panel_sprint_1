import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(
        _("created"),
        auto_now_add=True
    )
    modified = models.DateTimeField(
        _("modified"),
        auto_now=True
    )

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(
        _('name'),
        max_length=255
    )
    description = models.TextField(
        _('description'),
        blank=True
    )

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('verbose_name_genre')
        verbose_name_plural = _('verbose_name_plural_genre')

    def __str__(self):
        return self.name


class Filmwork(UUIDMixin, TimeStampedMixin):
    class FilmTypes(models.TextChoices):
        movie = 'movie', _('movie')
        tv_show = 'tv_show', _('tv_show')

    title = models.CharField(
        _('title'),
        max_length=255
    )
    description = models.TextField(
        _('description'),
        blank=True
    )
    creation_date = models.DateTimeField(_('creation_date'))
    rating = models.FloatField(
        _('rating'),
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    type = models.TextField(
        _("type"),
        choices=FilmTypes.choices
    )
    genres = models.ManyToManyField(
        Genre,
        through='GenreFilmwork'
    )

    certificate = models.CharField(
        _('certificate'),
        max_length=512,
        blank=True
    )
    file_path = models.FileField(
        _('file'),
        blank=True,
        null=True,
        upload_to='movies/'
    )

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('verbose_name_film_work')
        verbose_name_plural = _('verbose_name_plural_film_work')

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(
        'Filmwork',
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.CASCADE,
        verbose_name=_("verbose_name_genre")
    )
    created = models.DateTimeField(
        _("created"),
        auto_now_add=True
    )

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('verbose_name_genre_film_work')
        verbose_name_plural = _('verbose_name_plural_genre_film_work')

    def __str__(self):
        return ""


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.TextField(_('full_name'))

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('verbose_name_person')
        verbose_name_plural = _('verbose_name_plural_person')

    def __str__(self):
        return self.full_name


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey(
        'Filmwork',
        on_delete=models.CASCADE
    )
    person = models.ForeignKey(
        'Person',
        on_delete=models.CASCADE,
        verbose_name=_("verbose_name_person")
    )
    role = models.TextField(
        _('role'),
        null=True
    )
    created = models.DateTimeField(
        _("created"),
        auto_now_add=True
    )

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('verbose_name_person_film_work')
        verbose_name_plural = _('verbose_name_plural_person_film_work')

    def __str__(self):
        return ""
