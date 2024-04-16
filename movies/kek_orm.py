from movies.models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork
from django.db import connection
connection.queries

star_wars = FilmWork.objects.get(title='Star Wars: Episode VIII - The Last Jedi')
print(star_wars.genres.all())

# Взять три записи из таблицы FilmworkGenre, и выясните, к каким фильмам и жанрам они относятся.
filmworks_genres = GenreFilmWork.objects.all()[:3]
for filmwork_genre in filmworks_genres:
    print(filmwork_genre.film_work.title, filmwork_genre.genre.name)


filmworks_genres = GenreFilmWork.objects.all().select_related('film_work', 'genre')[:3]
for filmwork_genre in filmworks_genres:
    print(filmwork_genre.film_work.title, filmwork_genre.genre.name)

# 10 фильмов, в названии которых упомянуты Star Wars, и выведите их жанры и имена создателей.
star_wars_films = FilmWork.objects.filter(title__icontains='Star Wars')[:10]
for filmwork in star_wars_films:
    print(filmwork.genres.all())
    print(filmwork.persons.all())

