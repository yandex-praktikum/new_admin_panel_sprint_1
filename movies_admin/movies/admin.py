from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ("name",)


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    verbose_name = _("Genre")
    verbose_name_plural = _("Genres")


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline,)

    # Отображение полей в списке
    list_display = (
        "title",
        "type",
        "creation_date",
        "rating",
        "created",
        "modified",
    )

    # Фильтрация в списке
    list_filter = ("type",)

    # Поиск по полям
    search_fields = ("title", "description", "id")


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ("film_work",)
    verbose_name = _("Filmwork")
    verbose_name_plural = _("Filmworks")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (PersonFilmworkInline,)

    search_fields = ("full_name", "id")
