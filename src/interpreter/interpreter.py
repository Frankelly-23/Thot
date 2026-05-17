
from typing import Any

from parser.expr import *
from scanner.token import Token
from scanner.tokenType import TokenType
from scanner.keywords import *

from interpreter.environment import Environment
from interpreter.stmt import Visitor as VisitorStmt, Print, Expresion, Stmt, Var, Block, If, Mientras, Continue, Break

import errorUtils

    
class Interpreter(Visitor, VisitorStmt): 
    _environment = Environment() 

    def interpret(self, statements: list[Stmt]):

        try:
            for statement in statements:
                self._execute(statement)

        except errorUtils.ThotRuntimeError as error:
            errorUtils.runtimeError(error) 
        
    def _execute(self, stmt: Stmt): 
       stmt.accept(self) 
    
    def _execute_block(self, statements: list[Stmt], environment: Environment):
        previous: Environment = self._environment

        try: 
            self._environment = environment
            for statement in statements:
                self._execute(statement)
        finally:
            self._environment = previous
        
    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def _is_truthy(self, value: Any):
        return True if value else False  
    
    def _check_num_operand(self, operator: Token, operand: Any):
        if isinstance(operand, float):
            return

        raise errorUtils.ThotRuntimeError(operator, f"Operand must be numbers ")

    def _check_binary_operands(self, operator: Token, operand_right: Any, operand_left: Any):
    
        if isinstance(operand_right, float) and isinstance(operand_left, float):
            return

        raise errorUtils.ThotRuntimeError(operator, f"Operands must be numbers")
    
    def _thotxify(self, value: Any):

        if isinstance(value, bool):        
            if value == True:
                return 'one'
            if value == False:
                return 'zero'

        if value == None:
            return 'nada'

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

                if isinstance(left, float):
                    return str(int(left)) + str(right)
                        
                if isinstance(right, float):
                    return str(left) + str(int(right))

                raise errorUtils.ThotRuntimeError(expr.operator, "Operands must be strings | numbers") 

            case TokenType.SLASH:
               self._check_binary_operands(expr.operator, left, right)

               if float(right) != 0:
                    return float(left) / float(right)

               return None  

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
    
    def visit_expresion_stmt(self, stmt: Expresion):
        self.evaluate(stmt.expression) 

    def visit_print_stmt(self, stmt: Print):
        value: Any = self.evaluate(stmt.expression)
        print(self._thotxify(value))
    

    def visit_var_stmt(self, stmt: Var):
        value: Any = None 
        
        if stmt.init != None:
            value = self.evaluate(stmt.init)
        
        self._environment._define(stmt.name.lexeme, value)
        return None
        
    def visit_variable_expr(self, expr: Variable):

        return self._environment._get(expr.name)

    def visit_assign_expr(self, expr: Assign):
        value: Any = self.evaluate(expr.value)

        self._environment._assing(expr.name, value)
        return value
         
    def visit_block_stmt(self, stmt: Block):
        self._execute_block(stmt.statements, Environment(self._environment))
        return None

    def visit_if_stmt(self, stmt: If):

        if self._is_truthy(self.evaluate(stmt.condition)):        
            self._execute(stmt.thenBranch) 

        elif stmt.elseBranch != None:
            self._execute(stmt.elseBranch)

        return None
    
    def visit_logical_expr(self, expr: Logical):
        left: Any = self.evaluate(expr.left)

        if expr.operator.type == TokenType.OR:
            if self._is_truthy(left):
                return left
        else: 
            if not self._is_truthy(left):
                return left

        return self.evaluate(expr.right)

    def visit_mientras_stmt(self, stmt: Mientras):
        while self._is_truthy(self.evaluate(stmt.condition)):
            try:     
                self._execute(stmt.body)  
            except errorUtils.BreakException: 
                break
            except errorUtils.ContinueException: 
                continue 

        return None
    
    def visit_break_stmt(self, stmt: Break):
        raise errorUtils.BreakException()

    def visit_continue_stmt(self, stmt: Continue):
        raise errorUtils.ContinueException()
