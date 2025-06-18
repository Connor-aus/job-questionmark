import env_setup
from src.agents.unified_agent import agent
from src.utils.print_agent_convo import print_agent_conversation

inputs = {"messages": [{"role": "user", "content": 
                        """
                        To apply to this role, you will need to be proficient in either Python and/or JavaScript. Your role will require proficiency in at least one programming language/framework (JavaScript, TypeScript, Python, C, C#, C++, HTML/CSS, React, Go, Java, Kotlin, SQL, or Swift) in order to solve coding problems (think LeetCode, HackerRank, etc). For each coding problem, you must be able to explain how your solution solves the problem.

                        Responsibilities:
                        Come up with diverse problems and solutions for a coding chatbot
                        Write high-quality answers and code snippets
                        Evaluate code quality produced by AI models for correctness and performance

                        Qualifications:
                        Fluency in English (native or bilingual level)
                        Proficient in either Python and/or JavaScript
                        Excellent writing and grammar skills
                        A bachelor's degree (completed or in progress)
                        Previous experience as a Software Developer, Coder, Software Engineer, or Programmer
                        """}]}
for chunk in agent.stream(inputs, stream_mode="updates"):
    print_agent_conversation(chunk)