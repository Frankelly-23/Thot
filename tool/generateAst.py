import sys

if len(sys.argv) != 2:
    sys.stdout.write("Usage: generate < output directory >")
    sys.exit(0)

output_dir = sys.argv[1]

grammar = [
 "Assign : name: Token, value: Expr",    
 "Binary : left: Expr, operator: Token, right: Expr",
 "Grouping : expression: Expr",
 "Literal : value: object",
 "Logical : left: Expr, operator: Token, right: Expr",
 "Unary : operator: Token, right: Expr",
 "Variable: name: Token"
] 

grammar2 = [
 "Block : statements: list[Stmt]",   
 "Expresion : expression: Expr",
 "If : condition: Expr, thenBranch: Stmt, elseBranch: Stmt",
 "Print : expression: Expr",
 "Var : name: Token, init: Expr",
 "Mientras : condition: Expr, body: Stmt",
] 

def defineType(file, base_n, class_n, fields):

    # child class
    file.write(f"class {class_n}({base_n}):\n") 

    # child class constructor
    file.write(f"\tdef __init__(self, {fields}):\n")
    fieldList = fields.split(", ")


    for field in fieldList:
        name = field.split(":")[0].strip()   
        Ptype = field.split(":")[1].strip()   
        file.write(f"\t\tself.{name}: {Ptype} = {name}\n")  

    file.write("\n")
    file.write("\tdef accept(self, visitor: 'Visitor'):\n")  
    file.write(f"\t\treturn visitor.visit_{class_n.lower()}_{base_n.lower()}(self)\n") 
    file.write("\n")

def defineVisitor(file, base_name,  grammar): 
    file.write("\n")

    file.write("class Visitor(ABC):\n")
    
    for string in grammar:
        class_name = string.split(":", 1)[0].strip()
        lbase_name = base_name.lower()
        file.write("\t@abstractmethod\n")
        file.write(f"\tdef visit_{class_name.lower()}_{lbase_name}(self, {lbase_name}: {class_name}):\n")
        file.write("\t\tpass\n")
        

def defineAst(output: str, base_name: str, grammar: list[str]):
    path = output + "/" + base_name.lower() + ".py"

    try:
        with open(path, "w") as file: 
            # vistitor interface 

            file.write("from abc import ABC, abstractmethod\n") 
            file.write("from scanner.token import Token\n") 

            if base_name == 'Stmt':
                file.write("from parser.expr import Expr\n")

            file.write("\n")

            file.write(f"class {base_name}(ABC):\n")
            file.write("\t@abstractmethod\n")
            file.write(f"\tdef accept(self, visitor: 'Visitor'):\n")
            file.write(f"\t\tpass\n")
            file.write("\n")

            for string in grammar:
                class_name = string.split(":", 1)[0].strip()
                fields = string.split(":", 1)[1].strip()
                defineType(file, base_name, class_name, fields)

            defineVisitor(file, base_name, grammar)
    except OSError as e:
        sys.stdout.write(f"{e}") 
        sys.exit(0) 
    
# defineAst(output_dir, "Expr", grammar)    
defineAst(output_dir, "Stmt", grammar2)    

