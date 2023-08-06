
import rlogging
import rocshelf

from django.http import HttpRequest

logger = rlogging.get_logger('mainLogger')


class RocshelfRouteMixin(object):
    """ Миксин для генерации пути до шаблона """

    def template(self, request: HttpRequest, route: str) -> str:
        """ Получение пути до rocshelf шаблона

        Args:
            request (HttpRequest): Объект запроса
            route (str): Маршрут

        Returns:
            str: Абсолютный путь до шаблона

        """

        languageCode = '_'
        if hasattr(request, 'LANGUAGE_CODE'):
            languageCode = request.LANGUAGE_CODE

        templatePath = rocshelf.UIIntegration.template('ru', route)

        logger.debug('Получение пути до rocshelf шаблона ({0}/{1}): {2}'.format(
            languageCode,
            route,
            templatePath
        ))

        return templatePath
