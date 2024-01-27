import sys
import importlib
from pathlib import Path

from questions import *

def check(submission):
    with open(f'src/feedback/{submission.stem}.txt', 'a') as out:
        print(f'Checking {submission.stem}...')
        out.write(f'SCRIPT: \t{submission.stem}\n')

        for question, attrs in questions.items():
            print(f'\tChecking {question}...')
            out.write(f'\nQUESTION: \t{question}\n')

            question_submission = getattr(importlib.import_module(f'submissions.{submission.stem}'), question)
            question_solution = getattr(importlib.import_module(f'solutions'), question)

            def trace_solution(frame, event, arg):
                if event == 'return':
                    for var in attrs['vars']:
                        vars_solution[var] = frame.f_locals.get(var)
                return trace_solution
            def trace_submission(frame, event, arg):
                if event == 'return':
                    for var in attrs['vars']:
                        vars_submission[var] = frame.f_locals.get(var)
                return trace_submission
            
            for test in attrs['tests']:
                print(f'\t\tTrying {test}...')

                sys.settrace(trace_solution)
                vars_solution = {}
                result_solution = question_solution(*test)
                sys.settrace(None)

                try:
                    sys.settrace(trace_submission)
                    vars_submission = {}
                    result_submission = question_submission(*test)
                    sys.settrace(None)
                except Exception as e:
                    result_submission = e


                if result_submission == result_solution:
                    out.write(f'\tINPUT: \t{test} \t{"PASSED" : >30}\n')
                else:
                    out.write(f'\tINPUT: \t{test} \t{"FAILED" : >30}\n')
                    out.write(f'\t\tSOLUTION: \t\t{result_solution}\n')
                    out.write(f'\t\tSUBMISSION: \t{result_submission}\n')

                for var in attrs['vars']:
                    if vars_submission[var] == vars_solution[var]:
                        out.write(f'\t\tVAR: \t{var} {"PASSED" : >30}\n')
                    else:
                        out.write(f'\t\tVAR: \t{var} {"FAILED" : >30}\n')
                        out.write(f'\t\t\tSOLUTION: \t\t{vars_solution[var]}\n')
                        out.write(f'\t\t\tSUBMISSION: \t{vars_submission[var]}\n')
                

if __name__ == '__main__':
    SUBMISSIONS = Path('src/submissions')
    FEEDBACK = Path('src/feedback')

    for feedback in FEEDBACK.glob('*.txt'):
        feedback.unlink()
    FEEDBACK.mkdir(parents=True, exist_ok=True)

    print('Initialising...\n')
    for submission in SUBMISSIONS.glob('*.py'):
        check(submission)
    print('Done.')