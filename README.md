# CareerForage-AI

In the modern recruitment ecosystem, organizations increasingly rely on Applicant Tracking Systems (ATS) and structured interview processes to filter candidates. As a result, job seekers must not only possess the required skills but also present them effectively through optimized resumes and strong interview performance.
However, most candidates face difficulties such as:

-Creating ATS-friendly resumes

-Understanding job-specific skill requirements

-Identifying gaps in their knowledge

-Practicing interviews in a realistic environment

To address these challenges, CareerForge is developed as an AI-powered placement preparation platform that integrates resume building, resume analysis, and interview preparation into a single system.

The platform provides:

-Resume Builder: Allows users to create professional resumes with structured templates and export them as PDF.

-Resume Analysis System: Uses AI to compare the uploaded resume with a job description and generate:

-ATS Score

-Missing Skills

-Skill Gap Report



AI Interview System: Simulates interview scenarios by generating questions based on job descriptions and provides scoring and feedback.

Built using Python (Flask framework), the system leverages modern web technologies and AI libraries to deliver intelligent insights and an interactive user experience.
7

Objectives of the Project :

*The primary objectives of CareerForge are:

*To develop an intuitive, web-based platform for end-to-end placement preparation using Python and Flask.

*To implement an AI-powered Resume Builder that enables users to create and manage professional resumes stored in an SQLite database.

*To build a Resume ATS Analysis module that evaluates uploaded resumes against job descriptions and generates a comprehensive Skill Gap Report including ATS score, missing skills.

*To create an AI-driven Interview Preparation module where users can attend mock interviews based on job descriptions and receive detailed scores and feedback.

*To ensure secure user authentication with signup/login functionality using Werkzeug password hashing.

*To provide a seamless, responsive, and user-friendly experience accessible from any modern web browser.


# Scope of the Project :

The scope of CareerForge includes:

- Web-based application accessible via desktop and mobile browsers.
  
- User account management with secure authentication.
  
- AI-powered resume creation and storage with PDF export capability using xhtml2pdf.
  
- Resume analysis against any job description with ATS scoring and skill recommendations.
  
- Adaptive AI interview sessions with real-time feedback and scoring.
  
- Persistent storage of user data, resumes, interview records using SQLite.



2. System Analysis
2.1 Existing System
Currently, job preparation is done using multiple disconnected platforms:
•
Resume creation using tools like MS Word or basic online builders.
•
Resume analysis using limited or paid ATS tools.
•
Interview preparation through random online videos or manual practice.
Problems in Existing System:
•
Lack of integration between tools
•
No AI-driven personalized feedback
•
Limited ATS evaluation capabilities
•
No real-time interview simulation
•
Inefficient and time-consuming process
2.2 Scope and Limitation of Existing System
Scope:
•
Basic resume creation.
•
General interview preparation resources.
•
Limited online assessment tools.
Limitations:
•
No AI-driven insights.
•
No job-specific resume analysis.
•
No structured learning path.
•
No automated interview feedback system.
•
Time-consuming and inefficient process.
•
Limited user engagement and interactivity
9
2.3 Proposed System
The proposed system, CareerForge, is a unified AI-powered platform designed to enhance placement readiness.
Workflow of System:
1.
User lands on homepage
2.
Registers (SignUp) and logs in securely
3.
Accesses dashboard
4.
Uses three main modules:
1. Resume Builder
•
Create resumes using structured templates
•
Edit and update resumes
•
Store resumes in database
•
Export resumes as PDF (using xhtml2pdf)
2. Resume Analysis
•
Upload resume and job description
•
AI processes and compares content
•
Generates:
o
ATS Score
o
Missing Skills
o
Skill Gap Analysis
o
Learning Roadmap
3. Interview Preparation
•
AI generates interview questions based on job role
•
User answers questions interactively
•
System evaluates responses
•
Provides:
10
o
Score
o
Feedback
o
Improvement suggestions
Advantages:
•
All-in-one platform
•
AI-driven insights
•
Personalized feedback
•
Improves employability skills
11
2.4 Feasibility Study
A feasibility study ensures the project is viable and sustainable. The study includes:
1. Technical Feasibility
The project is technically feasible as it uses widely available technologies such as:
•
Built using:
o
Python (Flask)
o
MySQL database
o
HTML, CSS, JavaScript
•
Uses libraries:
o
Flask
o
Werkzeug (authentication/security)
o
PyPDF2 (PDF text extraction)
o
xhtml2pdf (PDF generation)
o
generative AI APIs
2. Economic Feasibility
CareerForge is economically feasible for the following reasons:
•
All core technologies (Python, Flask, MYSQL, HTML/CSS/JS) are open-source and free.
•
Google Gemini API offers a free tier sufficient for development, testing, and academic demonstration.
•
No dedicated server hardware is required; the application can be run on a standard laptop or a low-cost cloud instance.
•
Development effort is contained within a single academic year with a small team, minimizing resource expenditure.
