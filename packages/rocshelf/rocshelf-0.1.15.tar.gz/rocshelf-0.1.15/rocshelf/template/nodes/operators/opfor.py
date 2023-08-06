import re
import typing as _T
from copy import deepcopy

import rlogging
from rocshelf import exception as ex
from rocshelf.compile.params import ProcessingParams
from rocshelf.template import areas, deconstruct, literals, main, node, nodes

logger = rlogging.get_logger('mainLogger')


class ForNode(nodes.BaseOperatorNode):
    """ Структура цикла """

    __slots__ = ('iterableCondition', 'newVars')

    iterableCondition: str
    newVarsNames: tuple[str]

    @classmethod
    def literal_rule(cls):
        return literals.InTwoLineStructureLiteral(
            'operators', cls,
            ('for', None),
            (None, 'for')
        )

    __slots__ = ('sections', )

    sections: dict[str, list]

    def parse_condition(self):
        """ Разбивка условия цикла на подобный python синтаксис """

        logger.debug('Выборка переменных и итерируемого значения для ноды "{0}" из строки "{1}"'.format(
            self.__class__.__name__,
            self.callParameter
        ))

        try:
            (newVarsNames, self.iterableCondition) = [i.strip() for i in self.callParameter.split('in')]
            self.newVarsNames = re.split(r',\s*', newVarsNames)

            for i in self.newVarsNames:
                if i.find(' ') != -1:
                    raise ValueError

        except ValueError as exError:
            logger.warning('Заголовок структуры "{0}" при обработки выдал исключение: "{1}"'.format(
                self.__class__.__name__,
                exError
            ))
            raise SyntaxError('For structure must follow python syntax')

        logger.debug('Результат выборки. Новые переменные {0} из итерируемой {1}'.format(
            self.newVarsNames,
            self.iterableCondition
        ))

    def _deconstruct(self) -> None:
        self.parse_condition()

        self.sections = {
            'true': [],
            'else': []
        }

        for subNode in self.subNodes:
            if isinstance(subNode, nodes.ElseNode):
                self.sections['else'].append(subNode)

            else:
                self.sections['true'].append(subNode)

    @classmethod
    def create(cls, litValue: literals.LiteralValue, litValues: main.NodesList):
        newNode = cls(litValue.content, litValue.fileSpan, litValues)
        newNode.deconstruct()
        return newNode

    def __iterable(self, proccParams: ProcessingParams, iterVar: _T.Iterable):
        newNodesList = []

        for anyItems in iterVar:

            localVars = {}

            if len(self.newVarsNames) == 1:
                localVars[self.newVarsNames[0]] = anyItems

            else:
                for (VarName, varValue) in zip(self.newVarsNames, anyItems):
                    localVars[VarName] = varValue

            localProccParams = deepcopy(proccParams)
            localProccParams.localVars.update(localVars)

            newNode = node.Node(fileSpan=self.fileSpan)
            newNode.subNodes = deepcopy(self.sections['true'])
            newNode.proccParams = localProccParams
            newNodesList.append(newNode)

        self.subNodes = main.NodesList(newNodesList)

    def _processing(self, proccParams: ProcessingParams) -> node.ProcessingOutputNode:
        iterVar = self.python_value(proccParams, self.iterableCondition)

        if not iterVar:
            self.subNodes = main.NodesList(deepcopy(self.sections['else']))
            return node.ProcessingOutputNode.from_node(self, proccParams)

        if not isinstance(iterVar, _T.Iterable):
            raise ex.SyntaxTemplateError('Передаваемое в конструкцию цикла значение, должно быть итерируемым, или == False')

        self.__iterable(proccParams, iterVar)

        return node.ProcessingOutputNode.from_node(self, proccParams)
