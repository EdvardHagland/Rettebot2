import os

def load_prompt(prompt_path="prompts/grading_prompt.txt"):
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

def prepare_prompt(prompt_template, student_answer, curriculum_context):
    prompt = prompt_template.replace("{{STUDENT_ANSWER}}", student_answer)
    prompt = prompt.replace("{{CURRICULUM_CONTEXT}}", curriculum_context)
    return prompt
