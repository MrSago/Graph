
""" Модуль модели (Model) предоставляет данные и реагирует
    на команды контроллера (Controller), изменяя своё состояние.
"""



from .Graph import Graph
from .Render import *


class GraphModel():
    """Класс модели (Model)."""
    def __init__(self):
        """ Инициализация класса.

            Attributes:
                graph (Graph): Экземпляр класса Graph.
                functions (dict): Словарь функций.
        """
        self.graph = Graph()
        self.functions = {
            drawDefault.__name__: drawDefault,
            drawColoring.__name__: drawColoring,
            drawMinPath.__name__: drawMinPath
        }

