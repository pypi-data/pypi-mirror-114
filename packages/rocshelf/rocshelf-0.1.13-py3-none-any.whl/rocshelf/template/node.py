from __future__ import annotations

import typing as _T

import rlogging
from rcore import utils
from rocshelf import exception as ex
from rocshelf.compile.params import ProcessingParams
from rocshelf import template

logger = rlogging.get_logger('mainLogger')


class InitNode(object):
    """ Основа """

    __slots__ = ('callParameter', 'fileSpan', 'subNodes', 'proccParams')

    area = None

    callParameter: _T.Optional[str]
    fileSpan: _T.Optional[template.main.FileSpan]
    subNodes: _T.Optional[template.main.NodesList]
    proccParams: ProcessingParams

    def __str__(self):
        return '<Node:{0} ({1})>'.format(
            self.__class__.__name__,
            self.callParameter
        )

    def __repr__(self) -> str:
        return '<Node:{0} ({1}) with [{2}]>'.format(
            self.__class__.__name__,
            self.callParameter,
            repr(self.subNodes),
        )

    def __init__(self, callParameter: _T.Optional[str] = None, fileSpan: _T.Optional[template.main.FileSpan] = None, subNodes: _T.Optional[_T.Union[template.main.NodesList, list]] = None) -> None:

        template.main.InitComponent.all_stages()

        if callParameter is not None and callParameter.strip() == '':
            callParameter = None

        if isinstance(subNodes, list):
            subNodes = template.main.NodesList(subNodes)

        self.callParameter = callParameter
        self.fileSpan = fileSpan
        self.subNodes = subNodes
        self.proccParams = None

        logger.debug('Инициализация ноды: "{0}"'.format(
            repr(self)
        ))

    @classmethod
    def literal_rule(cls):
        """ Формирование правила для разбиения строки """

        raise TypeError('Нода {0} не поддерживает создание через использование литерала'.format(
            cls.__name__
        ))

    @classmethod
    def create(cls, literal):
        """ Инициализация объекта через литерал """

        raise TypeError('Нода {0} не поддерживает создание через использование литерала'.format(
            cls.__name__
        ))


class ApiNode(InitNode):
    """ Основа """

    def _exception(self, stage: str, exError: ex.rExError) -> ex.rExError:
        """ Если при обработке или компиляции ноды что-то пойдет не так """

        return exError

    def _deconstruct(self, *args, **kwargs) -> ProcessingOutputNode:
        """ Первостепенная обработка ноды происходящая в момент обработки файлов """

        raise TypeError('Нода {0} не первостепенную обработку'.format(
            self.__class__.__name__
        ))

    def _processing(self, proccParams: ProcessingParams) -> ProcessingOutputNode:
        """ Обработка ноды """

        return ProcessingOutputNode.from_node(self, proccParams)

    def _compile(self, proccParams: ProcessingParams) -> str:
        """ Перевод ноды в текст """

        raise TypeError('Нода {0} не поддерживает компиляцию'.format(
            self.__class__.__name__
        ))


class Node(ApiNode):
    """ Основа """

    def exception(self, stage: str, exError: ex.rExError) -> ex.rExError:
        """ Создание исключения/добавление трейсбека

        Args:
            stage (ex.rExError): Стадия компиляции ноды
            exError (ex.rExError): Исключение

        Returns:
            ex.rExError: Исключение

        """

        logger.log(0, 'Запуск генерации трейсбека от ноды "{0}" во время стадии "{2}" для ошибки "{1}"'.format(
            repr(self),
            exError,
            stage
        ))

        return self._exception(stage, exError)

    def deconstruct(self, *args, **kwargs) -> None:
        """ Первостепенная обработка ноды происходящая в момент обработки файлов

        Raises:
            exception: Если что-то пойдет не так, к трейсбеку добавиться новый уровень

        """

        logger.log(0, 'Запуск создания ноды "{0}" с параметрами: {1}, {2}'.format(
            repr(self),
            args,
            kwargs
        ))

        try:
            self._deconstruct(*args, **kwargs)

        except ex.rExError as exError:
            raise self.exception('deconstruct', exError)

    def processing(self, proccParams: _T.Optional[ProcessingParams] = None) -> ProcessingOutputNode:
        """ Первая стадия компиляции нод - предварительная обработка нод:

        Удаление ненужных нод, преобразование статичных нод и т.д.

        Args:
            proccParams (_T.Optional[ProcessingParams], optional): Параметры компиляции. Defaults to None.
                Переменные, используемые при компиляции.

        Returns:
            ProcessingOutputNode: Нода предварительной стадии компиляции.
            Для завершения компиляции нужно вызвать метод compile()

        Raises:
            exception: Если что-то пойдет не так, к трейсбеку добавиться новый уровень

        """

        logger.log(0, 'Запуск обработки ноды "{0}"'.format(
            repr(self)
        ))

        if not isinstance(proccParams, ProcessingParams):
            proccParams = ProcessingParams(proccParams)

        if self.proccParams is not None:
            proccParams.add(
                self.proccParams
            )

        try:
            return self._processing(proccParams)

        except ex.rExError as exError:
            raise self.exception('processing', exError)

    def compile(self, proccParams: _T.Union[ProcessingParams, dict, None] = None) -> str:
        """ Вторая стадия компиляции нод - перевод нод в текст.

        Args:
            proccParams (_T.Optional[ProcessingParams], optional): Параметры компиляции. Defaults to None.
                Переменные, используемые при компиляции.

        Returns:
            str: Итоговая строка

        Raises:
            exception: Если что-то пойдет не так, к трейсбеку добавиться новый уровень

        """

        logger.log(0, 'Запуск компиляции ноды "{0}"'.format(
            repr(self)
        ))

        if not isinstance(proccParams, ProcessingParams):
            proccParams = ProcessingParams(proccParams)

        if self.proccParams is not None:
            proccParams.add(
                self.proccParams
            )

        try:
            return self._compile(proccParams)

        except ex.rExError as exError:
            raise self.exception('processing', exError)


