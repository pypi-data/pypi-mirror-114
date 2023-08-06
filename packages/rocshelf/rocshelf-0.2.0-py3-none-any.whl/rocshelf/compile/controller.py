""" Модуль описания контроллеров, которые следят за процессом компиляции """

import typing as _T
import multiprocessing as _M
import rlogging
from rcore.rpath import rPath
from rocshelf.compile import static
from rocshelf.frontend.chunks import Chunk, StaticAnalyze
from rcore.sync import controllers
from rocshelf.components import routes, localization

saveStaticChunksFileName = 'rocshelf-static-chunks.json'
saveCollectedDataFileName = 'rocshelf-collected-data.json'

logger = rlogging.get_logger('mainLogger')


class CompileControllerManager(controllers.managers.BaseControllerManager):
    """ Менеджер для контроллера управления процессом компиляции """

    def queue_dict_key(self, localizationName: _T.Union[str, None], routeKey: str) -> str:
        return '{0}|{1}'.format(
            localizationName, routeKey
        )

    def queues(self, localizationName: _T.Union[str, None], routeKey: str) -> tuple[_M.Queue, _M.Queue]:
        processKey = self.queue_dict_key(localizationName, routeKey)
        return super().queues(processKey)

    def set_queues(self, localizationName: _T.Union[str, None], routeKey: str):
        processKey = self.queue_dict_key(localizationName, routeKey)
        super().set_queues(processKey)


class CompileControllerWorker(controllers.workers.BaseControllerWorker):
    """ Worker котроллера для управления процессом компиляции """

    localizationsList: list[str]
    routesList: list[str]

    collectedData: dict[str, dict[str, dict]]
    chunks: dict[str, list[Chunk]]
    usedShelves: set

    def __init__(self) -> None:
        self.localizationsList = localization.localData.list()
        self.routesList = routes.GetRoute.list()

        self.collectedData = None
        self.chunks = {}
        self.usedShelves = set()

    def put_data(self):
        """ Отправка обработанных данных в очереди """

        outputtedData = {}

        for localizationName, routesCollectedData in self.collectedData.items():
            for routeKey in routesCollectedData:
                dictKey = self.manager.queue_dict_key(localizationName, routeKey)

                outputtedData[dictKey] = [chunk for chunk in self.chunks[localizationName] if routeKey in chunk.routeKeys]

        super().put_data(outputtedData)

    def worker(self):
        self.collectedData = self.get_data()
        self.collectedData = self.deconstruct_data(self.collectedData)

        self.analyze_localization()
        self.put_statistics()

        self.compile_static()
        # Пут дата запускает компиляцию всей бизнеслогики шаблонов
        # А некоторые ноды опираются на файлы статики.
        # Поэтому статику нужно компилировать раньше
        self.put_data()
        
        self.save_cache()

    def deconstruct_data(self, collectedData: dict[str, _T.Any]) -> dict[str, dict[str, dict]]:
        """ Преобразование ключей процессов в имя локализации и маршрута

        Args:
            collectedData (dict[str, _T.Any]): Данные собранные из процессов

        Returns:
            dict: Преобразованный словарь

        """

        newCollectedData = {}

        for processKey, compileData in collectedData.items():
            localizationName, routeKey = processKey.split('|')

            if localizationName not in newCollectedData:
                newCollectedData[localizationName] = {}

            newCollectedData[localizationName][routeKey] = compileData

        return newCollectedData

    def analyze_localization(self):
        """ Анализ полученых от процессов данных на уровне локализации """

        logger.debug('Котнроллер Worker "{0}". Стадия: Анализ всех локализаций'.format(
            self.__class__.__name__
        ))

        for localizationName in self.collectedData:
            self.analyze_route(localizationName)

    def analyze_route(self, localizationName: str):
        """ Анализ полученых от процессов данных на уровне маршрутов в локализации

        Args:
            localizationName (str): Локализация

        """

        logger.debug('Котнроллер Worker "{0}". Стадия: Анализ всех маршуртов в локализации "{1}"'.format(
            self.__class__.__name__,
            localizationName
        ))

        for compileData in self.collectedData[localizationName].values():
            self.usedShelves.update(compileData['shelves'])

        self.analyze_static(localizationName)

    def analyze_static(self, localizationName: str) -> list[Chunk]:
        """ Анализ используемой статики при компиляции локализации

        Args:
            localizationName (str): Локализация

        """

        logger.info('Котнроллер Worker "{0}". Стадия: Передача собраных данных для локализации "{1}" в анализатор статики.'.format(
            self.__class__.__name__,
            localizationName
        ))

        staticProcessingData = {
            'shelves': {}
        }

        for routeKey, compileData in self.collectedData[localizationName].items():
            staticProcessingData['shelves'][routeKey] = set(compileData['shelves'])

        staticAnalyze = StaticAnalyze.all_stages(
            staticProcessingData
        )

        self.chunks[localizationName] = staticAnalyze.chunks

    def save_cache(self):
        """ Сохранение результатов анализа в кеш """

        logger.info('Котнроллер Worker "{0}". Стадия: Сохранение всей информации в кеш'.format(
            self.__class__.__name__
        ))

        chunkAnalyzedData = {}
        for localizationName, localizationChunks in self.chunks.items():
            chunkAnalyzedData[localizationName] = []
            for chunk in localizationChunks:
                chunkAnalyzedData[localizationName].append({
                    'routes': list(chunk.routeKeys),
                    'shelves': list(chunk.shelfSlugs)
                })

        filePath = rPath(saveCollectedDataFileName, fromPath='cache')
        filePath.dump(self.collectedData)

        filePath = rPath(saveStaticChunksFileName, fromPath='cache')
        filePath.dump(chunkAnalyzedData)

    def put_statistics(self):
        self.manager.commonQueue.put(self.usedShelves)

    def compile_static(self):
        """ Запуск компиляции статики """

        logger.info('Котнроллер Worker "{0}". Стадия: Запуск компиляции статики'.format(
            self.__class__.__name__
        ))

        for localizationName, localizationChunks in self.chunks.items():
            static.start_compile(localizationName, localizationChunks)


class CompileController(controllers.BaseController):
    """ Котроллера для управления процессом компиляции  """

    managerClass = CompileControllerManager
    workerClass = CompileControllerWorker

    def __init__(self):
        super().__init__()

        self.generate_queues()

    def generate_queues(self):
        """ Заполнение словарей очередей для input и output """

        for localizationName in localization.localData.list():
            for routeKey in routes.GetRoute.list():
                self.manager.set_queues(localizationName, routeKey)
