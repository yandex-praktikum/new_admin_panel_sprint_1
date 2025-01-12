from django.contrib import admin
from .models import Genre, Filmwork, GenreFilmwork, Person, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('id','name')
    search_fields = ('id', 'name')

class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    autocomplete_fields = ('genre',)

@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline,)
    list_filter = ('title', 'type', 'rating')
    # Поиск по полям
    search_fields = ('id', 'title', 'description',) 
    list_display = ('id', 'title', 'type', 'creation_date', 'rating', 'get_genres')
    list_prefetch_related = ('genres',)

    def get_queryset(self, request): 
        queryset = ( 
            super()
            .get_queryset(request) 
            .prefetch_related(*self.list_prefetch_related) 
        ) 
        return queryset 
    
    def get_genres(self, obj): 
        genres = obj.genres.all()
        return ', '.join([genre.name for genre in genres]) 

    get_genres.short_description = 'Жанры фильма'


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ('person', 'film_work')

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (PersonFilmworkInline,) 
    # Отображение полей в списке
    list_display = ('id', 'full_name',)
    # Фильтрация в списке
    list_filter = ('full_name',)
    # Поиск по полям
    search_fields = ('id', 'full_name', 'person', 'film_work')

