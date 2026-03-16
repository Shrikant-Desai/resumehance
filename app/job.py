import pdf_parser
from skill_extractor import extract_skills_from_resume
from job_analyzer import analyze_job_posting
from skill_matcher import match_skills, skill_gap_analyzer
from readiness_score import calculate_job_readiness_score
from roadmap_generator import generate_roadmap


def run_job():
    resume_text = pdf_parser.extract_pdf_text("sample.pdf")
    job_description_text = pdf_parser.extract_txt_text("jd.txt")

    print("Resume text:", resume_text)
    print("Job description text:", job_description_text)

    # extracted_skills = extract_skills_from_resume(resume_text)
    # print("Extracted skills:", extracted_skills)
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

    # required_skills = analyze_job_posting(job_description_text)
    # print(f"Required skills from job description {':' * 10} {required_skills}")

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

    # skills_match = match_skills(extracted_skills, required_skills)
    # print(f"Skills matching report {':' * 10} {skills_match}")

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

    job_readiness_score = calculate_job_readiness_score(
        extracted_skills, required_skills, skills_match
    )

    print(f"Candidate's job readiness score: {job_readiness_score}%")

    # roadmap = generate_roadmap(
    #     target_role=required_skills["job_title"],
    #     seniority_level=required_skills["seniority_level"],
    #     missing_skills=skill_analysis_report["gaps"],
    #     partial_skills=[skill["skill"] for skill in skills_match["partial"]],
    #     total_experience_years=extracted_skills["total_experience_years"],
    # )

    # print(f"Personalized learning roadmap: {roadmap}")

    roadmap = {
        "target_role": "Software Engineer",
        "total_weeks": 24,
        "roadmap": [
            {
                "week": 1,
                "skill": "TypeScript",
                "priority": "critical",
                "action": "learn from scratch",
                "resource": "TypeScript Documentation & Handbook",
                "mini_project": "Convert a basic JavaScript project to TypeScript",
                "milestone": "Fluent in static typing, interfaces, and generics",
            },
            {
                "week": 2,
                "skill": "TypeScript Advanced Patterns",
                "priority": "critical",
                "action": "strengthen",
                "resource": "Advanced TypeScript Patterns by Total TypeScript",
                "mini_project": "Implement a generic API service layer with TS",
                "milestone": "Mastery of advanced utility types and conditional types",
            },
            {
                "week": 3,
                "skill": "Redux (Toolkit)",
                "priority": "critical",
                "action": "learn from scratch",
                "resource": "Redux Toolkit Official Tutorials",
                "mini_project": "Create a Todo app with complex state management using RTK",
                "milestone": "Proficiency in Slices, Thunks, and Middleware",
            },
            {
                "week": 4,
                "skill": "Zustand",
                "priority": "critical",
                "action": "learn from scratch",
                "resource": "Zustand GitHub Documentation",
                "mini_project": "Refactor the Week 3 project state from Redux to Zustand",
                "milestone": "Deep understanding of lightweight state management",
            },
            {
                "week": 5,
                "skill": "State Management Patterns (Global/Local)",
                "priority": "critical",
                "action": "strengthen",
                "resource": "React Patterns (patterns.dev)",
                "mini_project": "Design a complex multi-step form with shared state",
                "milestone": "Choosing the right tool for state management based on project scale",
            },
            {
                "week": 6,
                "skill": "Modern Frontend Tooling (Vite/Webpack)",
                "priority": "important",
                "action": "strengthen",
                "resource": "Vite documentation and configuration guides",
                "mini_project": "Configure a custom build pipeline with Webpack/Vite plugins",
                "milestone": "Ability to optimize and customize frontend build environments",
            },
            {
                "week": 7,
                "skill": "API Integration & Async Patterns",
                "priority": "critical",
                "action": "strengthen",
                "resource": "TanStack Query Docs",
                "mini_project": "Integrate a real-world REST API with error handling and caching",
                "milestone": "Advanced API layer architecture",
            },
            {
                "week": 8,
                "skill": "Unit & Integration Testing (Jest/Cypress)",
                "priority": "critical",
                "action": "strengthen",
                "resource": "Testing Library documentation",
                "mini_project": "Write test coverage for complex UI components and API hooks",
                "milestone": "90%+ test coverage in components",
            },
            {
                "week": 9,
                "skill": "Performance Optimization (Rendering)",
                "priority": "critical",
                "action": "learn from scratch",
                "resource": "Google Web Vitals Documentation",
                "mini_project": "Profile and fix render-blocking JS in a lagging application",
                "milestone": "Improved Lighthouse performance score from 60 to 90+",
            },
            {
                "week": 10,
                "skill": "Performance Optimization (Bundling/Network)",
                "priority": "critical",
                "action": "learn from scratch",
                "resource": "Webpack Bundle Analyzer documentation",
                "mini_project": "Implement lazy loading, tree shaking, and code splitting",
                "milestone": "Reduction in bundle size by 30%",
            },
            {
                "week": 11,
                "skill": "Performance Monitoring & Caching",
                "priority": "critical",
                "action": "learn from scratch",
                "resource": "MDN Performance Docs",
                "mini_project": "Implement Service Workers for offline capabilities/caching",
                "milestone": "Successful implementation of offline application state",
            },
            {
                "week": 12,
                "skill": "Advanced Optimization Capstone",
                "priority": "critical",
                "action": "strengthen",
                "resource": "Practical web performance guides",
                "mini_project": "Optimize an existing large-scale dashboard application",
                "milestone": "Demonstrable performance audit reporting",
            },
            {
                "week": 13,
                "skill": "Vue 3 (Essentials)",
                "priority": "important",
                "action": "learn from scratch",
                "resource": "Vue 3 Composition API Documentation",
                "mini_project": "Build a basic dashboard UI in Vue",
                "milestone": "Comparison of React vs Vue paradigms",
            },
            {
                "week": 14,
                "skill": "Vue Ecosystem (Pinia/Router)",
                "priority": "important",
                "action": "learn from scratch",
                "resource": "Pinia documentation",
                "mini_project": "Rebuild a component from your React project in Vue",
                "milestone": "Fluency in Vue reactivity and state management",
            },
            {
                "week": 15,
                "skill": "Vue Advanced Concepts",
                "priority": "important",
                "action": "learn from scratch",
                "resource": "Vue School Masterclasses",
                "mini_project": "Create a multi-page Vue application with complex routing",
                "milestone": "Full-stack frontend competence across frameworks",
            },
            {
                "week": 16,
                "skill": "Next.js (App Router)",
                "priority": "good_to_have",
                "action": "learn from scratch",
                "resource": "Next.js Official Learn",
                "mini_project": "Develop a server-side rendered landing page with SEO",
                "milestone": "Mastery of Server Components and Data Fetching",
            },
            {
                "week": 17,
                "skill": "Next.js (Server Actions & Caching)",
                "priority": "good_to_have",
                "action": "learn from scratch",
                "resource": "Next.js documentation",
                "mini_project": "Integrate a form submission flow via Server Actions",
                "milestone": "Complete hybrid rendering architecture knowledge",
            },
            {
                "week": 18,
                "skill": "Professional Codebase Maintainability",
                "priority": "important",
                "action": "strengthen",
                "resource": "Clean Code / Refactoring books",
                "mini_project": "Refactor a monolithic project into modular architecture",
                "milestone": "Improved code quality metrics (ESLint/Prettier standards)",
            },
            {
                "week": 19,
                "skill": "CI/CD & Deployment",
                "priority": "important",
                "action": "strengthen",
                "resource": "GitHub Actions Documentation",
                "mini_project": "Automate testing and deployment pipelines",
                "milestone": "Automated production deployment workflow",
            },
            {
                "week": 20,
                "skill": "System Design for Frontend",
                "priority": "important",
                "action": "strengthen",
                "resource": "Frontend System Design Interview Guide",
                "mini_project": "Design architecture for a social media feed/notification system",
                "milestone": "Ability to plan scalable frontend systems",
            },
            {
                "week": 21,
                "skill": "Security (XSS, CSRF, CSP)",
                "priority": "important",
                "action": "strengthen",
                "resource": "OWASP Top 10 for Frontend",
                "mini_project": "Conduct security audit on previous projects",
                "milestone": "Hardened application security implementation",
            },
            {
                "week": 22,
                "skill": "Accessibility (A11y)",
                "priority": "important",
                "action": "strengthen",
                "resource": "WCAG 2.1 Guidelines",
                "mini_project": "Perform an A11y audit and fix violations",
                "milestone": "WCAG compliant UI interfaces",
            },
            {
                "week": 23,
                "skill": "Advanced Debugging",
                "priority": "important",
                "action": "strengthen",
                "resource": "Browser Developer Tooling deep dive",
                "mini_project": "Solve 3 complex memory leak issues in a test app",
                "milestone": "Advanced troubleshooting expertise",
            },
            {
                "week": 24,
                "skill": "Final Capstone Project",
                "priority": "critical",
                "action": "strengthen",
                "resource": "Portfolio preparation",
                "mini_project": "Full-stack dashboard with TypeScript, Redux, Performance optimization, and Testing",
                "milestone": "Ready for mid-level software engineering interviews",
            },
        ],
    }

    return {
        "roadmap": roadmap,
        "job_readiness_score": job_readiness_score,
        "skill_analysis_report": skill_analysis_report,
        "skills_match": skills_match,
        "required_skills": required_skills,
        "extracted_skills": extracted_skills,
        "resume_text": resume_text,
        "job_description_text": job_description_text,
    }


if __name__ == "__main__":
    run_job()
