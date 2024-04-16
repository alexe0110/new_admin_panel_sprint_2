from movies.models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork
from django.db import connection
import datetime
from django.db.models import Count, Avg

from django.db import models
from django.db.models.functions import ExtractDay, Abs


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

star_wars_films = FilmWork.objects.prefetch_related('genres', 'persons').filter(title__icontains='Star Wars')[:10]
for filmwork in star_wars_films:
    print(filmwork.genres.all())
    print(filmwork.persons.all())

FilmWork.objects.filter(rating__gte=8, creation_date__gte=datetime.date(year=2020, month=1, day=1))

from django.db.models import Q, F
from movies.models import FilmWork

FilmWork.objects.filter(Q(rating__gte=8) | Q(creation_date__gte=datetime.date(year=2020, month=1, day=1)))

# Выбрать все нужные фильмы не составит труда:
need_to_increase_rating = FilmWork.objects.filter(persons__full_name='Samuli Torssonen')

# прибавить по 0.2 балла к каждой оценке.
for film in need_to_increase_rating:
    film.rating += 0.2
    film.save()

need_to_increase_rating.update(rating=F('rating') + 0.2)

# Для каждого актёра посчитайте количество фильмов, в которых он снимался.
print(*Person.objects.filter(
        personfilmwork__role=PersonFilmWork.RoleType.ACTOR
    ).annotate(count=Count('filmwork')).values_list('full_name', 'count'), sep='\n')

# Допустим, вы хотите найти фильм, который был выпущен в прокат недалеко от важной для вас даты.
# Для этого вам нужно рассчитать расстояние между датами используя F,
# привести результат к количеству дней при помощи ExtractDay, избавиться от отрицательных значений при помощи Abs,
# отсортировать по получившемуся числу и взять первый фильм.


filmwork_qs = FilmWork.objects.all()
expr = ExtractDay(models.ExpressionWrapper(
    datetime.datetime(2018, 11, 8 ) - F('creation_date'),
    output_field=models.DateField(),
))
film = filmwork_qs.annotate(delta=expr).filter(delta__isnull=False).annotate(abs_delta=Abs('delta')).order_by('abs_delta').first()


FilmWork.objects.filter(persons__full_name='Harrison Ford').aggregate(Avg('rating'))

# Raw-SQL
film = FilmWork.objects.raw('SELECT id, age(creation_date) AS age FROM "content"."film_work"')[0]
print(film)


FilmWork.objects.create(title='Conan Lol', creation_date=datetime.date.today(), rating=6)

