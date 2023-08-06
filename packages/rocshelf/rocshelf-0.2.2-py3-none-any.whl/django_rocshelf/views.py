import typing as _T

import rlogging
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from django_rocshelf import mixins

logger = rlogging.get_logger('mainLogger')


class RocshelfTemplateView(View, mixins.RocshelfRouteMixin):
    """ Представление для использования маршрутов rocshelf """

    def template(self, request: HttpRequest, route: str, context: _T.Optional[dict] = None) -> HttpResponse:
        """ Создание ответа с шаблоном по маршруту

        Args:
            request (HttpRequest): Объект запроса
            route (str): Маршрут
            context (dict): Контекст рендеринга страницы

        Returns:
            HttpResponse: Рендер страницы

        """

        logger.warning('Создание ответа с шаблоном по маршруту: {0}'.format(
            route
        ))

        if context is None:
            context = {}

        templatePath = super().template(request, route)

        return render(request, templatePath, context)


class RocshelfRouteView(RocshelfTemplateView):
    """ Представление для подстановки в генерацию путей на основе маршрутов rocshelf """

    def get(self, request: HttpRequest, routeName: str) -> HttpResponse:
        return self.template(request, routeName)
