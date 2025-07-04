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

def run_summarise_experience(experience_question: str) -> str:
    try:
        log.info("Running Experience Summary Tool")
        prompt = f"""
    You are an expert career assistant helping potential employers understand Connor experience and skills.

    Connor's experience:
    \"\"\"{CV_TEXT}\"\"\"

    Connor's projects:
    \"\"\"{PROJECTS_TEXT}\"\"\"

    Questions about Connor's experience:
    \"\"\"{experience_question}\"\"\"

    Please return:
    - Whether Connor has experience or has completed projects matching the question.
    - Use clear, concise, and professional language suitable for recruiters. Maintain a positive, strengths-based tone in your assessment.
"""
        response = llm.invoke(prompt)
        log.info("Experience Summary Tool response: " + response.content)
        return response.content
    
    except Exception as e:
        log.error("Error running Experience Summary Tool: " + str(e))
        return "I'm sorry, I'm having trouble answering that question. Please try again."