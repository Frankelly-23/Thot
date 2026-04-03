
from scanner.token import Token

class Expr:
    def __init__(self):
        pass 

class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

