from __future__ import annotations

import typing as _T
from copy import copy

import rlogging
from rocshelf import exception as ex
from rocshelf.compile.params import ProcessingParams
from rocshelf.template import areas, deconstruct, literals, main, node, nodes

logger = rlogging.get_logger('mainLogger')


class MergedHtmlTags(object):
    """ Класс-группировка функций для слияния двух тегов """

    __merge_attrs = ['class']

    fromTagSubTags: dict[str, ShelfSubTagNode]

    @classmethod
    def safe_merge(cls, targetTag: _T.Union[nodes.BaseHtmlTag, ShelfTagNode], fromTag: _T.Union[nodes.BaseHtmlTag, ShelfTagNode]) -> nodes.BaseHtmlTag:
        """ Поиск и передача тегов в класс слияния тегов

        Args:
            targetTag (nodes.BaseHtmlTag): Тег, в который будет вставлен новый тег
            fromTag (_T.Union[nodes.BaseHtmlTag, ShelfTagNode]): Тег, который будет вставлен

        Returns:
            nodes.BaseHtmlTag: Новый тег

        """

        targetHtmlTag = None
        fromHtmlTag = None

        if isinstance(targetTag, nodes.BaseHtmlTag):
            targetHtmlTag = targetTag
            targetTag = None

        elif isinstance(targetTag, ShelfTagNode):
            targetHtmlTag = targetTag.htmlTagNode

        if isinstance(fromTag, nodes.BaseHtmlTag):
            fromHtmlTag = fromTag
            fromTag = None

        elif isinstance(fromTag, ShelfTagNode):
            fromHtmlTag = fromTag.htmlTagNode

        if targetHtmlTag is None or fromHtmlTag is None:
            raise ex.ex.errors.DeveloperIsShitError(type(targetHtmlTag, fromHtmlTag))

        return cls().merge(targetHtmlTag, fromHtmlTag, targetTag, fromTag)

    def gen_new_tag_type(self, targetHtmlTag, fromHtmlTag) -> type[nodes.BaseHtmlTag]:
        """ Определение типа будущего html тега

        Args:
            targetHtmlTag ([type]): [description]
            fromHtmlTag ([type]): [description]

        Returns:
            type[nodes.BaseHtmlTag]: Тип нового тега

        """

        if not isinstance(targetHtmlTag, nodes.SwapHtmlTagNode):
            return type(targetHtmlTag)

        elif isinstance(fromHtmlTag, nodes.SwapHtmlTagNode):
            return type(fromHtmlTag)

        return nodes.HtmlTagNode

    def merge(
        self,
        targetHtmlTag: nodes.BaseHtmlTag,
        fromHtmlTag: nodes.BaseHtmlTag,
        targetTag: _T.Optional[ShelfTagNode],
        fromTag: _T.Optional[ShelfTagNode],
    ) -> nodes.BaseHtmlTag:
        """ Слияние двух html tag нод.

        Args:
            targetHtmlTag (nodes.BaseHtmlTag): Html тег для слияния. Параметры этого тега будут заменяться на параметры fromHtmlTag.
            fromHtmlTag (nodes.BaseHtmlTag): Html тег для слияния. Параметры этого тега будут заменять параметры targetHtmlTag.
            targetTag (_T.Optional[ShelfTagNode]): Shelf тег, из которого взят html тег targetHtmlTag.
            fromTag (_T.Optional[ShelfTagNode]): Shelf тег, из которого взят html тег fromHtmlTag.

        Returns:
            nodes.BaseHtmlTag: Узел нового тега

        Raises:
            SyntaxTemplateError: Попытка слить два разных типа html тегов.

        """

        newTagType = self.gen_new_tag_type(targetHtmlTag, fromHtmlTag)

        newTag = newTagType()

        newTag.tag = self.merge_tag(targetHtmlTag.tag, fromHtmlTag.tag)
        newTag.attributes = self.merge_attrs(targetHtmlTag.attributes, fromHtmlTag.attributes)

        self.merge_shelf_params(newTag, targetTag, fromTag)
        self.merge_subtags(newTag, targetTag, fromTag)

        if isinstance(newTag, nodes.HtmlTagNode):
            targetSubNodes = targetHtmlTag.subNodes
            if isinstance(targetHtmlTag, nodes.ClosingHtmlTagNode):
                targetSubNodes = []

            newTag.subNodes = self.merge_content_recursion(targetSubNodes, fromHtmlTag.subNodes)

        newTag.proccParams = ProcessingParams({
            'shelf_tag_content': fromHtmlTag.subNodes
        })

        return newTag

    def merge_subtags(self, newNode: node.Node, targetTag: _T.Optional[ShelfTagNode], fromTag: _T.Optional[ShelfTagNode]):
        """ Слияние под тегов у нод shelf-тега

        Args:
            newNode (node.Node): Надо в которую перенесутся все данные.
            targetTag (_T.Optional[ShelfTagNode]): Узел для слияния.
            fromTag (_T.Optional[ShelfTagNode]): Узел для слияния.

        """

        self.fromTagSubTags = {}

        if targetTag is not None:
            self.fromTagSubTags = targetTag.subTags

        if fromTag is not None:
            self.fromTagSubTags.update(
                fromTag.subTags
            )

        if isinstance(newNode, ShelfTagNode):
            newNode.subTags = self.fromTagSubTags

    def merge_shelf_params(self, newNode: node.Node, targetTag: _T.Optional[ShelfTagNode], fromTag: _T.Optional[ShelfTagNode]):
        """ Слияние данных компиляции.

        Args:
            newNode (node.Node): Надо в которую перенесутся все данные.
            targetTag (_T.Optional[ShelfTagNode]): Узел для слияния.
            fromTag (_T.Optional[ShelfTagNode]): Узел для слияния.

        """

    def merge_tag(self, targetHtmlTag: _T.Optional[str], fromTag: _T.Optional[str]):
        """ Слияние тегов """

        if fromTag is not None:
            return fromTag
        return targetHtmlTag

    def merge_attrs(self, inAttributes: dict[str, _T.Optional[list]], fromAttributes: dict[str, _T.Optional[list]]) -> dict[str, _T.Optional[list]]:
        """ Слияние атрибутов """

        newAttributes = copy(inAttributes)

        for attributeName, attributeValue in fromAttributes.items():
            if attributeName in self.__merge_attrs:
                newAttributes[attributeName] += attributeValue
            else:
                newAttributes[attributeName] = attributeValue

        return newAttributes

    def merge_content_recursion(self, inSubNodes: main.NodesList, fromSubNodes: main.NodesList) -> main.NodesList:
        newNodes = []

        for iterNode in inSubNodes:
            if isinstance(iterNode, ShelfTagPlaceNode):
                wrapperNode = node.Node()
                wrapperNode.subNodes = fromSubNodes
                newNodes.append(wrapperNode)
                continue

            elif isinstance(iterNode, ShelfSubTagNode):
                newTag = MergedHtmlTags.safe_merge(
                    iterNode.htmlTagNode,
                    self.fromTagSubTags[iterNode.callParameter].htmlTagNode
                )
                newNodes.append(newTag)
                continue

            elif isinstance(iterNode, ShelfTagNode):
                pass

            elif iterNode.subNodes is not None:
                iterNode.subNodes = self.merge_content_recursion(iterNode.subNodes, fromSubNodes)

            newNodes.append(iterNode)

        return main.NodesList(newNodes)


