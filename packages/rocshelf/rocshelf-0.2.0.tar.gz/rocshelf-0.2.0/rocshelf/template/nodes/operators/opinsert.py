
import typing as _T

import rlogging
from rocshelf.compile.params import ProcessingParams
from rocshelf.template import areas, deconstruct, literals, main, node, nodes

logger = rlogging.get_logger('mainLogger')


class InsertNode(nodes.BaseOperatorNode):
    """ Структура вставки переменной """

    area = areas.ThisNodeArea

    @classmethod
    def literal_rule(cls):
        for point in ['i', 'insert']:
            yield literals.InLineOptionalStructureLiteral(
                'operators', cls,
                (point, None)
            )

    __slots__ = ('defaultValue', )
    defaultValue: str

    def _deconstruct(self, defaultValue: _T.Optional[str] = None) -> None:
        self.defaultValue = defaultValue

        if self.callParameter is None:
            logger.warning('Переданный в структуру "{0}" аргумент - пустой. Структура заменится на пустую строку'.format(
                self.__class__.__name__
            ))
            self.callParameter = '""'

    @classmethod
    def create(cls, literal: literals.LiteralValue):

        try:
            option = literal.contentMath.group('option')

        except IndexError:
            option = None

        newNode = cls(literal.content, literal.fileSpan)
        newNode.deconstruct(option)
        return newNode

    def _processing(self, proccParams: ProcessingParams) -> node.ProcessingOutputNode:
        try:
            callParameterValue = self.python_value(proccParams)

        except BaseException as exError:
            if self.defaultValue is None:
                raise exError

            callParameterValue = self.defaultValue

        textNode = nodes.TextNode(str(callParameterValue), self.fileSpan)
        textNode.deconstruct()

        self.subNodes = main.NodesList([textNode])

        return node.ProcessingOutputNode.from_node(self, proccParams)
