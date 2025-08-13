from antlr4 import *
from ./GrammarLexer import GrammarLexer
from GrammarParser import GrammarParser
import sys
import subprocess
import os

print("Hello! Let's check your expression 😊")
print("I am going to build the Grammar first. If I need your help, I will ask your input")



python_path = sys.executable
antlr_path = os.path.join(os.path.dirname(python_path), "Scripts", "antlr4.exe")
print(f"🔍 Looking for ANTLR at: {antlr_path}")


#building the grammar

command = [
    antlr_path,
    "-Dlanguage=Python3",
    "Grammar.g4"
]

try:
    subprocess.run(command, check=True)
    print("ANTLR ran successfully.")
except subprocess.CalledProcessError as e:
    print("ANTLR command failed:", e)
except FileNotFoundError:
    print("antlr4.exe not found. Check the path and try again.")


# Read input from the command line
expression = input("Enter expression: ")

input_stream = InputStream(expression)
lexer = GrammarLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = GrammarParser(token_stream)
tree = parser.start()

print("\n🎉 All done! Your expression is valid according to the grammar.")


def check_correctness(expression):
    input_stream = InputStream(expression)
    lexer = GrammarLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = GrammarParser(token_stream)
    tree = parser.start()

    #TODO: add return
    return True