class ShelfTagNode(nodes.ShelfNode):
    """ Нода шелфа-тега """

    area = areas.NextNodeArea

    @classmethod
    def literal_rule(cls):
        return literals.InLineStructureLiteral(
            'shelves', cls,
            ('tag', None),
        )

    __slots__ = ('htmlTagNode', 'subTags')
    htmlTagNode: _T.Union[nodes.BaseHtmlTag, ShelfTagNode]
    subTags: dict[str, ShelfSubTagNode]

    def _deconstruct(self, nextNode: node.Node) -> None:
        super()._deconstruct('tag', self.callParameter)

        self.deconstruct_tag(nextNode)

        self.subTags = {}
        if isinstance(self.htmlTagNode, (nodes.HtmlTagNode, nodes.SwapHtmlTagNode)):
            self.htmlTagNode.subNodes = self.deconstruct_sub_tags(self.htmlTagNode.subNodes)

    def deconstruct_tag(self, nextNode: node.Node) -> None:
        if isinstance(nextNode, nodes.BaseHtmlTag):
            self.htmlTagNode = nextNode

        elif isinstance(nextNode, ShelfTagNode):
            htmlTagNode = nodes.DevNode('<_></_>', ['file-html']).subNodes.nodes[0]
            htmlTagNode.subNodes = main.NodesList([nextNode])
            self.htmlTagNode = htmlTagNode

        elif isinstance(nextNode, (nodes.TextNode, ShelfTagPlaceNode)):
            htmlTagNode = nodes.SwapHtmlTagNode(
                subNodes=main.NodesList([nextNode])
            )
            self.htmlTagNode = htmlTagNode

        else:
            raise ex.ex.errors.DeveloperIsShitError(str(nextNode))

    def deconstruct_sub_tags(self, subNodes: main.NodesList):
        """ Поиск дочерних тегов """

        newNodes = []

        for iterNode in subNodes:
            if isinstance(iterNode, ShelfSubTagNode):
                self.subTags[iterNode.callParameter] = iterNode
                continue

            elif isinstance(iterNode, ShelfTagNode):
                pass

            elif iterNode.subNodes is not None:
                iterNode.subNodes = self.deconstruct_sub_tags(iterNode.subNodes)

            newNodes.append(iterNode)

        return main.NodesList(newNodes)

    @classmethod
    def create(cls, litValue: literals.LiteralValue, nextNode: node.Node):
        logger.debug('Создание "{0}" со значением имен: "{1}"'.format(
            cls.__name__,
            litValue.content
        ))

        shelfNames = litValue.content.split()

        if not shelfNames:
            raise ex.SyntaxTemplateError('Tag Shelf должен принимать минимум 1 параметр [имя шелфа]')

        shelfNode = cls(shelfNames[-1], litValue.fileSpan)
        shelfNode.deconstruct(nextNode)

        if len(shelfNames) == 1:
            return shelfNode

        for shelfName in shelfNames[::-1][1:]:
            subNode = cls(shelfName, litValue.fileSpan)
            subNode.deconstruct(shelfNode)

            shelfNode = subNode

        newNode = node.Node(litValue.content, litValue.fileSpan)
        newNode.subNodes = main.NodesList([
            shelfNode
        ])

        return newNode

    def __find_html_tag(self) -> _T.Union[nodes.BaseHtmlTag, ShelfTagNode]:
        """ Поиск в файле шелфа html тег """

        logger.debug('Поиск html тег (shelf html тег) в шелф файле "{0}"'.format(
            self.decFile
        ))

        targetHtmltagNode = None

        for subNode in self.shelfFileNodes:
            if isinstance(subNode, (nodes.BaseHtmlTag, ShelfTagNode)):
                targetHtmltagNode = subNode
                break

            elif not (isinstance(subNode, nodes.CommentNode) or (isinstance(subNode, nodes.TextNode) and subNode.callParameter == '')):
                logger.error('Shelf-tag содержит не подходящую ноду: {0}'.format(
                    subNode
                ))
                raise ex.SyntaxTemplateError('Shelf-tag должен содержать только html тег')

        if targetHtmltagNode is None:
            raise ex.SyntaxTemplateError('Shelf-tag должен содержать любой html тег')

        logger.debug('В шелф-файле "{0}" найден тег типа: "{1}"'.format(
            self.decFile,
            type(targetHtmltagNode)
        ))

        return targetHtmltagNode

    def _processing(self, proccParams: ProcessingParams) -> node.ProcessingOutputNode:
        super()._processing()

        targetHtmltagNode = self.__find_html_tag()

        newHtmltagNode = MergedHtmlTags.safe_merge(targetHtmltagNode, self)

        self.htmlTagNode = newHtmltagNode
        self.subNodes = main.NodesList([newHtmltagNode])

        return node.ProcessingOutputNode.from_node(self, proccParams, {
            'shelves': [str(self.shelfItem)]
        })


