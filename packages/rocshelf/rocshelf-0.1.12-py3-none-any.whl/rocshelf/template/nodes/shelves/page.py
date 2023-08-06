from __future__ import annotations

import rlogging
from rocshelf.compile.params import ProcessingParams
from rocshelf.template import node
from rocshelf.template import areas, deconstruct, literals, main, node, nodes

logger = rlogging.get_logger('mainLogger')


class ShelfPageNode(nodes.ShelfNode):
    """ Нода шелфа-страницы """

    def __init__(self, shelfPageName: str):
        super().__init__(None, None, None)
        self.deconstruct('page', shelfPageName)

    def _processing(self, proccParams: ProcessingParams) -> node.ProcessingOutputNode:
        super()._processing()

        self.subNodes = self.shelfFileNodes

        return node.ProcessingOutputNode.from_node(self, proccParams, {
            'shelves': [str(self.shelfItem)]
        })
