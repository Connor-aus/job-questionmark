from pathlib import Path
from src.llms.llm import llm
from src.utils.logger import log

# Get the directory containing this script
CURRENT_DIR = Path(__file__).parent.parent

CV_TEXT = ""

with open(CURRENT_DIR / 'staticFiles' / 'cv.txt', 'r') as f:
    CV_TEXT = f.read()

def run_job_fit(job_ad_text: str) -> str:
    log.info("Running Job Fit Tool")
    prompt = f"""
You are an expert career assistant helping potential employers understand how well Connor matches job descriptions.

Connor's experience:
\"\"\"{CV_TEXT}\"\"\"

Job description:
\"\"\"{job_ad_text}\"\"\"

Please return:
# - Which skills or experiences Connor matches. Be concise and refer to specific examples from Connor's experience
# - Which are missing or partial
# - An overall fit score (0–100%) with a brief explanation
# - Use clear, professional language suitable for recruiters
"""
    response = llm.invoke(prompt)
    return response.content

