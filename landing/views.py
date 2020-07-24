# from django.shortcuts import render
from django.views.generic.base import TemplateView
from .services import get_anime_by_season

# Create your views here.


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['anime_list'] = get_anime_by_season(
            '2020', 'summer', '-averageRating', 20
        )['data']

        return context
