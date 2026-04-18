from typing import Any
from parser.expr import *
from errorUtils import ThotRuntimeError

class Environment():
    _values: dict[str, Any] = {}
    
    def _get(self, name: Token):
    
        if name.lexeme in self._values: 
            return self._values.get(name.lexeme)

        raise ThotRuntimeError(name, f"Undefined variable '{name.lexeme}'") 

    def _define(self, name: str, value: Any):
        self._values[name] = value 
