# Installation

Download **ScriptCheck.zip** from [Releases](https://github.com/ElliottSullingeFarrall/ScriptCheck/releases/latest) and unzip. This will include all the necessary files/folders with example data.

# Usage

In the unzipped directory, there will be 4 files/folders.

### Solutions

In **solutions.py** create the solution script.

### Questions

In **questions.py** create a dictionary named **questions**. This dictionary should have a key for each question/function name in **solutions.py** that needs to be checked and a value that is a dictionary with two keys: **vars** and **tests**. Both of these keys should have a list as their value.

In **vars**, include each local variable to be checked in the question/function.

In **tests**, include each argument(s) as a tuple to be passed to the question/function for testing.

Any modules that need to be imported should also be done in this file.

### Submissions

All submitted scripts (in *.py* format) should be included in this folder.

### Script

To run the script checking process, run **main.py**. This will produce a **feedback** folder containing all the feedback files (in *.txt* format) for the submissions.