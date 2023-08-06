""" Модуль с областями видимости структур

Для использования классов из этого модуля,
...

"""

from __future__ import annotations

import typing as _T

import rlogging
from rocshelf import template

logger = rlogging.get_logger('mainLogger')


class NodeArea(object):
    """ Класс формирования области видемости литералов """

    @classmethod
    def arealize(cls, litValues: list[_T.Union[template.literals.LiteralValue, template.node.Node]], thisIndex: int) -> range:
        """ Формирует область виденья.

        Args:
            litValues (int): Список литералов
            thisIndex (int): Индекс вызвавшего литерала

        Returns:
            range: Диапазон индексов, которые относятся к литералу
                Если возвращается None вызывается area
        """

        raise TypeError('NodeArea "{0}" не имеет собственного "arealize"'.format(
            cls.__name__
        ))


class ThisNodeArea(NodeArea):
    """ Область видимости - вызывающий литерал """

    @classmethod
    def arealize(cls, litValues: list[_T.Union[template.literals.LiteralValue, template.node.Node]], thisIndex: int) -> int:
        return thisIndex


class AllNodeArea(NodeArea):
    """ Область видимости - все доступные литералы """

    @classmethod
    def arealize(cls, litValues: list[_T.Union[template.literals.LiteralValue, template.node.Node]], thisIndex: int) -> int:
        return -1


class NextNodeArea(NodeArea):
    """ Область видимости - вызывающий литерал и следующий """

    @classmethod
    def arealize(cls, litValues: list[_T.Union[template.literals.LiteralValue, template.node.Node]], thisIndex: int) -> int:
        callLitValue = litValues[thisIndex]

        nextLitValues = template.deconstruct.Juxtaposition.juxtaposition_core(litValues[thisIndex + 1:])

        targetNodeIndex = None

        for nodeIndex in range(len(nextLitValues)):
            iterNode = nextLitValues[nodeIndex]
            if not (isinstance(iterNode, template.nodes.TextNode) and iterNode.callParameter == ''):
                targetNodeIndex = nodeIndex
                break

        if targetNodeIndex is None:
            raise Exception('Будет смешно')

        newNode = callLitValue.literal.node.create(callLitValue, nextLitValues[targetNodeIndex])
        nodesList = litValues[:thisIndex] + [newNode] + nextLitValues[targetNodeIndex + 1:]

        return template.main.NodesList(nodesList)


class CloseNodeArea(NodeArea):
    """ Область видимости - вызывающий литерал и все до закрывающего. Закрывающий пропускается. """

    @classmethod
    def arealize(cls, litValues: list[_T.Union[template.literals.LiteralValue, template.node.Node]], thisIndex: int) -> _T.Optional[range]:
        callLitValue = litValues[thisIndex]

        if callLitValue.patterIndex == 1:
            return None

        logger.debug('Поиск закрывающего литерала для литерала "{0}"'.format(
            callLitValue
        ))

        startIndex = thisIndex
        stopIndex = len(litValues)

        closeOpenCount = 1

        for literalIndex in range(thisIndex + 1, len(litValues)):

            litValue = litValues[literalIndex]

            if isinstance(litValue, template.node.Node):
                continue

            if litValue.literal.node != callLitValue.literal.node:
                continue

            if litValue.patterIndex == 0:
                closeOpenCount += 1

            elif litValue.patterIndex == 1:
                closeOpenCount -= 1

            if closeOpenCount == 0:
                stopIndex = literalIndex
                break

        return range(startIndex + 1, stopIndex - 1)