class ShelfSubTagNode(ShelfTagNode):
    """ Нода шелфа-тега """

    @classmethod
    def literal_rule(cls):
        return literals.InLineStructureLiteral(
            'shelves', cls,
            ('t', None),
        )

    def _deconstruct(self, nextLitValue: node.Node) -> None:
        self.deconstruct_tag(nextLitValue)
        self.subNodes = main.NodesList([
            self.htmlTagNode
        ])

    def _processing(self, proccParams: ProcessingParams) -> node.ProcessingOutputNode:
        return node.ProcessingOutputNode.from_node(self, proccParams)


class ShelfTagPlaceNode(node.Node):
    """ Нода места для вставки секций шелфа-обертки """

    area = areas.ThisNodeArea

    @classmethod
    def literal_rule(cls):
        for tagPoint in ['t', 'tag']:
            for placePoint in ['p', 'place']:
                yield literals.InLineStructureLiteral(
                    'shelves', cls,
                    (tagPoint, placePoint),
                )

    @classmethod
    def create(cls, litValue: literals.LiteralValue):
        return cls(None, litValue.fileSpan)

    def _processing(self, proccParams: ProcessingParams) -> node.ProcessingOutputNode:
        return node.ProcessingOutputNode.node(self, proccParams)

    def _compile(self, proccParams: ProcessingParams) -> str:
        wrapperNode = node.Node()
        wrapperNode.subNodes = proccParams.localVars.get('shelf_tag_content', 'ShelfTagPlaceNode')
        return wrapperNode.processing(proccParams).compile(proccParams)
