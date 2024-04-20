from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q, QuerySet
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import FilmWork, PersonFilmWork


class MoviesApiMixin:
    model = FilmWork
    http_method_names = ["get"]

    def get_queryset(self) -> QuerySet:
        result = FilmWork.objects.prefetch_related("genres", "persons").values(
            "id", "title", "description", "creation_date", "rating", "type"
        )

        annotated_result = result.annotate(
            genres=ArrayAgg("genres__name", distinct=True),
            actors=ArrayAgg(
                "persons__full_name",
                distinct=True,
                filter=Q(personfilmwork__role=PersonFilmWork.RoleType.ACTOR),
            ),
            directors=ArrayAgg(
                "persons__full_name",
                distinct=True,
                filter=Q(personfilmwork__role=PersonFilmWork.RoleType.DIRECTOR),
            ),
            writers=ArrayAgg(
                "persons__full_name",
                distinct=True,
                filter=Q(personfilmwork__role=PersonFilmWork.RoleType.WRITER),
            ),
        )
        return annotated_result

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Возвращает словарь с данными для формирования страницы;
        """
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, self.paginate_by)
        return {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": page.previous_page_number() if page.has_previous() else None,
            "next": page.next_page_number() if page.has_next() else None,
            "results": list(queryset),
        }


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_context_data(self, **kwargs):
        return kwargs["object"]
