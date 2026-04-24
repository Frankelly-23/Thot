
from scanner.token import Token
from scanner.token import TokenType
from parser.expr import * 
from interpreter.stmt import * 

class ParseError(Exception): 
    pass

class Parser:
        
   def __init__(self, tokens: list[Token], is_relp: bool = False): 
       self.tokens = tokens   
       self.current: int = 0
       self.is_relp: bool = is_relp 
   
   def parse(self):
        
       statements: list[Stmt] = []   

       while not self._is_at_end():
            statements.append(self._declaration())  

       return statements      
   
   def _declaration(self):
       try: 
           if self._match(TokenType.LET): 
               return self._var_declaration()
           return self._statement()

       except ParseError: 
           self._syncronize() 

   def _statement(self):

       if self._match(TokenType.FOR):
           return self._for_statement()

       if self._match(TokenType.IF):
           return self._if_statement()

       if self._match(TokenType.PRINT): 
           return self._printStmt() 
       
       if self._match(TokenType.MIENTRAS): 
           return self._WhileStmt() 

       if self._match(TokenType.LEFT_BRACE):
           return Block(self._block())  

       return self._exprStatement()
           
   def _for_statement(self):
       self._consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.") 
       
       initializer = None  

       if self._match(TokenType.SEMICOLON): 
           initializer = None  
       elif self._match(TokenType.LET): 
           initializer = self._var_declaration()  
       else:  
           initializer = self._exprStatement() 
       
       condition: Expr | None = None 
        
       if self._check(TokenType.SEMICOLON): 
           condition = self.expression() 

       self._consume(TokenType.SEMICOLON, "Expect ';' after loop condition")   

       increment: Expr | None = None 
        
       if not self._check(TokenType.RIGHT_PAREN): 
           increment = self.expression() 
       self._consume(TokenType.RIGHT_PAREN, "Expect ')' after for closes")   

       body: Stmt = self._statement()

       if increment != None:
           body = Block([body, Expresion(increment)])
       
       if condition == None:
           condition = Literal(True)
       body = Mientras(condition, body) 

       if initializer != None:
           body = Block([initializer, body])

       return body

  
   def _WhileStmt(self): 

       self._consume(TokenType.LEFT_PAREN, "Expect '(' after 'mientras'.") 
       condition: Expr = self.expression() 
       self._consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.") 

       body: Stmt = self._statement()

       return Mientras(condition, body)


   def _if_statement(self):
       self._consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'")
       condition: Expr = self.expression() 
       self._consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition") 

       thenBranch: Stmt = self._statement()
       elseBranch: Stmt | None = None

       if self._match(TokenType.ELSE):
           elseBranch = self._statement()
       
       return If(condition, thenBranch, elseBranch)



   def _printStmt(self):

       value: Expr = self.expression() 
       self._consume(TokenType.SEMICOLON, "Expect ; after value")
       return Print(value) 

   def _exprStatement(self):

       expr: Expr = self.expression() 

       if self.is_relp and self._is_at_end():
           return Print(expr) 

       self._consume(TokenType.SEMICOLON, "Expect ; after expression")
       return Expresion(expr) 
   
   def _block(self):
       statements: list[Stmt] = [] 

       while not self._check(TokenType.RIGHT_BRACE) and not self._is_at_end():
            statements.append(self._declaration())
        
       self._consume(TokenType.RIGHT_BRACE, "Expect } after block.") 
       return statements

   def _var_declaration(self):
       name: Token = self._consume(TokenType.IDENTIFIER, "Expect variable name :)") 
       initializer: Expr | None = None 

       if self._match(TokenType.EQUAL):
           initializer = self.expression()      

       self._consume(TokenType.SEMICOLON, "Expect ; after declaration")  
       return Var(name, initializer)

        
   def _advance(self): 
       if not self._is_at_end():  
            self.current += 1   

       return self._previus()  

   def _previus(self): 
       return self.tokens[self.current - 1]   

   def _is_at_end(self):
       return self._peek().type == TokenType.EOF 

   def _peek(self): 
       return self.tokens[self.current]  

   def _check(self, Ttype: TokenType): 
        if self._is_at_end(): 
            return False
        return self._peek().type == Ttype 

   def _match(self, *Ttypes: TokenType): 
        for Ttype in Ttypes: 
            if self._check(Ttype): 
                self._advance()
                return True

        return False
    
   def _consume(self, Ttype: TokenType, message: str): 
        if self._check(Ttype):
            return self._advance()

        raise self._error(self._peek(), message)
   
   def _error(self, token: Token, msg):

       from errorUtils import error 
       error(token, msg) 
       
       return ParseError()
   
   def _syncronize(self):
       self._advance() 
       
       while not self._is_at_end():

           if self._previus().type == TokenType.SEMICOLON: 
               return  
           
           match self._peek().type:
            case ( TokenType.CLASS | TokenType.FN | TokenType.LET | 
                   TokenType.FOR | TokenType.IF | TokenType.MIENTRAS| 
                   TokenType.PRINT | TokenType.RETURN ):
               return 

           self._advance() 

   def expression(self):
        return self.assingment() 

   def assingment(self): 
        expr: Expr = self._or()  

        if self._match(TokenType.EQUAL):
            equals: Token = self._previus()
            value: Expr = self.assingment()

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)
                
            raise self._error(equals, "Invalid asingment target") 

        return expr 

   # Binary
   def _or(self):  
       expr: Expr = self._and()

       while self._match(TokenType.OR):
           operator: Token = self._previus()
           right: Expr = self._and()
           expr = Logical(expr, operator, right)

       return expr 

   def _and(self):
       expr: Expr = self.comma()
       
       while self._match(TokenType.AND):
           operator: Token = self._previus()
           right: Expr = self.equality()
           expr = Logical(expr, operator, right)
       
       return expr



   def comma(self): 
       expr: Expr = self.equality() 

       while self._match(TokenType.COMMA):
            operator = self._previus()  
            expr_right = self.equality() 
            expr = Binary(expr, operator, expr_right)
       return expr

   def equality(self):
        expr: Expr = self.comparison() 

        while self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
           operator: Token = self._previus() 
           exp_right: Expr = self.comparison()  
           expr = Binary(expr, operator, exp_right)
        
        return expr

   def comparison(self): 
       expr: Expr = self.term()  

       while self._match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
           operator: Token = self._previus()        
           exp_right: Expr = self.term()
           expr = Binary(expr, operator, exp_right)

       return expr 

   def term(self): 
       expr: Expr = self.factor()  
        
       while self._match(TokenType.MINUS, TokenType.PLUS): 
           operator: Token = self._previus() 
           exp_right: Expr = self.factor()
           expr = Binary(expr, operator, exp_right)

       return expr 

   def factor(self): 
       expr: Expr = self.unary()  
       
       while self._match(TokenType.SLASH, TokenType.STAR):
           operator: Token = self._previus() 
           exp_right: Expr = self.unary()
           expr = Binary(expr, operator, exp_right)
    
       return expr 

   def unary(self):

        if self._match(TokenType.BANG, TokenType.MINUS):
            operator: Token = self._previus()
            exp_right = self.unary()
            return Unary(operator, exp_right)

        expr: Expr = self.primary() 
        return expr 

   def primary(self): 

       if self._match(TokenType.ZERO): 
           return Literal(False)  

       if self._match(TokenType.ONE): 
           return Literal(True)  
       
       if self._match(TokenType.NADA):
           return Literal(None) 
       
       if self._match(TokenType.STRING, TokenType.NUMBER):
           return Literal(self._previus().literal) 
       
       if self._match(TokenType.IDENTIFIER):
           return Variable(self._previus()) 

       if self._match(TokenType.LEFT_PAREN):
           expr: Expr = self.expression() 
           self._consume(TokenType.RIGHT_PAREN, "Expected )")
           return Grouping(expr)

       if self._match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            self._error(self._previus(), "Missing left-hand operand.")
            self.comparison() 
            return None 

       if self._match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            self._error(self._previus(), "Missing left-hand operand.")
            self.term() 
            return None

       if self._match(TokenType.PLUS): 
            self._error(self._previus(), "Missing left-hand operand.")
            self.factor()
            return None

       if self._match(TokenType.STAR, TokenType.SLASH):
            self._error(self._previus(), "Missing left-hand operand.")
            self.unary()
            return None      

       raise self._error(self._peek(), "Expect expression.")

