import os
from math import isclose

from tqdm import tqdm

from .utils.modules import import_module
from .utils.functions import safe_evaluate

QUESTIONS = "questions.py"
SOLUTIONS = "solutions.py"
SUBMISSIONS = "submissions"

def get_submissions(path: str) -> list[str]:
    files_found = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                files_found.append(os.path.join(root, file))
            if file.endswith(".txt"):
                os.remove(os.path.join(root, file))
    return files_found

def run() -> None:
    module_questions = import_module(QUESTIONS)
    if module_questions is None:
        print("Questions file not found")
        return
    else:
        questions = module_questions.questions

    for script_path in tqdm(get_submissions(SUBMISSIONS), desc="Checking submissions"):
        module_sub = import_module(script_path)
        module_sol = import_module(SOLUTIONS)

        feedback_path = os.path.splitext(script_path)[0] + ".txt"
        with open(feedback_path, "w") as feedback_file:
            for question in tqdm(questions, desc=f"Checking {script_path}", leave=False):
                    feedback_file.write(f"Question: {question}\n")

                    if hasattr(module_sub, question):
                        question_sub = getattr(module_sub, question)
                        question_sol = getattr(module_sol, question)
                    else:
                        feedback_file.write(f"\tFunction '{question}' not found in submission\n")
                        continue

                    for test in tqdm(questions[question], desc=f"Checking {question} in {script_path}", leave=False):
                        feedback_file.write(f"\tTest: {test}\n")

                        try:
                            result_sub = safe_evaluate(question_sub, *test)
                            result_sol = safe_evaluate(question_sol, *test)
                        except Exception:
                            feedback_file.write("\tResult: ERROR\n")
                            continue

                        try:
                            # Check for float equality first
                            if not isclose(result_sub, result_sol):
                                feedback_file.write("\tResult: FAIL\n")
                                feedback_file.write(f"\t\tExpected: {result_sol}\n")
                                feedback_file.write(f"\t\tObtained: {result_sub}\n")
                            else:
                                feedback_file.write("\tResult: PASS\n")
                        except TypeError:
                            # Fallback generic equality check
                            if result_sub is not result_sol:
                                feedback_file.write("\tResult: FAIL\n")
                                feedback_file.write(f"\t\tExpected: {result_sol}\n")
                                feedback_file.write(f"\t\tObtained: {result_sub}\n")
                            else:
                                feedback_file.write("\tResult: PASS\n")

if __name__ == "__main__":
    run()
