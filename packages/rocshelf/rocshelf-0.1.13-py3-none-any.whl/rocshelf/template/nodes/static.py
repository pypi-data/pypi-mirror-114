""" Модуль для описания структур, которые предназначины для файлов статики (styles, scripts) """


from __future__ import annotations

import re

import rlogging
from rocshelf.compile.params import ProcessingParams
from rocshelf.template import areas, deconstruct, literals, main, node, nodes

logger = rlogging.get_logger('mainLogger')

contextTypes = {
    'style': 'file-style',
    'sass': 'file-style-sass',
    'script': 'file-script',
}


class ImportSassFileNode(node.Node):
    """ Нода указать на то, что обрабатываемому файлу нужен другой файл для выполнения скриптов.

    Заменяется на относительную ссылку до того файла.

    Так же целевой файл должен быть в папе, в которой происходит компиляция статики.

    """

    area = areas.ThisNodeArea

    @classmethod
    def literal_rule(cls):
        return literals.InLineStaticStructureLiteral(
            contextTypes['sass'], cls,
            ('import', 'sass')
        )

    def _deconstruct(self) -> None:
        targetFile = self.fileSpan.path().merge(
            self.callParameter
        )

        importNode = nodes.TextNode('@import url(\'{0}\');'.format(
            targetFile
        ))
        self.subNodes = main.NodesList([importNode])

    @classmethod
    def create(cls, litValue: literals.LiteralValue):
        newNode = cls(litValue.content, litValue.fileSpan)
        newNode.deconstruct()
        return newNode

    def _processing(self, proccParams: ProcessingParams) -> node.ProcessingOutputNode:
        return node.ProcessingOutputNode.from_node(self, proccParams)


class SectionNode(node.Node):
    """ Нода - разделение на секции  """

    area = areas.CloseNodeArea

    @classmethod
    def literal_rule(cls):
        for context in ['style', 'script']:
            yield literals.InTwoLineStaticStructureLiteral(
                contextTypes[context], cls,
                (cls.loadTime, None),
                (None, cls.loadTime)
            )

    __slots__ = ('loadTime', )

    loadTime: str

    @classmethod
    def create(cls, litValue: literals.LiteralValue, litValues: main.NodesList):
        return cls(litValue.content, litValue.fileSpan, litValues)

    def _processing(self, proccParams: ProcessingParams) -> node.ProcessingOutputNode:

        if proccParams.localVars['__meta__'].loadTime != self.loadTime:
            self.subNodes = None

        return node.ProcessingOutputNode.from_node(self, proccParams)


class PrependSectionNode(SectionNode):
    """ Нода секции кода, которая должна загружаться в начале страницы """

    loadTime = 'prep'


class FinalSectionNode(SectionNode):
    """ Нода секции кода, которая должна загружаться в начале страницы """

    loadTime = 'final'


class StaticInLineCommentLiteral(literals.CommentLiteral):
    """ Литерал для обозначения блока однострочного комментария в css/js разметке """

    def gen_patterns(self):
        self.patterns = (
            re.compile(r'\/\/\s*(?P<content>[^\n]*?)\n'),
            re.compile(r'\/\/\s*(?P<content>[^\n]*?)$'),
        )


class StaticMoreLineCommentLiteral(literals.CommentLiteral):
    """ Литерал для обозначения блока многострочного комментария в css/js разметке """

    def gen_patterns(self):
        self.patterns = (
            re.compile(r'\/\*\s*(?P<content>[\s\S]*?)\s*\*\/'),
        )


class StaticCommentNode(nodes.CommentNode):
    """ Нода закоментированного текста для html разметки """

    @classmethod
    def literal_rule(cls):
        for context in ['file-style-sass', 'file-script']:
            yield StaticInLineCommentLiteral(
                context, cls
            )

        for context in ['file-style', 'file-script']:
            yield StaticMoreLineCommentLiteral(
                context, cls
            )
