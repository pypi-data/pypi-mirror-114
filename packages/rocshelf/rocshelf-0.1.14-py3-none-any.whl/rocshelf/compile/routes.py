""" Модуль компиляции страниц.

Компиляция зависит от следующих параметров:
    Маршруты (настройка route): каждый маршрут - это отдельная страница
    Файлы локализации (настройка path -> import -> localization):
        На каждый файл с расширением .lang будет производиться итерация компиляция страниц из пункта выше.
        Результат компиляции каждого файла локализации будет храниться в папке с именем файла локализации.

"""

from __future__ import annotations

import multiprocessing as _M

import rlogging
from bs4 import BeautifulSoup
from rcore import sync
from rocshelf.compile import controller, params, tracebacks, utils
from rocshelf.components import localization, routes
from rocshelf.components.relations import Relation
from rocshelf.components.routes import GetRoute
from rocshelf.frontend.chunks import Chunk
from rocshelf import template


logger = rlogging.get_logger('mainLogger')

PROCESSING_PARSE_SHELVES_CACHE_FILE = 'rocshelf-used-shelves.json'


@tracebacks.stage_pre_analyze
def pre_analyze():
    """ Запуск анализатора шаблонов.

    Нужен для прочтения всех файлов, разбитие их на литералы и предварительную обработку.

    """

    logger.info('Анализ всех используемых shelf-страниц')

    for routeKey, route in GetRoute.walk():
        logger.debug('Анализ shelf-страницы "{0}" на которую ссылается маршрут "{1}"'.format(
            route.page,
            routeKey
        ))

        template.nodes.ShelfPageNode(route.page)


class CompileRoute(sync.process.OnProcessMixin):
    """ Класс в рамках которого происходит компиляция одного маршрута для одной локации """

    localizationName: str
    routeKey: str

    inputQueue: _M.Queue
    outputQueue: _M.Queue

    relation: Relation

    procParams: params.ProcessingParams

    def __init__(self, localizationName: str, routeKey: str, inputQueue: _M.Queue, outputQueue: _M.Queue):
        self.localizationName = localizationName
        self.routeKey = routeKey

        self.inputQueue = inputQueue
        self.outputQueue = outputQueue

        self.relation = Relation(None, localizationName)

        self.procParams = params.TemplateCompilationMetaData.processing_params(routeKey, localizationName)

    @tracebacks.stage_route_processing
    def processing(self, shelfNode: template.nodes.ShelfPageNode) -> template.node.ProcessingOutputNode:
        """ Обработка маршрута

        Args:
            shelfNode (template.nodes.ShelfPageNode): Узел shelf-страницы

        Returns:
            node.ProcessingOutputNode: Узел результата обработки

        """

        logger.info('Обработка маршрута "{0}" с локализацией "{1}"'.format(
            self.routeKey, self.localizationName
        ))

        return shelfNode.processing(self.procParams)

    def processing_data_analyze(self, processingNode: template.node.ProcessingOutputNode):
        """ Передача данных, собранных во время обработки, в соответствующие модули.

        Args:
            processingNode (template.node.ProcessingOutputNode): Узел результата обработки

        """

        # Передача в процесс-контроллер собраных данных
        self.inputQueue.put(processingNode.collectedData)

        # Получение результата котроллера
        # chunks - список чанков компилируемого маршрута
        chunks: list[Chunk] = self.outputQueue.get()

        # Добавление чанков в процесс компиляции
        self.procParams.meta().add_chucks(chunks)

    @tracebacks.stage_route_compile
    def compile(self, processingNode: template.node.ProcessingOutputNode) -> str:
        """ Компиляция маршрута

        Args:
            processingNode (template.node.ProcessingOutputNode): Узел результата обработки

        Returns:
            str: Скомпилированный текст

        """

        logger.info('Компиляция маршрута "{0}" в локализации "{1}"'.format(
            self.routeKey, self.localizationName
        ))

        return processingNode.compile(self.procParams)

    def save(self, compiledText: str):
        """ Сохранение результата компиляции

        Args:
            compiledText (str): Текст - результат компиляции

        """

        logger.info('Сохранение результата компиляции маршрута "{0}" в локализации "{1}"'.format(
            self.routeKey, self.localizationName
        ))

        filePath = self.relation.template_path(self.routeKey)
        if not filePath.check():
            filePath.create()

        filePath.write(compiledText, 'w')

    def normalize_html(self):
        """ Нормализация html разметки скомпилированного файла """

        pageFile = self.relation.template_path(self.routeKey)

        logger.debug('Нормализация Html страницы "{0}" маршрута "{1}" в локализации "{2}"'.format(
            pageFile, self.routeKey, self.localizationName
        ))

        pageText = pageFile.read()

        soup = BeautifulSoup(pageText, 'html.parser')

        pageText = soup.prettify()

        pageFile.write(pageText, 'w')

    @tracebacks.stage_route
    def on_process(self):
        page = GetRoute.route(self.routeKey).page
        shelfNode = template.nodes.ShelfPageNode(page)
        processingNode = self.processing(shelfNode)
        self.processing_data_analyze(processingNode)
        compiledText = self.compile(processingNode)
        self.save(compiledText)
        self.normalize_html()


def run():
    """ Запуск компиляции маршрутов """

    logger.info('Компиляция маршрутов. Компиляция будет происходить параллельно для {0} локализаций'.format(
        len(localization.localData.list())
    ))

    if not routes.GetRoute.list():
        logger.error('Компиляция маршрутов пропущена, так как не инициализированно ни одного маршрута')
        return

    processesPool = sync.process.NoDeamonProcessesPoolController(CompileRoute)

    compileController = controller.CompileController()

    with compileController as controllerManager:
        for localizationName in localization.localData.list():
            for routeKey in routes.GetRoute.list():
                inputQueue, outputQueue = controllerManager.queues(localizationName, routeKey)
                processesPool.add_process(localizationName, routeKey, inputQueue, outputQueue)

        processesPool.map()

        utils.statistics.usedShelves = controllerManager.common()
