""" Модуль для работы с файлами, которые попадают в шаблонизатор """

from __future__ import annotations

import typing as _T
from copy import deepcopy

import rlogging
from rcore.rpath import rPath
from rocshelf import exception as ex
from rocshelf import template

logger = rlogging.get_logger('mainLogger')

# Словарь пути до файла и объекта файла
deconstructedFiles: dict[str, DeconstructedFile] = {}

# Словарь идентификатора файла и объекта файла
deconstructedFilesId: dict[int, DeconstructedFile] = {}

# Количество разрешимых обработок для файла
MAX_RECURSION_COUNT = 10


def get_file(fileId: int) -> rPath:
    """ Получение файла по идентификатору

    Args:
        fileId (int): Идентификатор файла

    Returns:
        rPath: Путь до файла

    """

    return deconstructedFilesId[fileId].pathFile


class DeconstructedFile(object):
    """ Файл прошедший разборку """

    __slots__ = ('pathFile', 'hash', 'id', 'subNodes', 'recursionCount')

    # Счетчик объектов, используемый при установке идентификаторов
    quantityFiles: int = 0

    pathFile: rPath
    hash: str
    id: int

    subNodes: template.main.NodesList

    recursionCount: int

    def __str__(self) -> str:
        return '<{0}.{1} id: {2} ({3})>'.format(
            __name__,
            self.__class__.__name__,
            self.id,
            self.pathFile,
        )

    def __init__(self, pathFile: rPath) -> None:
        """ Инициализация объекта

        Args:
            pathFile (rPath): Путь до файла

        """

        logger.debug('Инициализация объекта файла проходящего разбор')

        self.recursionCount = 0

        self.pathFile = pathFile
        self.hash = self.file_hash(pathFile)

        self.id = DeconstructedFile.quantityFiles
        DeconstructedFile.quantityFiles += 1

        deconstructedFiles[self.pathFile] = self
        deconstructedFilesId[self.id] = self

        context = template.main.context_generator(pathFile)

        self.subNodes = template.deconstruct.deconstruct(
            pathFile.read(), self.id, context
        )

        logger.debug('Инициализация объекта файла проходящего разбор с идентификатором {0} и {1} под нод'.format(
            self.id,
            len(self.subNodes)
        ))

    def check_actual(self):
        """ Проверка актуальности объекта

        Raises:
            TypeError: Объект, из которого вызван метод устарел

        """

        actualObject = deconstructedFiles[self.pathFile]

        if actualObject.hash != self.hash:
            raise TypeError('Объект, из которого вызван метод, устарел')

    def get_nodes(self) -> template.main.NodesList:
        """ Получение копии нод файла

        Returns:
            main.NodesList: Ноды

        """

        self.check_actual()

        return deepcopy(self.subNodes)

    def recursion(self):
        """ Учет рекурсии

        Raises:
            RecursionTemplateError: Превышение лимита

        """

        self.recursionCount += 1

        if self.recursionCount >= MAX_RECURSION_COUNT:
            raise ex.RecursionTemplateError('Обрабатываемый файл "{0}" превысил рекурсионный лимит.'.format(
                self.pathFile
            ))

    @staticmethod
    def file_hash(pathFile: rPath) -> str:
        """ Генерация хеша файла, проходящего обработку

        Хеш формируется из пути файла и содержимого.

        Args:
            pathFile (rPath): Путь до файла

        Returns:
            str: Хеш файла

        """

        pathHash = hash(pathFile)
        contentHash = hash(
            pathFile.read()
        )

        resultHash = str(pathHash) + str(contentHash)

        logger.debug('Формирование хеша для файла "{0}". Результат: "{1}"'.format(
            pathFile,
            resultHash
        ))

        return resultHash

    @classmethod
    def get(cls: _T.Type[DeconstructedFile], pathFile: rPath) -> DeconstructedFile:
        """ Получение экземпляра объекта разобранного файла

        Args:
            pathFile (rPath): Путь до файла

        Returns:
            DeconstructedFile: Разобранный файл

        """

        if pathFile not in deconstructedFiles:
            logger.debug('Файл "{0}" не проходил разбор'.format(
                pathFile
            ))
            return cls(pathFile)

        decFile = deconstructedFiles[pathFile]
        hashFile = cls.file_hash(pathFile)

        if decFile.hash == hashFile:
            logger.debug('Файл "{0}" ({1}) проходил разбор и хеши с имеющимся объектом совпадают'.format(
                pathFile, decFile.id
            ))
            return decFile

        logger.debug('Файл "{0}" ({1}) проходил разбор и хеши с имеющимся объектом не совпадают'.format(
            pathFile, decFile.id
        ))

        return cls(pathFile)
