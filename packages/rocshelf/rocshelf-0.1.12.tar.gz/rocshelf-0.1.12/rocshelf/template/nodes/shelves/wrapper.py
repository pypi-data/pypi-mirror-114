from __future__ import annotations

import typing as _T

import rlogging
from rocshelf import exception as ex
from rocshelf.compile.params import ProcessingParams
from rocshelf.template import areas, deconstruct, literals, main, node, nodes

logger = rlogging.get_logger('mainLogger')


class ShelfWrapperNode(nodes.ShelfNode):
    """ Нода шелфа-обертки """

    area = areas.AllNodeArea

    @classmethod
    def literal_rule(cls):
        for point in ['wp', 'wrapper']:
            yield literals.InLineStructureLiteral(
                'shelves', cls,
                (point, None)
            )

    __slots__ = ('sections', )

    sections: dict[str, list]

    def _deconstruct(self, litValues: list[_T.Union[literals.LiteralValue, node.Node]]) -> None:
        super()._deconstruct('wrapper', self.callParameter)

        self.sections = {
            'main': []
        }

        litValues = deconstruct.Juxtaposition.juxtaposition_core(litValues)

        for litValue in litValues:
            if isinstance(litValue, ShelfWrapperSectionNode):
                if litValue.callParameter not in self.sections:
                    self.sections[litValue.callParameter] = []

                self.sections[litValue.callParameter].append(litValue)

            else:
                self.sections['main'].append(litValue)

    @classmethod
    def create(cls, litValue: literals.LiteralValue, litValues: main.NodesList):
        logger.debug('Создание "{0}" со значением имен: "{1}"'.format(
            cls.__name__,
            litValue.content
        ))

        shelfNames = litValue.content.split()

        if not shelfNames:
            raise ex.SyntaxTemplateError('Wrapper Shelf должен принимать минимум 1 параметр [имя шелфа]')

        shelfNode = cls(shelfNames[-1], litValue.fileSpan)
        shelfNode.deconstruct(litValues)

        if len(shelfNames) == 1:
            return shelfNode

        for shelfName in shelfNames[::-1][1:]:
            newNode = cls(shelfName, litValue.fileSpan)
            newNode.deconstruct(main.NodesList([
                shelfNode
            ]))
            shelfNode = newNode

        newNode = node.Node(litValue.content, litValue.fileSpan)
        newNode.subNodes = main.NodesList([
            shelfNode
        ])

        return newNode

    def __processing(self, shelfSubNodes):
        newShelfSubNodes = []

        for litValue in shelfSubNodes:
            if isinstance(litValue, ShelfWrapperPlaceNode) and litValue.callParameter in self.sections:
                newShelfSubNodes += self.sections.get(litValue.callParameter)
                continue

            elif litValue.subNodes is not None:
                litValue.subNodes = self.__processing(litValue.subNodes)

            newShelfSubNodes.append(litValue)

        return main.NodesList(newShelfSubNodes)

    def _processing(self, proccParams: ProcessingParams) -> node.ProcessingOutputNode:
        super()._processing()

        self.subNodes = self.shelfFileNodes
        middleProcessingNode = node.ProcessingOutputNode.from_node(self, proccParams)

        self.subNodes = self.__processing(middleProcessingNode.subNodes)

        processingNode = node.ProcessingOutputNode.from_node(self, proccParams, {
            'shelves': [str(self.shelfItem)]
        })

        processingNode.add(middleProcessingNode, False)

        return processingNode


class ShelfWrapperPlaceNode(node.Node):
    """ Нода места для вставки секций шелфа-обертки """

    area = areas.ThisNodeArea

    @classmethod
    def literal_rule(cls):
        for wpPoint in ['wp', 'wrapper']:
            for placePoint in ['p', 'place']:
                yield literals.InLineStructureLiteral(
                    'shelves', cls,
                    (wpPoint, placePoint),
                )

    @classmethod
    def create(cls, litValue: literals.LiteralValue):
        sectionName = litValue.content if litValue.content else 'main'
        return cls(sectionName, litValue.fileSpan)

    def _processing(self, proccParams: ProcessingParams) -> node.ProcessingOutputNode:
        return node.ProcessingOutputNode.node(self, proccParams)


class ShelfWrapperSectionNode(node.Node):
    """ Нода секции для шелфа-обертки """

    area = areas.CloseNodeArea

    @classmethod
    def literal_rule(cls):
        for wpPoint in ['wp', 'wrapper']:
            for sectionPoint in ['s', 'sect', 'section']:
                yield literals.InTwoLineStructureLiteral(
                    'shelves', cls,
                    (wpPoint, sectionPoint),
                    (sectionPoint, wpPoint)
                )

    @classmethod
    def create(cls, litValue: literals.LiteralValue, litValues: main.NodesList):
        sectionName = litValue.content if litValue.content else 'main'
        return cls(sectionName, litValue.fileSpan, main.NodesList(litValues))
