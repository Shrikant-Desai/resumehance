import pdf_parser
from skill_extractor import extract_skills_from_resume
from job_analyzer import analyze_job_posting
from skill_matcher import match_skills, skill_gap_analyzer

resume_text = pdf_parser.extract_pdf_text("sample.pdf")
job_description_text = pdf_parser.extract_txt_text("jd.txt")


# print("Resume text:", resume_text)
# print("Job description text:", job_description_text)


# skills = extract_skills_from_resume(resume_text)
# print("Extracted skills:", skills)
extracted_skills = {
    "total_experience_years": 0.33,
    "experience": [
        {
            "company": "TechNova Solutions",
            "role": "Software Developer Intern",
            "start_date": "Jan 2023",
            "end_date": "Apr 2023",
            "duration_months": 4,
        }
    ],
    "skills": {
        "technical_skills": [
            "JavaScript",
            "Python",
            "Java",
            "C++",
            "Data Structures",
            "Algorithms",
            "OOP",
            "REST APIs",
        ],
        "soft_skills": ["Communication", "Agile", "Team Collaboration"],
        "tools_and_technologies": [
            "Git",
            "GitHub",
            "Docker",
            "VS Code",
            "HTML5",
            "CSS3",
            "Tailwind CSS",
        ],
        "frameworks": ["React", "Node.js", "Express.js"],
        "databases": ["MongoDB", "MySQL"],
        "certifications": [
            "Data Structures and Algorithms Certification – Coursera",
            "Full Stack Web Development Bootcamp – Udemy",
        ],
    },
    "skill_experience_map": {
        "JavaScript": 0.33,
        "React": 0.33,
        "Node.js": 0.33,
        "MongoDB": 0.33,
    },
}

# required_skills_new = analyze_job_posting(job_description_text)
# print(f"Required skills from job description {':' * 10} {required_skills_new}")

required_skills = {
    "job_title": "Software Engineer",
    "seniority_level": "Mid-Level",
    "domain": "Frontend / Full Stack",
    "experience_required": {"minimum_years": 1, "preferred_years": 3},
    "required_skills": {
        "technical_skills": [
            "JavaScript",
            "State Management",
            "API Integration",
            "Application Performance Optimization",
            "Unit Testing",
            "Integration Testing",
        ],
        "soft_skills": ["Collaboration"],
        "tools_and_technologies": ["Modern Frontend Tooling"],
        "frameworks": ["React", "Vue"],
        "databases": [],
    },
    "good_to_have_skills": {
        "technical_skills": ["Backend Development"],
        "tools_and_technologies": ["Jest", "Cypress"],
        "frameworks": ["Next.js"],
        "databases": ["SQL Databases"],
    },
    "skill_priority_map": {
        "React": "critical",
        "Vue": "critical",
        "TypeScript": "critical",
        "JavaScript": "critical",
        "Modern Frontend Tooling": "critical",
        "API Integration": "critical",
        "State Management": "critical",
        "Redux": "critical",
        "Zustand": "critical",
        "Unit Testing": "critical",
        "Integration Testing": "critical",
        "Collaboration": "critical",
        "Next.js": "good_to_have",
        "Node.js": "good_to_have",
        "SQL Databases": "good_to_have",
        "Jest": "good_to_have",
        "Cypress": "good_to_have",
    },
}

skills_match = {
    "matched": ["JavaScript", "Collaboration", "React", "Node.js", "SQL Databases"],
    "partial": [
        {
            "skill": "Experience Level",
            "reason": "Candidate has 0.33 years of experience, which is below the minimum 1-year requirement for a Mid-Level role.",
        },
        {
            "skill": "Modern Frontend Tooling",
            "reason": "Candidate has experience with Tailwind CSS, Git, and VS Code, but lacks broader exposure to the full ecosystem of modern build tools required for a Mid-Level role.",
        },
        {
            "skill": "API Integration",
            "reason": "Candidate has REST API exposure, but lacks formal project experience demonstrating complex integration patterns typically expected at the Mid-Level.",
        },
        {
            "skill": "State Management",
            "reason": "Candidate lists React, which implies exposure to state, but lacks specific mentioned experience with industry-standard libraries like Redux or Zustand.",
        },
        {
            "skill": "Unit Testing / Integration Testing",
            "reason": "Candidate has no explicit testing experience listed, though general programming knowledge is present.",
        },
        {
            "skill": "Jest / Cypress",
            "reason": "These are 'good to have' skills; the candidate has general programming skills but no documented experience with these specific testing frameworks.",
        },
    ],
    "missing": [
        "Vue",
        "TypeScript",
        "Redux",
        "Zustand",
        "Application Performance Optimization",
        "Next.js",
    ],
}
# skills_matching_report = match_skills(extracted_skills, required_skills)
# print(f"Skills matching report {':' * 10} {skills_matching_report}")

# skill_analysis_report = skill_gap_analyzer(
#     skills_match["missing"], job_description_text
# )
# print(f"Skill analysis report {'>' * 10} {skill_analysis_report}")


skill_analysis_report = {
    "gaps": [
        {
            "skill": "TypeScript",
            "priority": "critical",
            "learning_time_months": "1",
            "reason": "Explicitly listed in Required Skills and mentioned as a core requirement for frontend tooling.",
        },
        {
            "skill": "Redux",
            "priority": "critical",
            "learning_time_months": "1",
            "reason": "Explicitly listed as a required skill for state management.",
        },
        {
            "skill": "Zustand",
            "priority": "critical",
            "learning_time_months": "0.5",
            "reason": "Explicitly listed as a required skill for state management.",
        },
        {
            "skill": "Application Performance Optimization",
            "priority": "critical",
            "learning_time_months": "2",
            "reason": "Specifically listed as a core responsibility for the role.",
        },
        {
            "skill": "Vue",
            "priority": "important",
            "learning_time_months": "1.5",
            "reason": "Mentioned as an alternative framework to React under responsibilities.",
        },
        {
            "skill": "Next.js",
            "priority": "good_to_have",
            "learning_time_months": "1",
            "reason": "Listed under Preferred Skills, making it an optional but advantageous skill.",
        },
    ]
}
