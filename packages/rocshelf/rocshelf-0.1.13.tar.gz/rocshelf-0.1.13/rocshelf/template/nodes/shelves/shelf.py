from __future__ import annotations

import rlogging
from rocshelf.components.shelves import GetShelf, ShelfItem
from rocshelf.template import areas, deconstruct, literals, main, node, nodes

logger = rlogging.get_logger('mainLogger')


class ShelfNode(nodes.BaseFileNode):
    """ Основной класс шелф нод """

    __slots__ = ('shelfItem', 'shelfFileNodes')

    shelfItem: ShelfItem
    shelfFileNodes: main.NodesList

    def _deconstruct(self, shelfType: str, shelfName: str) -> None:
        self.shelfItem = GetShelf.name(shelfType, shelfName)
        self.callParameter = str(self.shelfItem)

        logger.debug('Инициализация ноды шелфа: {}'.format(
            self.shelfItem
        ))

        shelfHtmlPath = self.shelfItem.paths.type('html')

        self.decFile = None

        if shelfHtmlPath is not None:
            try:
                super()._deconstruct(shelfHtmlPath)

            except FileNotFoundError:
                self.decFile = None

    def _processing(self) -> node.ProcessingOutputNode:
        """ Инициализация нод шелф-файла """

        logger.debug('Обработка ноды "{0}" разобранного файла "{1}"'.format(
            self.__class__.__name__,
            self.decFile
        ))

        self.shelfFileNodes = self.get_file_nodes()
