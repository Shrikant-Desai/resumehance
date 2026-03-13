import pdf_parser
from skill_extractor import extract_skills_from_resume
from job_analyzer import analyze_job_posting

resume_text = pdf_parser.extract_pdf_text("sample.pdf")
job_description_text = pdf_parser.extract_txt_text("jd.txt")


# print("Resume text:", resume_text)
# print("Job description text:", job_description_text)


skills = extract_skills_from_resume(resume_text)
# print("Extracted skills:", skills)


required_skills = analyze_job_posting(job_description_text)
print(f"Required skills from job description {':' * 10} {required_skills}")
