from .node import Node


class Tree:
    def __init__(self,
                 root: Node = None,
                 left_branch: str = '/',
                 middle_branch: str = '|',
                 right_branch: str = '\\'):
        self.root = None

    def __str__(self):
        pass

    def __call__(self):
        pass