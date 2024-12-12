import os
import io
import logging
from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfReader

# Import the parallel grading function
from logic.grader import grade_answer, grade_answers_in_parallel
from logic.postprocessing import postprocess_results
from logic.prompt_handler import prepare_prompt

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def extract_text_from_file(filepath: str) -> str:
    ext = os.path.splitext(filepath)[1].lower()
    try:
        if ext == '.txt':
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        elif ext == '.pdf':
            reader = PdfReader(filepath)
            pages_text = [page.extract_text() for page in reader.pages if page.extract_text()]
            return "\n".join(pages_text)
        else:
            logger.warning(f"Unsupported file type: {ext}")
            return ""
    except Exception as e:
        logger.error(f"Error extracting text from {filepath}: {e}", exc_info=True)
        return ""

def load_context(grade: str, subject: str) -> str:
    subject_lower = subject.lower()
    subject_dir = "norwegian" if subject_lower == 'norwegian' else "english"

    if subject_dir == "norwegian":
        context_file = f"contexts/grade{grade}/{subject_dir}/NORSK_VURDERINGSKRITERIER.txt"
    else:
        context_file = f"contexts/grade{grade}/{subject_dir}/ENGELSK_VURDERINGSKRITERIER.txt"

    try:
        if not os.path.exists(context_file):
            logger.warning(f"No criteria file found for grade: {grade}, subject: {subject}")
            return "No criteria found for this grade and subject."
        with open(context_file, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error loading context file {context_file}: {e}", exc_info=True)
        return "Error loading criteria."

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_grade = request.form.get('grade', '10').strip()
        selected_subject = request.form.get('subject', 'Norwegian').strip()

        context = load_context(selected_grade, selected_subject)
        files = request.files.getlist("files")

        upload_folder = "uploaded_files"
        os.makedirs(upload_folder, exist_ok=True)

        # Extract text for all files first, storing (filename, subject, extracted_text)
        file_data = []
        for file in files:
            filename = file.filename
            logger.info(f"Processing file: {filename}")
            save_path = os.path.join(upload_folder, filename)
            file.save(save_path)
            extracted_text = extract_text_from_file(save_path)
            file_data.append((filename, selected_subject, extracted_text))

        # Now grade all files in parallel
        results = grade_answers_in_parallel(file_data, context, max_workers=5)

        # Postprocess results into Excel
        try:
            wb = postprocess_results([
                ["File_Name", "Subject", "Grade", "Justification", "Student_Feedback"]
            ] + results)
            output = io.BytesIO()
            wb.save(output)
            output.seek(0)

            logger.info("Returning generated Excel file to client.")
            return send_file(
                output,
                as_attachment=True,
                download_name="grading_results.xlsx",
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            logger.error(f"Error creating Excel file: {e}", exc_info=True)
            return "Error generating Excel report."

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
