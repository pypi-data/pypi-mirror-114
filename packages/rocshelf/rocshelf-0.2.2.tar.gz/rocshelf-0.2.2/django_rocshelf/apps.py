import rocshelf
from django.apps.config import AppConfig
from django.conf import settings

from django_rocshelf import urls


class RocshelfAppConfig(AppConfig):
    """ Конфигурация django приложения для подключения к django """

    name = 'django_rocshelf'
    verbose_name = 'rocshers for django'

    def ready(self):
        rocshelf.UIIntegration.init(
            getattr(settings, 'ROCSHELF_DIST_PATH', None),
            getattr(settings, 'ROCSHELF_CACHE_PATH', None)
        )

        urls.generate_urls()
