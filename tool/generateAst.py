import sys

if len(sys.argv) != 2:
    sys.stdout.write("Usage: generate < output directory >")
    sys.exit(0)

output_dir = sys.argv[1]

grammar = [
 "Binary : left: Expr, operator: Token, right: Expr",
 "Grouping : expression: Expr",
 "Literal : value: object",
 "Unary : operator: Token, right: Expr"
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

def defineAst(output: str, base_name: str, grammar: list[str]):
    path = output + "/" + base_name + ".py"

    try:
        with open(path, "w") as file: 
            file.write("from scanner.token import Token\n") 
            file.write("\n")
            file.write(f"class {base_name}:\n")
            file.write(f"\tdef __init__(self):\n")
            file.write(f"\t\tpass\n")
            file.write("\n")

            for string in grammar:
                class_name = string.split(":", 1)[0].strip()
                fields = string.split(":", 1)[1].strip()
                defineType(file, base_name, class_name, fields)

    except OSError as e:
        sys.stdout.write(f"{e}") 
        sys.exit(0) 
    
defineAst(output_dir, "Expr", grammar)    
