
from parser.expr import *
from scanner.tokenType import TokenType
from scanner.token import Token
from typing import Any
import sys
import errorUtils

class ThotRuntimeError(RuntimeError):

   def __init__(self, token: Token, message: str):
       super().__init__(message) 
       self.token = token
    
class Interpreter(Visitor): 
    
    def interpret(self, expression: Expr):
        try:
            value: Any = self.evaluate(expression)
            sys.stdout.write(f"{self._thotxify(value)}\n")

        except ThotRuntimeError as error:
            errorUtils.runtimeError(error) 
        
        
    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def _is_truthy(self, value: Any):
        return True if value else False  
    
    def _check_num_operand(self, operator: Token, operand: Any):
        if isinstance(operand, float):
            return

        raise ThotRuntimeError(operator, f"Operand must be numbers ")

    def _check_binary_operands(self, operator: Token, operand_right: Any, operand_left: Any):
    
        if isinstance(operand_right, float) and isinstance(operand_left, float):
            return

        raise ThotRuntimeError(operator, f"Operands must be numbers")
    
    def _thotxify(self, value: Any):

        if value == None:
            return 'nada'
        if value == True:
            return 'one'
        if value == False:
            return 'zero'

        if isinstance(value, float):
           if str(value).endswith(".0"): 
                return str(value)[0:-2] 
           else:
              return str(value)   
        return str(value) 

    def visit_binary_expr(self, expr: Binary):

        left: Any = self.evaluate(expr.left)
        right: Any = self.evaluate(expr.right)

        match expr.operator.type:
            # aricmetic
            case TokenType.MINUS:
               self._check_binary_operands(expr.operator, left, right)
               return float(left) - int(right)

            case TokenType.PLUS:
                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)

                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)

                raise ThotRuntimeError(expr.operator, "Operands must be strings | numbers") 

            case TokenType.SLASH:
               self._check_binary_operands(expr.operator, left, right)
               return float(left) / float(right)

            case TokenType.STAR:
               self._check_binary_operands(expr.operator, left, right)
               return float(left) * float(right)

            # comparison
            case TokenType.GREATER:
                self._check_binary_operands(expr.operator, left, right)
                return float(left) > float(right)

            case TokenType.LESS:
                self._check_binary_operands(expr.operator, left, right)
                return float(left) < float(right)

            case TokenType.GREATER_EQUAL:
                self._check_binary_operands(expr.operator, left, right)
                return float(left) >= float(right)

            case TokenType.LESS_EQUAL:
                self._check_binary_operands(expr.operator, left, right)
                return float(left) <= float(right)
            
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
               self._check_num_operand(expr.operator, right)
               return -float(right)
        return None

    def visit_grouping_expr(self, expr: Grouping):
        return self.evaluate(expr.expression) 

    def visit_literal_expr(self, expr: Literal):
        return expr.value
