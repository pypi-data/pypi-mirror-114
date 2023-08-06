""" Модуль html структур

"""

from __future__ import annotations

import re
import typing as _T

import rlogging
from rocshelf.compile.params import ProcessingParams
from rocshelf.template import areas, deconstruct, literals, main, node, nodes

logger = rlogging.get_logger('mainLogger')

CONTEXT_TYPE = 'file-html'


class HtmlTagLiteral(literals.Literal):
    """ Открывающая и закрывающая html тег структура """

    def gen_patterns(self):
        self.patterns = (
            re.compile(r'<(?P<content>(?P<tag>([\!][^\-])?[\w\-\_]+)(?P<attributes>[\s\S]*?)(\\)?)>'),
            re.compile(r'<\/(?P<content>(?P<tag>([\!][^\-])?[\w\-\_]+))>')
        )


class HtmlTagNodeArea(areas.CloseNodeArea):
    """ Область видимости - html tag """

    @classmethod
    def arealize(cls, litValues: list[_T.Union[literals.LiteralValue, node.Node]], thisIndex: int) -> _T.Optional[range]:

        callLitValue = litValues[thisIndex]

        if callLitValue.patterIndex == 1:
            return None

        logger.debug('Поиск закрывающего литерала для литерала "{0}"'.format(
            callLitValue
        ))

        startIndex = thisIndex
        stopIndex = None

        closeOpenCount = 1

        for literalIndex in range(thisIndex + 1, len(litValues)):
            litValue = litValues[literalIndex]

            if isinstance(litValue, node.Node):
                continue

            if litValue.literal.node != callLitValue.literal.node:
                continue

            if callLitValue.contentMath.group('tag') != litValue.contentMath.group('tag'):
                continue

            if litValue.patterIndex == 0:
                closeOpenCount += 1

            elif litValue.patterIndex == 1:
                closeOpenCount -= 1

            if closeOpenCount == 0:
                stopIndex = literalIndex
                break

        if stopIndex is None:
            return ClosingHtmlTagNode.create(callLitValue)

        startIndex += 1

        nodesList = deconstruct.Juxtaposition.juxtaposition_core(litValues[startIndex:stopIndex])

        newNode = HtmlTagNode.create(
            callLitValue, nodesList
        )

        return (
            range(startIndex, stopIndex),
            newNode
        )


tag_attributes_regex = {
    'attr_val_2': re.compile(r'\s*(?P<key>\w+)\s*=\s*"(?P<value>[^"]*)"\s*'),
    'attr_val_1': re.compile(r"\s*(?P<key>\w+)\s*=\s*'(?P<value>[^']*)'\s*"),
    'attr': re.compile(r'\s*(?P<key>[^\s]+)\s*')
}


class BaseHtmlTag(node.Node):
    """ Базовый класс html тегов """

    area = HtmlTagNodeArea

    @classmethod
    def literal_rule(cls):
        return HtmlTagLiteral(
            CONTEXT_TYPE, cls
        )

    __slots__ = ('tag', 'attributes')
    tag: _T.Optional[str]
    attributes: dict[str, _T.Optional[list]]

    def _deconstruct(self, litValue: literals.LiteralValue) -> None:
        self.tag = litValue.contentMath.group('tag')
        if self.tag in ('rocshelf-tag', '_'):
            self.tag = None

        self.deconstruct_attributes(litValue.contentMath.group('attributes'))

    def _processing(self, proccParams: ProcessingParams) -> node.ProcessingOutputNode:
        if self.tag is None:
            self.tag = 'rocshelf-tag'

        return node.ProcessingOutputNode.node(self, proccParams)

    def deconstruct_attributes(self, attributesString):
        """ Зазбор строки аттрибутов """

        attributes = {}

        stringLen = -1
        while stringLen != len(attributesString):
            stringLen = len(attributesString)

            for _, regexMatch in tag_attributes_regex.items():
                attributeMatch = regexMatch.match(attributesString)
                if attributeMatch is None:
                    continue

                attributesString = attributesString[attributeMatch.end():]

                attributeMatchDict = attributeMatch.groupdict()
                attributes[attributeMatchDict['key']] = attributeMatchDict.get('value', None)
                break

        for attributeName, attributeValue in attributes.items():
            if attributeValue is not None:
                attributes[attributeName] = attributeValue.split()

        self.attributes = attributes

    def compile_header(self, proccParams: ProcessingParams) -> str:
        """ Компиляция открывающего тега

        Args:
            proccParams (ProcessingParams): Параметры компиляции

        Returns:
            str: Открывающий тег

        """

        headerWords = [self.tag]

        for attributeName, attributeValue in self.attributes.items():
            if attributeValue is None:
                headerWords.append(attributeName)
            else:
                headerWords.append('{0}="{1}"'.format(
                    attributeName,
                    ' '.join(attributeValue)
                ))

        headerString = ' '.join(headerWords)

        headerStringNode = nodes.DevNode(headerString, literals.CONTEXT_TYPES)
        headerString = headerStringNode.processing(proccParams).compile(proccParams)

        return '<{0}>'.format(
            headerString
        )

    def compile_footer(self) -> str:
        """ Компиляция закрывающего тега

        Returns:
            str: Закрывающий тег

        """

        return '</{0}>'.format(
            self.tag
        )


class HtmlTagNode(BaseHtmlTag):
    """ Html тег требующий закрытие.

    Html тег указан.

    """

    @classmethod
    def create(cls, litValue: literals.LiteralValue, subNodes: main.NodesList):
        newNode = cls(litValue.content, litValue.fileSpan, main.NodesList(subNodes))
        newNode.deconstruct(litValue)
        return newNode

    def _compile(self, proccParams: ProcessingParams) -> str:

        resultString = self.compile_header(proccParams)

        for subItem in self.subNodes:
            resultString += subItem.compile(proccParams)

        resultString += self.compile_footer()

        return resultString


class ClosingHtmlTagNode(BaseHtmlTag):
    """ Html тег не требующий закрытие.

    Html тег указан.

    """

    @classmethod
    def create(cls, litValue: literals.LiteralValue):
        newNode = cls(litValue.content, litValue.fileSpan)
        newNode.deconstruct(litValue)
        return newNode

    def _compile(self, proccParams: ProcessingParams) -> str:
        return self.compile_header(proccParams)


class SwapHtmlTagNode(BaseHtmlTag):
    """ Нода HTML тега, который не имеет четкого типа (закрывающийся или нет) """

    def __init__(self, tag: _T.Optional[str] = None, subNodes: _T.Optional[main.NodesList] = None, attributes: _T.Optional[dict] = None):
        super().__init__()
        self.tag = tag
        self.subNodes = subNodes
        self.attributes = attributes if attributes else {}


class HtmlCommentLiteral(literals.CommentLiteral):
    """ Литерал закоментированного текста для html разметки """

    def gen_patterns(self):
        self.patterns = (
            re.compile(r'<!--(?P<content>[\s\S]*?)-->'),
        )


class HtmlCommentNode(nodes.CommentNode):
    """ Нода закоментированного текста для html разметки """

    @classmethod
    def literal_rule(cls):
        return HtmlCommentLiteral(
            CONTEXT_TYPE, cls
        )
