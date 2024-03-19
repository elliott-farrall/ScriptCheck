import re
import os
import sys
import warnings
from importlib import import_module
from copy import deepcopy
from pathlib import Path

from questions import *

def check(submission):
    with open(submission.with_suffix('.txt'), 'a') as out:
        print(f'Checking {submission}...')
        out.write(f'SCRIPT: \t{submission}\n')

        # Import python files, redirecting stdout to supress print statements
        stdout = sys.stdout
        try:
            sys.stdout = open(os.devnull, 'w')
            script_submission = import_module(f'submissions.{submission.stem}')
            script_solution = import_module(f'solutions')
            sys.stdout = stdout
        except Exception:
            print(f'Failed to import {submission}') 
            out.write(f'\tIMPORT ERROR\n')
            sys.stdout = stdout
            return

        for question, tests in questions.items():
            print(f'\tChecking {question}...')
            out.write(f'\nQUESTION: \t{question}\n')

            try:
                question_submission = getattr(script_submission, question)
                question_solution = getattr(script_solution, question)
            except AttributeError:
                print(f'\t\tFailed to import {question}')
                out.write(f'\t\tMISSING\n')
                continue
            if type(question_submission) != type(question_solution):
                print(f'\t\tFailed to import {question}')
                out.write(f'\t\tMISSING\n')
                continue
            
            for idx, test in enumerate(tests):
                print(f'\t\tRunning Test {idx+1}...')

                # Execute code using copy of test input, redirecting stdout to supress print statements
                inputs = deepcopy(test)
                stdout = sys.stdout
                try:
                    sys.stdout = open(os.devnull, 'w')
                    result_submission = question_submission(*inputs)
                    result_solution = question_solution(*inputs)
                    sys.stdout = stdout
                except Exception as error:
                    out.write(f'\tTEST {idx+1} \t{"ERROR" : >30}\n')
                    out.write(f'\t\t{error}\n')
                    continue

                if type(result_submission) != type(result_solution):
                    out.write(f'\tTEST {idx+1} \t{"FORMAT" : >30}\n')
                    out.write(f'\t\tSOLUTION: \t\t{result_solution}\n')
                    out.write(f'\t\tSUBMISSION: \t{result_submission}\n')
                elif result_submission != result_solution:
                    out.write(f'\tTEST {idx+1} \t{"FAILED" : >30}\n')
                    out.write(f'\t\tSOLUTION: \t\t{result_solution}\n')
                    out.write(f'\t\tSUBMISSION: \t{result_submission}\n')
                else:
                    out.write(f'\tTEST {idx+1} \t{"PASSED" : >30}\n')
                    
                

if __name__ == '__main__':
    SUBMISSIONS = Path('src/submissions')
    INVALID_CHARS = r'[.]'   #TODO How to handle . in filename when importing as module?

    print('Initialising...')

    # Cleanup existing feedback files
    print('Cleanuing up old feedback files...')
    for feedback in SUBMISSIONS.glob('**/*.txt'):
        feedback.unlink()

    # Rename any files containing unsupported characters
    print('Renaming files with unsupported characters...')
    for submission in SUBMISSIONS.glob('**/*.py'):
        name = re.sub(INVALID_CHARS, '_', submission.stem) + '.py'
        submission.rename(SUBMISSIONS / name)

    # Run checks
    print('Starting checks...\n')
    for submission in SUBMISSIONS.glob('**/*.py'):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            check(submission)
    print('Done!')