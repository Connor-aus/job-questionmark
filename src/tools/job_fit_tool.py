from pathlib import Path
from src.llms.llm import llm
from src.utils.logger import log

# Get the directory containing this script
CURRENT_DIR = Path(__file__).parent.parent

CV_TEXT = ""
PROJECTS_TEXT = ""

with open(CURRENT_DIR / 'staticFiles' / 'cv.txt', 'r') as f:
    CV_TEXT = f.read()

with open(CURRENT_DIR / 'staticFiles' / 'projects.txt', 'r') as f:
    PROJECTS_TEXT = f.read()

def run_job_fit(job_ad_text: str) -> str:
    try:
        log.info("Running Job Fit Tool")
        prompt = f"""
You are an expert career assistant helping potential employers understand how well Connor matches job descriptions.

Connor's experience:
\"\"\"{CV_TEXT}\"\"\"

Connor's projects:
\"\"\"{PROJECTS_TEXT}\"\"\"

Job description:
\"\"\"{job_ad_text}\"\"\"

Please return:
Identify which skills and experiences listed in the Job Description Connor possesses. Provide specific examples from his experience or projects that demonstrate alignment with these skills and experiences.
Assign a percentage score based only on the proportion of the Job Description’s skills and experiences that Connor matches.
-A score of 100% means Connor meets all of the required and desired criteria in the job description.
-A score of 80 or 85% means Connor meets most but not all (e.g., 3 out of 4) of the required skills.
-A score of 50% means Connor may not match many skills but it is in the correct industry (e.g. software engineering or cloud engineering).
-A score of 0% means none of the job description's requirements are met and the job is in a completely different industry to Connor's experience (e.g. arts or marketing).
Do not penalize Connor for having skills or experience that are NOT listed in the job description as the score is based on the skills and experiences that are listed in the job description only.
Use clear, concise, and professional language suitable for recruiters. Maintain a positive, strengths-based tone in your assessment.
    """
        response = llm.invoke(prompt)
        log.info("Job Fit Tool response: " + response.content)
        return response.content
    except Exception as e:
        log.error("Error running Job Fit Tool: " + str(e))
        return "I'm sorry, I'm having trouble answering that question. Please try again."

