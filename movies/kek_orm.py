from models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork


filmworks_genres = GenreFilmWork.objects.all()[:3]
for filmwork_genre in filmworks_genres:
    print(filmwork_genre.filmwork.title, filmwork_genre.genre.name)