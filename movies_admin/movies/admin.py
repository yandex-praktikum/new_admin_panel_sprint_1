from django.contrib import admin
from .models import Genre, Filmwork, GenreFilmwork, Person, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('id','name')

class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork

@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline,)
    # Отображение полей в списке
    list_display = ('id', 'title', 'type', 'creation_date', 'rating',) 
    # Фильтрация в списке
    list_filter = ('title', 'type', 'rating')
    # Поиск по полям
    search_fields = ('id', 'title', 'description',) 

class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (PersonFilmworkInline,)

    # Отображение полей в списке
    list_display = ('id', 'full_name',)
    # Фильтрация в списке
    list_filter = ('full_name',)
    # Поиск по полям
    search_fields = ('id', 'full_name',)

