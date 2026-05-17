from abc import ABC, abstractmethod
from scanner.token import Token
from parser.expr import Expr

class Stmt(ABC):
	@abstractmethod
	def accept(self, visitor: 'Visitor'):
		pass

class Block(Stmt):
	def __init__(self, statements: list[Stmt]):
		self.statements: list[Stmt] = statements

	def accept(self, visitor: 'Visitor'):
		return visitor.visit_block_stmt(self)

class Expresion(Stmt):
	def __init__(self, expression: Expr):
		self.expression: Expr = expression

	def accept(self, visitor: 'Visitor'):
		return visitor.visit_expresion_stmt(self)

class If(Stmt):
	def __init__(self, condition: Expr, thenBranch: Stmt, elseBranch: Stmt):
		self.condition: Expr = condition
		self.thenBranch: Stmt = thenBranch
		self.elseBranch: Stmt = elseBranch

	def accept(self, visitor: 'Visitor'):
		return visitor.visit_if_stmt(self)

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

class Mientras(Stmt):
	def __init__(self, condition: Expr, body: Stmt):
		self.condition: Expr = condition
		self.body: Stmt = body

	def accept(self, visitor: 'Visitor'):
		return visitor.visit_mientras_stmt(self)

class Break(Stmt):

	def accept(self, visitor: 'Visitor'):
		return visitor.visit_break_stmt(self)

class Continue(Stmt):

	def accept(self, visitor: 'Visitor'):
		return visitor.visit_continue_stmt(self)


class Visitor(ABC):
	@abstractmethod
	def visit_block_stmt(self, stmt: Block):
		pass
	@abstractmethod
	def visit_expresion_stmt(self, stmt: Expresion):
		pass
	@abstractmethod
	def visit_if_stmt(self, stmt: If):
		pass
	@abstractmethod
	def visit_print_stmt(self, stmt: Print):
		pass
	@abstractmethod
	def visit_var_stmt(self, stmt: Var):
		pass
	@abstractmethod
	def visit_mientras_stmt(self, stmt: Mientras):
		pass
	@abstractmethod
	def visit_break_stmt(self, stmt: Break):
		pass
	@abstractmethod
	def visit_continue_stmt(self, stmt: Continue):
		pass
