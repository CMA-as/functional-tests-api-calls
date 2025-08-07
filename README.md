🐍 Prerequisites: installing Python and packages
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

5.Install needed packages
> py -m pip install requests

or, if it doesn't work, type

> pip install requests

How to create a new parameter (Python version)
----------------------------
Make the script executable (if not already done so) by typing this in the command line:
> chmod +x creationOfNewParameter.sh

Run the script from the commandline
> ./creationOfNewParameter.sh

Follow the prompts and insert the following information
- domain name
- name of the parameter
- data type (NUMERIC if a number, STRING if text)


How to create a new parameter (Bash version)
----------------------------
Make the script executable (if not already done so) by typing this in the command line:
> chmod +x creationOfNewParameter.sh

Run the script from the commandline
> ./creationOfNewParameter.sh

Follow the prompts and insert the following information
- domain name
- name of the parameter
- data type (NUMERIC if a number, STRING if text)


