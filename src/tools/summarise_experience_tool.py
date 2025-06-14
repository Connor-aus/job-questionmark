from src.llms.llm import llm
from src.utils.logger import log

CV_TEXT = ""

with open('src/staticFiles/cv.txt', 'r') as f:
    CV_TEXT = f.read()


def run_summarise_experience(experience_question: str) -> str:
    log.info("Running Job Fit Tool")
    prompt = f"""
You are an expert career assistant helping potential employers understand Connor experience and skills.

Connor's skills and experience:
\"\"\"{CV_TEXT}\"\"\"

Quetions about Connor's experience:
\"\"\"{experience_question}\"\"\"
"""
# Please return:
# - Whether Connor has experience in the skills or experience.
# - Use clear, professional language suitable for recruiters
# """
    # response = llm.invoke(prompt)
    # return response.content
    return prompt
