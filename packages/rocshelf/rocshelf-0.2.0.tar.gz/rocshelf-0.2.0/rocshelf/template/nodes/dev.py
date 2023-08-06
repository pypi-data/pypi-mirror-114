
from __future__ import annotations

import rlogging
from rocshelf.compile.params import ProcessingParams
from rocshelf.template import areas, deconstruct, literals, main, node

logger = rlogging.get_logger('mainLogger')


class TextNode(node.Node):
    """ Нода текста """

    area = areas.ThisNodeArea

    @classmethod
    def literal_rule(cls):
        return literals.TextLiteral(
            'text',
            cls
        )

    def _deconstruct(self) -> None:
        if self.callParameter is None:
            self.callParameter = ''

    @classmethod
    def create(cls, literal: literals.LiteralValue):
        newNode = cls(literal.content, literal.fileSpan)
        newNode.deconstruct()
        return newNode

    def _processing(self, proccParams: ProcessingParams) -> node.ProcessingOutputNode:
        return node.ProcessingOutputNode.node(self, proccParams)

    def _compile(self, proccParams: ProcessingParams):
        logger.debug('Применение ноды: "{0}"'.format(
            repr(self)
        ))

        return self.callParameter


class DevNode(node.Node):
    """ Нода для реализации костылей """

    def __init__(self, string: str, context: list[str]):
        super().__init__(None, None, None)
        self.deconstruct(string, context)

    def _deconstruct(self, string: str, context: list[str]) -> None:
        self.subNodes = deconstruct.deconstruct(
            string, None, context
        )


class StringNode(node.Node):
    """ Нода текста для инициализации напрямую """

    def __init__(self, string: str):
        super().__init__(None, None, None)
        self.deconstruct(string)

    def _deconstruct(self, string: str) -> None:
        context = main.context_generator()
        self.subNodes = deconstruct.deconstruct(
            string, None, context
        )


class CommentNode(node.Node):
    """ Нода закоментированного кода """

    area = areas.ThisNodeArea

    def _deconstruct(self, litValue: literals.LiteralValue):
        # Добавить проверку необходимость компилировать комментарии
        if False:
            self.subNodes = main.NodesList([
                TextNode(litValue.content, litValue.fileSpan)
            ])

    @classmethod
    def create(cls, litValue: literals.LiteralValue):
        newNode = cls(litValue.content, litValue.fileSpan)
        newNode.deconstruct(litValue)
        return newNode
