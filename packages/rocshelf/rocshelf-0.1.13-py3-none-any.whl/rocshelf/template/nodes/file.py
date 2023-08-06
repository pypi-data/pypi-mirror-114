

from __future__ import annotations

import os
import typing as _T
from copy import copy

import rlogging
from rcore.rpath import rPath
from rocshelf import exception as ex
from rocshelf.compile.params import ProcessingParams
from rocshelf.template import areas, deconstruct_file, literals, main, node

logger = rlogging.get_logger('mainLogger')


class BaseFileNode(node.Node):
    """ Нода определяющая файл

    Нода обработки нового файла

    При инициализации принимает ссылку на файл

    """

    __slots__ = ('decFile', )

    decFile: _T.Optional[deconstruct_file.DeconstructedFile]

    def _exception(self, stage: str, exError: ex.rExError) -> ex.rExError:
        exError.append_traceback(
            self.fileSpan.generate_traceback()
        )
        return exError

    def _deconstruct(self, filePath: rPath):
        if not filePath.check():
            raise ex.rException(FileNotFoundError(str(filePath)))

        self.decFile = deconstruct_file.DeconstructedFile.get(filePath)

    def get_file_nodes(self) -> _T.Optional[main.NodesList]:
        """ Получение нод файла

        Returns:
            _T.Optional[main.NodesList]: Ноды

        """

        logger.debug('Получения нод файла {0}'.format(
            self.decFile
        ))

        self.decFile.recursion()

        if self.decFile is not None:
            return self.decFile.get_nodes()

        return None

    def _processing(self, proccParams: ProcessingParams) -> node.ProcessingOutputNode:
        logger.debug('Обработка ноды "{0}" разобранного файла "{1}"'.format(
            self.__class__.__name__,
            self.decFile
        ))

        self.subNodes = self.get_file_nodes()

        return node.ProcessingOutputNode.from_node(self, proccParams)


class FileStructureNode(BaseFileNode):
    """ Нода файла для инициализации через литералы """

    area = areas.ThisNodeArea

    def _exception(self, stage: str, exError: ex.rExError) -> ex.rExError:
        exError.append_traceback(
            self.fileSpan.generate_traceback()
        )
        return exError

    @classmethod
    def literal_rule(cls):
        return literals.InLineStructureLiteral(
            'file', cls,
            ('import', None)
        )

    @classmethod
    def create(cls, literal: literals.LiteralValue):
        fileNode = cls(literal.content, literal.fileSpan)

        thisDecFile = deconstruct_file.deconstructedFilesId[literal.fileSpan.fileId]
        thisPathFile = copy(thisDecFile.pathFile)

        _, parentFileExtension = os.path.splitext(str(thisPathFile))

        fileName = literal.content
        fileName += parentFileExtension
        targetFile = thisPathFile.merge(fileName)

        fileNode.deconstruct(targetFile)

        return fileNode


class FileNode(BaseFileNode):
    """ Нода файла для инициализации напрямую """

    def _exception(self, stage: str, exError: ex.rExError) -> ex.rExError:
        exError.append_traceback(
            ex.ex.traceback.TextTracebackStage('Прямая инициализация файла через "{0}"'.format(
                self.__class__.__name__
            ))
        )
        return exError

    def __init__(self, filePath: rPath):
        super().__init__(None, None, None)
        self.deconstruct(filePath)
