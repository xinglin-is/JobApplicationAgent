EXTRACT_REQUIREMENTS_PROMPT = """You are an expert technical recruiter and resume writer.
Your task is to analyze the following job description and extract the core requirements.

Focus on:
1. Necessary skills and technologies.
2. Required experience level.
3. Soft skills or traits emphasized.
4. The company's tone and culture (if apparent).

Job Description:
{job_description}

Return the extracted information in a structured JSON format with the following keys:
- "skills" (list of strings)
- "experience_level" (string)
- "soft_skills" (list of strings)
- "culture" (string)
- "summary" (string)
"""

REWRITE_CV_PROMPT = """You are an expert resume writer.
Your task is to rewrite the provided CV to align with the provided extracted job requirements.

DO NOT invent new experiences or skills. 
DO reframe existing experiences to use the language and keywords found in the job requirements.
Highlight the experiences that are most relevant to the role.

Job Requirements (JSON format):
{job_requirements}

Current CV:
{current_cv}

Provide the rewritten CV.
"""

EVALUATE_CV_PROMPT = """You are an expert technical recruiter and resume evaluator.
Your task is to evaluate a candidate's CV against the extracted job requirements.

Score the CV from 0 to 100 based on how well it aligns with the required skills, experience, and soft skills.

Job Requirements:
{job_requirements}

Candidate CV:
{cv}

Return the evaluation in a structured JSON format with the following keys:
- "score" (integer between 0 and 100)
- "reasoning" (string explaining the score breakdown and justification)
- "missing_skills" (list of strings for missing core requirements)
"""
