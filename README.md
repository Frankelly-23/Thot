# Thot

An interpreter inspired by the book [Crafting Interpreters](https://craftinginterpreters.com/) by Robert Nystrom, implemented in Python. 

## Overview

Thot is a dynamically typed programming language. Its implementation includes a custom scanner (lexer), parser, and a tree-walking interpreter. It supports a mix of standard language features with a unique, customized set of keywords (such as `mientras`, `nada`, `zero`, and `one`).

## Features

- **Variables:** Declared using `let`.
- **Data Types:** Numbers, Strings, Booleans (`one` for true, `zero` for false), and Null (`nada`).
- **Control Flow:** 
  - `if` / `else`
  - `mientras` (while loops)
  - `for` loops
  - `break` and `continue`
- **Functions:** Declared using `fn`, with support for `return` ( feature on development ).
- **Classes:** Object-oriented support with `class`, `self`, and inheritance (`mother`) !!! (feature on development).
- **REPL:** Includes an interactive prompt for evaluating expressions on the fly.

## Usage

Thot requires Python 3 to run.

## Installation

run ./install.sh on your terminal to install all dependencies.

### Running a Script

To execute a `.thot` script file:

```bash
thot <path_to_script>

```

For example:
```bash
thot test/test.thot
```

### Interactive REPL

To start the interactive REPL (Read-Eval-Print Loop), simply run the main file without any arguments:

```bash
thot
```

You can exit the REPL by typing `exit` or using `Ctrl+C` / `Ctrl+D`.

## Example Code

```thot
// test/test.thot
let a = 4;
let temp;

mientras (a > 0) {
  print a; 
  a = a - 1;
}
```

## Project Structure

- `src/scanner/`: Contains the lexer, converting source code into tokens.
- `src/parser/`: Parses tokens into an Abstract Syntax Tree (AST).
- `src/interpreter/`: Evaluates the generated AST and manages environment state.
- `src/Thot.py`: The main entry point to start the REPL or execute a script file.
- `tool/`: Contains utility scripts (e.g., `generateAst.py` for generating AST classes).

---
*Note: This project is a custom exploration and extension of the concepts taught in Crafting Interpreters.*
