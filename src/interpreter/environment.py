from typing import Any
from parser.expr import *
from errorUtils import ThotRuntimeError

class Environment():
    
    def __init__(self, enclosing: 'Environment | None' = None):
        self.enclosing = enclosing 
        self._values: dict[str, Any] = {}

    def _get(self, name: Token):
    
        if name.lexeme in self._values: 
            return self._values.get(name.lexeme)
        
        if self.enclosing != None: 
            return self.enclosing._get(name)

        raise ThotRuntimeError(name, f"Undefined variable '{name.lexeme}'") 

    def _define(self, name: str, value: Any):
        self._values[name] = value 

    def _assing(self, name: Token, value: Any):
        
        if name.lexeme in self._values:
            self._values[name.lexeme] = value
            return

        if self.enclosing != None: 
            self.enclosing._assing(name, value)
            return 

        raise ThotRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
        
