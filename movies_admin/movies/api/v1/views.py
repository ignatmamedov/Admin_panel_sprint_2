from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import Filmwork, FilmworkPerson, ProfessionType


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        id = self.kwargs.get("pk", None)
        queryset = Filmwork.objects.values(
            'id',
            'title',
            'description',
            'creation_date',
            'rating',
            'type',
        ).annotate(
            genres=ArrayAgg('genres__name'),
            actors=ArrayAgg('persons__first_name', distinct=True, filter=Q(filmworkperson__role=ProfessionType.ACTOR)),
            directors=ArrayAgg('persons__first_name', distinct=True,
                               filter=Q(filmworkperson__role=ProfessionType.DIRECTOR)),
            writers=ArrayAgg('persons__first_name', distinct=True,
                             filter=Q(filmworkperson__role=ProfessionType.WRITER)),
        )
        return queryset

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context, safe=False)


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, *, object_list=None, **kwargs):
        return self.object


class Movies(MoviesApiMixin, BaseListView):
    def get_context_data(self, *, object_list=None, **kwargs):
        paginator, page, queryset, is_paginated = self.paginate_queryset(list(self.get_queryset()), 50)
        next = None
        previous = None
        if page.has_next():
            next = page.next_page_number()
        if page.has_previous():
            previous = page.previous_page_number()
        context = {
            'next': next,
            'count': page.paginator.count,
            'total_pages': page.paginator.num_pages,
            'prev': previous,
            'results': page.object_list
        }
        return context
