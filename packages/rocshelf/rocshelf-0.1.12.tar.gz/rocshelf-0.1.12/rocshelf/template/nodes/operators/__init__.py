""" Модуль структур. Узлы Стандартных операторов: insert, if, else, for

Предупреждение:
    Все нижеописанные структуры работают с переменными Python.
    Если при обработки ваш код выдаст исключение, то rocshelf остановит компиляцию всего приложения (кроме default insert).
    Ошибки по типу SyntaxError будут обнаружены почти сразу же,
    а ошибки вида TypeError, могут обнаружиться в самой последней структуре самого последнего файла и сломать все...

"""

import typing as _T

import rlogging
from rcore.strpython import ReturnValue
from rocshelf import exception as ex
from rocshelf.compile.params import ProcessingParams
from rocshelf.template import areas, deconstruct, literals, main, node, nodes

logger = rlogging.get_logger('mainLogger')

allowExceptions = (NameError, )


def python_value(contextVars: dict[str, _T.Any], condition: str) -> _T.Any:
    """ Фомирование python объекта по строке и локальным переменным

    Args:
        contextVars (dict[str, _T.Any]): Доступные переменные
        condition (str): Строковое представление значения

    Raises:
        rException: Ошибка произошедшая при компиляции страницы. Обернутая в ex.ex.rException.

    Returns:
        _T.Any: Результат выполнения строки condition

    """

    logger.debug('Выполнение условия "{0}" с локальными переменными: {1}'.format(
        condition,
        contextVars
    ))

    try:
        pythonValue = ReturnValue(contextVars, condition)

    except Exception as exError:
        logger.error('Выполнение условия "{0}" выдало исключение: "{1}"'.format(
            condition,
            exError
        ))
        raise ex.ex.rException(exError)

    logger.debug('Результат выполнения условия "{0}": {1}'.format(
        condition,
        pythonValue
    ))

    return pythonValue


class BaseOperatorNode(node.Node):
    """ Основа всех нод - опереторов """

    area = areas.CloseNodeArea

    def _exception(self, stage: str, exError: ex.rExError) -> ex.rExError:
        if stage == 'processing':
            exError.append_traceback(
                self.fileSpan.generate_traceback()
            )
        return exError

    @classmethod
    def create(cls, litValue: literals.LiteralValue, literals: main.NodesList):
        return cls(litValue.content, litValue.fileSpan, literals)

    def python_value(self, proccParams: ProcessingParams, condition: _T.Optional[str] = None) -> _T.Any:
        condition = self.callParameter if condition is None else condition
        return python_value(proccParams.localVars, condition)
