import os
import logging

logger = logging.getLogger(__name__)

def load_prompt(prompt_path="prompts/grading_prompt.txt"):
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

def prepare_prompt(prompt_template, student_answer, curriculum_context):
    # First replace curriculum context
    prompt = prompt_template.replace("{{CURRICULUM_CONTEXT}}", curriculum_context)
    
    # Add the transition text and student answer
    prompt = prompt.replace("{{STUDENT_ANSWER}}", 
        f"\nHer følger elevens besvarelse:\n\n{student_answer}")
    
    # Log the final prompt structure
    logger.debug("Final prompt structure:")
    logger.debug("-" * 50)
    logger.debug(prompt)
    logger.debug("-" * 50)
    
    return prompt
