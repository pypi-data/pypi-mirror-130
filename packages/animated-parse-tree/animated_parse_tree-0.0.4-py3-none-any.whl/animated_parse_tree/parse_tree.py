from typing import Union
from .tree import Tree


class ParseTree(Tree):
    def __init__(self,
                 **kwargs):
        super().__init__(**kwargs)

    def evaluate(self) -> Union[int, float]:
        return 1
