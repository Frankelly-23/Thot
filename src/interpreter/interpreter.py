
from parser.expr import *
from scanner.tokenType import TokenType
from typing import Any

class Interpreter(Visitor): 

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def _is_truthy(self, value: Any):
        return True if value else False  

    def visit_binary_expr(self, expr: Binary):

        left: Any = self.evaluate(expr.left)
        right: Any = self.evaluate(expr.right)

        match expr.operator.type:
            # aricmetic
            case TokenType.MINUS:
               return int(left) - int(right)

            case TokenType.PLUS:
                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)

                if isinstance(left, int) and isinstance(right, int):
                    return int(left) + int(right)

            case TokenType.SLASH:
               return int(left) / int(right)

            case TokenType.STAR:
               return int(left) * int(right)

            # comparison
            case TokenType.GREATER:
                return int(left) > int(right)

            case TokenType.LESS:
                return int(left) < int(right)

            case TokenType.GREATER_EQUAL:
                return int(left) >= int(right)

            case TokenType.LESS_EQUAL:
                return int(left) <= int(right)
            
            case TokenType.EQUAL_EQUAL:
                return left == right 

            case TokenType.BANG_EQUAL:
                return left != right 

        return None 

    def visit_unary_expr(self, expr: Unary):

        right: Any = self.evaluate(expr.right)
        match expr.operator.type:

            case TokenType.BANG:
                return not self._is_truthy(right)

            case TokenType.MINUS:
               return -int(right)
        return None

    def visit_grouping_expr(self, expr: Grouping):
        return self.evaluate(expr.expression) 

    def visit_literal_expr(self, expr: Literal):
        return expr.value
