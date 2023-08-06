from __future__ import annotations

import rlogging
from rocshelf import exception as ex
from rocshelf.compile.params import ProcessingParams
from rocshelf.template import areas, deconstruct, literals, main, node, nodes

logger = rlogging.get_logger('mainLogger')


class ShelfBlockNode(nodes.ShelfNode):
    """ Нода шелфа-блока """

    area = areas.ThisNodeArea

    @classmethod
    def literal_rule(cls):
        for point in ['bl', 'block']:
            yield literals.InLineStructureLiteral(
                'shelves', cls,
                (point, None)
            )

    def _deconstruct(self) -> None:
        super()._deconstruct('block', self.callParameter)

    @classmethod
    def create(cls, litValue: literals.LiteralValue):
        logger.debug('Создание "{0}" со значением имен: "{1}"'.format(
            cls.__name__,
            litValue.content
        ))

        shelfNames = litValue.content.split()

        if not shelfNames:
            raise ex.SyntaxTemplateError('Tag Shelf должен принимать минимум 1 параметр [имя шелфа]')

        elif len(shelfNames) == 1:
            shelfNode = cls(shelfNames[0], litValue.fileSpan)
            shelfNode.deconstruct()
            return shelfNode

        subNodes = []

        for shelfName in shelfNames:
            newNode = cls(shelfName, litValue.fileSpan)
            newNode.deconstruct()
            subNodes.append(newNode)

        shelfNode = node.Node(litValue.content, litValue.fileSpan)
        shelfNode.subNodes = main.NodesList(subNodes)

        return shelfNode

    def _processing(self, proccParams: ProcessingParams) -> node.ProcessingOutputNode:
        super()._processing()

        self.subNodes = self.shelfFileNodes

        return node.ProcessingOutputNode.from_node(self, proccParams, {
            'shelves': [str(self.shelfItem)]
        })
