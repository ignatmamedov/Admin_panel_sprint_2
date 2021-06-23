from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import Filmwork, FilmworkPerson, ProfessionType


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    def get_queryset(self):
        id = self.kwargs.get("pk", None)
        return Filmwork.objects.filter(pk=id).values().annotate(
            genres=ArrayAgg('genres__name'),
            actors=ArrayAgg('persons__first_name', distinct=True, filter=Q(filmworkperson__role=ProfessionType.ACTOR)),
            directors=ArrayAgg('persons__first_name', distinct=True,
                               filter=Q(filmworkperson__role=ProfessionType.DIRECTOR)),
            writers=ArrayAgg('persons__first_name', distinct=True,
                             filter=Q(filmworkperson__role=ProfessionType.WRITER)),
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = list(self.get_queryset())[0]

        return context


class Movies(MoviesApiMixin, BaseListView):
    def get_queryset(self):

        return Filmwork.objects.prefetch_related('genres').values().annotate(
            genres=ArrayAgg('genres__name'),
            actors=ArrayAgg('persons__first_name', distinct=True, filter=Q(filmworkperson__role=ProfessionType.ACTOR)),
            directors=ArrayAgg('persons__first_name', distinct=True,
                               filter=Q(filmworkperson__role=ProfessionType.DIRECTOR)),
            writers=ArrayAgg('persons__first_name', distinct=True,
                             filter=Q(filmworkperson__role=ProfessionType.WRITER)),
        )

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

