from abc import ABC, abstractmethod
from scanner.token import Token
from parser.expr import Expr

class Stmt(ABC):
	@abstractmethod
	def accept(self, visitor: 'Visitor'):
		pass

class Expresion(Stmt):
	def __init__(self, expression: Expr):
		self.expression: Expr = expression

	def accept(self, visitor: 'Visitor'):
		return visitor.visit_expresion_stmt(self)

class Print(Stmt):
	def __init__(self, expression: Expr):
		self.expression: Expr = expression

	def accept(self, visitor: 'Visitor'):
		return visitor.visit_print_stmt(self)

class Var(Stmt):
	def __init__(self, name: Token, init: Expr):
		self.name: Token = name
		self.init: Expr = init

	def accept(self, visitor: 'Visitor'):
		return visitor.visit_var_stmt(self)


class Visitor(ABC):
	@abstractmethod
	def visit_expresion_stmt(self, stmt: Expresion):
		pass
	@abstractmethod
	def visit_print_stmt(self, stmt: Print):
		pass
	@abstractmethod
	def visit_var_stmt(self, stmt: Var):
		pass
