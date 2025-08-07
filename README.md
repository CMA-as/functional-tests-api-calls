🐍 Prerequisites: installing Python
-------------

1. 👉 Go to the official Python website: https://www.python.org/downloads/windows/
2. Click the Download Python button (e.g., "Download Python 3.12.x").
3. Run the installer and wait for the installation to complete:
- ✅ Important: Check the box that says “Add Python to PATH” before clicking “Install Now.”
4. Check the installation was successful by typing the following in the Command Prompt
> python --version

or, if it doesn't work, type

> py --version

You should see something like Python 3.12.1


How to create a new parameter (Python version)
----------------------------

Follow instructions in "Prerequisites: installing Python"

Install needed packages
> py -m pip install requests

or, if it doesn't work, type

> pip install requests

Run the script from the commandline
> py .\creationOfNewParameter.py

Follow the prompts and insert the following information
- domain name
- name of the parameter
- data type (NUMERIC if a number, STRING if text)



How to check expressions
-----------------------

Install the required Python packages
> py -m pip install antlr4-python3-runtime

> py -m pip install antlr4-tools

Run script
> cd '.\creation of expressions\'
> py .\CheckCorrectnessOfExpression.py