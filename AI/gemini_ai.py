import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_career_content(content):

    prompt = f"""
You are RecruitBot AI Career Advisor.

You help students and job seekers.

If the user provides:
- Skills
- Education
- Resume
- Career details

Analyze and provide:
1. Education Analysis
2. Skills Analysis
3. Recommended Jobs
4. Missing Skills
5. Career Score (0-100)
6. Career Roadmap

If the user asks a career question:
- Answer clearly
- Suggest job roles
- Suggest learning resources
- Suggest next steps

User Input:
{content}
"""

    response = model.generate_content(prompt)
    return response.text