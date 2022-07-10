from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (
    Genre,
    Filmwork,
    GenreFilmwork,
    Person,
    PersonFilmwork
)


class EmptyValueMixin(admin.ModelAdmin):
    empty_value_display = _("-empty-")

    class Meta:
        abstract = True


@admin.register(Genre)
class GenreAdmin(EmptyValueMixin):
    list_display = (
        'name',
        'created',
        'modified'
    )
    list_filter = (
        'created',
        'modified'
    )
    search_fields = (
        'name',
        'description',
        'id'
    )


@admin.register(Person)
class PersonAdmin(EmptyValueMixin):
    list_display = (
        'full_name',
        'created',
        'modified'
    )
    list_filter = (
        'created',
        'modified'
    )
    search_fields = (
        'full_name',
        'id'
    )


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork


@admin.register(Filmwork)
class FilmWorkAdmin(EmptyValueMixin):
    inlines = (
        GenreFilmworkInline,
        PersonFilmworkInline,
    )
    list_display = (
        'title',
        'type',
        'creation_date',
        'rating',
        'created',
        'modified'
    )
    list_filter = (
        'type',
        'creation_date',
        'rating'
    )
    search_fields = (
        'title',
        'description',
        'id'
    )
