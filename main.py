import pdf_parser

resume_text = pdf_parser.extract_pdf_text("sample.pdf")
job_description_text = pdf_parser.extract_txt_text("jd.txt")


print("Resume text:", resume_text)
print("Job description text:", job_description_text)
