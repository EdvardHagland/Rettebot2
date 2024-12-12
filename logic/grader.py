import openai
import json
import os
import logging
from logic.prompt_handler import load_prompt, prepare_prompt

# Set logging level to DEBUG
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY", "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")

def grade_answer(student_answer: str, curriculum_context: str):
    prompt_template = load_prompt()
    prompt = prepare_prompt(prompt_template, student_answer, curriculum_context)

    # Prepare the request payload
    messages = [
        {
            "role": "system",
            "content": "You must return a JSON object with 'grade', 'justification', and 'student_feedback' fields."
        },
        {"role": "user", "content": prompt}
    ]

    # Log the entire request being sent to OpenAI
    logger.debug("Sending request to OpenAI API with the following parameters:")
    logger.debug("Model: gpt-4o-mini")
    logger.debug("Messages: %s", json.dumps(messages, indent=2))
    logger.debug("Response format and other parameters: response_format=json_schema, temperature=0.5, max_tokens=7000")

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=messages,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "grading_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "grade": {"type": "string"},
                        "justification": {"type": "string"},
                        "student_feedback": {"type": "string"}
                    },
                    "required": ["grade", "justification", "student_feedback"],
                    "additionalProperties": False
                }
            }
        },
        temperature=0.5,
        max_tokens=7000
    )

    # Log the entire response
    logger.debug("Received response from OpenAI:")
    logger.debug(json.dumps(response, indent=2))

    content = response.choices[0].message['content'].strip()
    data = json.loads(content)
    grade = data.get("grade")
    justification = data.get("justification")
    student_feedback = data.get("student_feedback")

    return grade, justification, student_feedback


def grade_answers_in_parallel(items, context, max_workers=1):
    import concurrent.futures

    logger.debug("Grading answers in parallel with max_workers=%d", max_workers)

    def process_item(item):
        filename, subject, answer = item
        logger.debug("Grading file: %s (subject: %s)", filename, subject)
        # If no answer, return early
        if not answer.strip():
            logger.debug("No text extracted for %s, skipping grading.", filename)
            return [filename, subject, "N/A", "No text extracted or file type not supported", "N/A"]
        try:
            result = grade_answer(answer, context)
            logger.debug("Result for %s: %s", filename, result)
            grade_val, justification, feedback = result
            return [filename, subject, grade_val, justification, feedback]
        except Exception as e:
            logger.error("Error grading file %s: %s", filename, str(e), exc_info=True)
            return [filename, subject, "N/A", f"Error during grading: {str(e)}", "N/A"]

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        futures = [executor.submit(process_item, i) for i in items]
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            logger.debug("Completed grading for one file: %s", res)
            results.append(res)

    return results
