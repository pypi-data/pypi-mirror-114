
from copy import deepcopy

import rlogging
from rocshelf.compile.params import ProcessingParams
from rocshelf.template import areas, deconstruct, literals, main, node, nodes

logger = rlogging.get_logger('mainLogger')


class IfNode(nodes.BaseOperatorNode):
    """ Структура условия """

    @classmethod
    def literal_rule(cls):
        return literals.InTwoLineStructureLiteral(
            'operators',
            cls,
            ('if', None),
            (None, 'if')
        )

    __slots__ = ('sections', )

    sections: dict[str, list]

    def _deconstruct(self) -> None:
        self.sections = {
            'true': [],
            'else': []
        }

        for subNode in self.subNodes:
            if isinstance(subNode, ElseNode):
                self.sections['else'].append(subNode)

            else:
                self.sections['true'].append(subNode)

    @classmethod
    def create(cls, litValue: literals.LiteralValue, litValues: main.NodesList):
        newNode = cls(litValue.content, litValue.fileSpan, litValues)
        newNode.deconstruct()
        return newNode

    def _processing(self, proccParams: ProcessingParams) -> node.ProcessingOutputNode:
        callParameterValue = self.python_value(proccParams)

        if callParameterValue:
            subNodes = deepcopy(self.sections['true'])

        else:
            subNodes = deepcopy(self.sections['else'])

        self.subNodes = main.NodesList(subNodes)

        return node.ProcessingOutputNode.from_node(self, proccParams)


class ElseNode(IfNode):
    """ Структура условия else """

    @classmethod
    def literal_rule(cls):
        for point in ['else', 'elif']:
            yield literals.InTwoLineStructureLiteral(
                'operators',
                cls,
                (point, None),
                (None, point)
            )

    def _processing(self, proccParams: ProcessingParams) -> node.ProcessingOutputNode:
        if self.callParameter is None:
            return node.ProcessingOutputNode.from_node(self, proccParams)

        return super()._processing(proccParams)
