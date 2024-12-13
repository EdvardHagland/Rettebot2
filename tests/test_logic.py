import pytest
from logic.prompt_handler import prepare_prompt
from logic.postprocessing import postprocess_results

def test_prepare_prompt():
    template = "Hello {{STUDENT_ANSWER}} and {{CURRICULUM_CONTEXT}}"
    prompt = prepare_prompt(template, "Student Answer", "Context")
    assert "Student Answer" in prompt
    assert "Context" in prompt

def test_postprocess_results():
    results = [
        ["File_Name", "Subject", "Grade", "Justification"],
        ["file1.pdf", "English", "5", "Well done!"]
    ]
    wb = postprocess_results(results)
    assert wb is not None
    # Additional checks can be done to verify sheet names, cells, etc.

def test_prompt_structure():
    template = "Instructions\n{{CURRICULUM_CONTEXT}}\n{{STUDENT_ANSWER}}"
    prompt = prepare_prompt(
        template,
        student_answer="This is a test answer",
        curriculum_context="Test curriculum"
    )
    
    assert "Her følger elevens besvarelse:" in prompt
    assert prompt.index("Her følger elevens besvarelse:") > prompt.index("Test curriculum")
    assert prompt.index("This is a test answer") > prompt.index("Her følger elevens besvarelse:")
