
from parser.expr import Visitor, Expr, Binary, Grouping, Literal, Unary
from scanner.token import Token
from scanner.tokenType import TokenType


expression: Expr = Binary(
        Unary(
            Token(TokenType.MINUS, "-", None, 1), 
            Literal(123)
            ),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(
            Literal(23.23)
            )
        ) 

class Ast_printer(Visitor):

    def print_exp(self, expr: Expr):
        return expr.accept(self) 

    def visit_binary_expr(self, expr: Binary):
        return self._parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: Grouping):
        return self._parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: Literal):
        if expr.value == None:
            return "nada"
        return str(expr.value)

    def visit_unary_expr(self, expr: Unary):
        return self._parenthesize(expr.operator.lexeme, expr.right)

    def _parenthesize(self, name: str, *exprs: Expr):
        result = f"({name}"

        for expr in exprs:
            result += " "
            result += f"{expr.accept(self)}"
        result += ")"
        return result
            


print(Ast_printer().print_exp(expression))
