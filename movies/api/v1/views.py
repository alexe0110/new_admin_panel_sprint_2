from django.http import JsonResponse
from django.views.generic.list import BaseListView

from movies.models import FilmWork


class MoviesListApi(BaseListView):
    model = FilmWork
    http_method_names = ["get"]  # Список методов, которые реализует обработчик

    def get_queryset(self):
        """
        Должен возвращать подготовленный QuerySet
        """
        return ["das", "dascxxx", "djgysys"]

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Возвращает словарь с данными для формирования страницы;
        """
        context = {
            "results": list(self.get_queryset()),
        }
        return context

    def render_to_response(self, context, **response_kwargs):
        """
        Форматирование данных, которые вернутся при GET-запросе.
        """

        return JsonResponse(context)