class ProcessingOutputNode(Node):
    """ Нода, которая будет использоваться при обработки других нод.

    Состоит только из нод текста. Все структуры должны выполнить свою обработку до вызова этой ноды.

    -!! Params:
    -!!    statistics: dict - некая статистика, собирающаяся при компиляции
    -!!    params: dict - некая параметры, собирающаяся при компиляции

    """

    __slots__ = ('collectedData', )

    collectedData: dict

    def __init__(self):
        super().__init__()

        self.collectedData = {}
        self.subNodes = template.main.NodesList()

    def _compile(self, proccParams: ProcessingParams) -> str:
        logger.debug('Сборка ноды: "{0}"'.format(
            repr(self)
        ))

        resultString = ''
        for subItem in self.subNodes:
            resultString += subItem.compile(proccParams)

        logger.debug('Результат сборки: "{0}"'.format(
            utils.short_text(resultString)
        ))

        return resultString

    def add(self, processingNode: ProcessingOutputNode, mergeNodes: bool = True):
        """ Добавление к трейсеру новых значений

        Args:
            processingNode (ProcessingOutputNode): Результат обработки другой ноды
            mergeNodes (bool, optional): Сливать ноды или нет. Defaults to True.

        """

        logger.debug('Слияние нод: "{0}" $ "{1}"'.format(
            repr(self),
            repr(processingNode)
        ))

        if mergeNodes:
            self.subNodes += processingNode.subNodes

        self.collectedData = utils.rDict(self.collectedData).merge(processingNode.collectedData, True).attend

    def start_sub_nodes_processing(self, subNodes: template.main.NodesList, proccParams: ProcessingParams):
        """ Запуск функции обработки у ноды и добавление результата в себя

        Args:
            subNodes (template.main.NodesList): Список нод
            proccParams (ProcessingParams): Параметры обработки

        """

        for subNode in subNodes:
            processingNode = subNode.processing(proccParams)
            self.add(processingNode)

    @classmethod
    def from_node(cls, activeNode: Node, proccParams: ProcessingParams, collectedData: _T.Optional[dict] = None):
        """  Формирование ноды обработки из под нод обрабатываемой ноды.

        Подразумевается, что эта нода завешила свою работу.

        Args:
            activeNode (Node): Обработанная нода.
            proccParams (ProcessingParams): Парастеры компиляции.
            collectedData (_T.Optional[dict], optional): Собираемые при обработке данные. Defaults to None.

        Returns:
            [type]: Нода результата обработки

        """

        logger.debug('Формирование ноды: "{0}" из subNodes у ноды "{1}"'.format(
            cls.__name__,
            repr(activeNode)
        ))

        outputNode = cls()

        if collectedData is not None:
            outputNode.collectedData = collectedData

        if activeNode.subNodes is not None:
            outputNode.start_sub_nodes_processing(activeNode.subNodes, proccParams)

        return outputNode

    @classmethod
    def node(cls, activeNode: Node, proccParams: ProcessingParams, collectedData: _T.Optional[dict] = None) -> ProcessingOutputNode:
        """ Формирование ноды обработки из обрабатываемой ноды.

        Подразумевается, что эта нода обработается до конца на этапе компиляции

        Args:
            activeNode (Node): Нода.
            proccParams (ProcessingParams): Парастеры компиляции.
            collectedData (_T.Optional[dict], optional): Собираемые при обработке данные. Defaults to None.

        Returns:
            ProcessingOutputNode: Нода результата обработки

        """

        logger.debug('Формирование ноды: "{0}" из ноды "{1}"'.format(
            cls.__name__,
            repr(activeNode)
        ))

        outputNode = cls()

        if activeNode.subNodes is not None:
            outputNode.start_sub_nodes_processing(activeNode.subNodes, proccParams)
            activeNode.subNodes = outputNode.subNodes

        outputNode.subNodes = template.main.NodesList([
            activeNode
        ])
        return outputNode
