""" Модуль формирования маршрутов django на основе маршрутов rocshelf """

import rocshelf
from django.urls import path

from django_rocshelf import views

urlpatterns: list = []


def generate_urls():
    """ Генерация маршрутов urlpatterns """

    templates = rocshelf.UIIntegration.templates()

    for _, routes in templates.items():
        for routeName in routes:

            djangoRoute = routeName.replace('.', '/')

            urlpatterns.append(
                path(djangoRoute, views.RocshelfRouteView.as_view(), {'routeName': routeName}, name=routeName),
            )
