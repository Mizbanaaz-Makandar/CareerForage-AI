"""
AI-Powered ATS Resume Analyzer
Uses GPT and semantic similarity for intelligent resume analysis
"""

import openai
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class AI_ATSAnalyzer:
    """AI-powered resume analysis for ATS compatibility"""
    
    def __init__(self, api_key: str = None):
        """Initialize AI models"""
        if api_key:
            openai.api_key = api_key
        
        # Load semantic similarity model (works offline)
        try:
            self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Semantic model loaded successfully")
        except Exception as e:
            logger.warning(f"Could not load semantic model: {e}")
            self.semantic_model = None
        
        # Common skills database
        self.skill_categories = {
            'python': ['python', 'django', 'flask', 'fastapi', 'pandas', 'numpy', 'scikit-learn'],
            'javascript': ['javascript', 'react', 'vue', 'angular', 'node.js', 'express'],
            'java': ['java', 'spring', 'springboot', 'hibernate', 'maven', 'gradle'],
            'data_science': ['python', 'r', 'sql', 'tensorflow', 'pytorch', 'machine learning'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform']
        }
    
    def analyze_resume(self, resume_text: str, job_role: str, 
                       job_description: str = None) -> Dict[str, Any]:
        """
        Comprehensive AI-powered resume analysis
        
        Args:
            resume_text: Extracted text from resume
            job_role: Target job role
            job_description: Optional job description for matching
        
        Returns:
            Dictionary with analysis results
        """
        
        results = {
            'success': True,
            'total_score': 0,
            'semantic_score': 0,
            'skills_match': 0,
            'format_score': 0,
            'strengths': [],
            'improvements': [],
            'suggested_keywords': [],
            'detailed_feedback': ''
        }
        
        try:
            # 1. Semantic Similarity Score (if job description provided)
            if job_description and self.semantic_model:
                semantic_score = self._calculate_semantic_score(resume_text, job_description)
                results['semantic_score'] = semantic_score
                results['total_score'] += semantic_score * 0.4
            
            # 2. Skills Matching
            skills_result = self._analyze_skills(resume_text, job_role)
            results['skills_match'] = skills_result['score']
            results['total_score'] += skills_result['score'] * 0.35
            results['strengths'].extend(skills_result['strengths'])
            results['improvements'].extend(skills_result['improvements'])
            results['suggested_keywords'].extend(skills_result['suggested'])
            
            # 3. Format & Structure Analysis
            format_result = self._analyze_format(resume_text)
            results['format_score'] = format_result['score']
            results['total_score'] += format_result['score'] * 0.25
            results['improvements'].extend(format_result['improvements'])
            
            # 4. Generate GPT Feedback (if API key available)
            if openai.api_key:
                gpt_feedback = self._generate_gpt_feedback(
                    resume_text, job_role, job_description, results
                )
                results['detailed_feedback'] = gpt_feedback
            
            # Normalize total score
            results['total_score'] = min(100, int(results['total_score']))
            
        except Exception as e:
            logger.error(f"Error in AI analysis: {e}")
            results['success'] = False
            results['error'] = str(e)
        
        return results
    
    def _calculate_semantic_score(self, resume: str, job_desc: str) -> float:
        """Calculate semantic similarity using sentence transformers"""
        if not self.semantic_model:
            return 50.0  # Default score if model unavailable
        
        try:
            # Truncate long texts
            resume = resume[:2000]
            job_desc = job_desc[:2000]
            
            # Get embeddings
            resume_embedding = self.semantic_model.encode([resume])[0]
            job_embedding = self.semantic_model.encode([job_desc])[0]
            
            # Calculate cosine similarity
            similarity = np.dot(resume_embedding, job_embedding) / (
                np.linalg.norm(resume_embedding) * np.linalg.norm(job_embedding)
            )
            
            # Convert to percentage (60-95 range)
            score = 60 + (similarity * 35)
            return min(95, max(60, score))
            
        except Exception as e:
            logger.error(f"Semantic calculation error: {e}")
            return 70.0
    
    def _analyze_skills(self, resume: str, job_role: str) -> Dict:
        """Analyze skills matching for target role"""
        resume_lower = resume.lower()
        
        # Determine role category
        role_category = self._detect_role_category(job_role)
        target_skills = self.skill_categories.get(role_category, [])
        
        if not target_skills:
            target_skills = ['communication', 'teamwork', 'problem solving', 
                           'leadership', 'project management']
        
        # Find matching skills
        matched = []
        missing = []
        
        for skill in target_skills:
            if skill in resume_lower:
                matched.append(skill)
            else:
                missing.append(skill)
        
        # Calculate score
        score = (len(matched) / len(target_skills)) * 100 if target_skills else 50
        
        # Generate strengths/improvements
        strengths = []
        improvements = []
        suggested = []
        
        if matched:
            strengths.append(f"Contains key skills: {', '.join(matched[:3])}")
        
        if missing:
            improvements.append(f"Add these skills: {', '.join(missing[:5])}")
            suggested.extend(missing[:5])
        
        if len(matched) < 3:
            improvements.append("Add more technical skills relevant to the role")
        
        return {
            'score': score,
            'strengths': strengths,
            'improvements': improvements,
            'suggested': suggested,
            'matched': matched,
            'missing': missing
        }
    
    def _detect_role_category(self, job_role: str) -> str:
        """Detect role category from job title"""
        role_lower = job_role.lower()
        
        if any(k in role_lower for k in ['python', 'django', 'flask']):
            return 'python'
        elif any(k in role_lower for k in ['javascript', 'react', 'vue']):
            return 'javascript'
        elif any(k in role_lower for k in ['java', 'spring']):
            return 'java'
        elif any(k in role_lower for k in ['data', 'machine learning', 'ai']):
            return 'data_science'
        elif any(k in role_lower for k in ['cloud', 'aws', 'devops']):
            return 'cloud'
        
        return 'general'
    
    def _analyze_format(self, resume: str) -> Dict:
        """Analyze resume format and structure"""
        score = 70  # Start with base
        improvements = []
        
        # Check length
        word_count = len(resume.split())
        if word_count < 300:
            improvements.append("Resume is too short. Add more details about your experience.")
            score -= 10
        elif word_count > 1000:
            improvements.append("Resume is too long. Keep it to 1-2 pages.")
            score -= 5
        
        # Check for sections
        sections = ['experience', 'education', 'skills', 'summary', 'projects']
        found_sections = 0
        
        for section in sections:
            if section in resume.lower():
                found_sections += 1
        
        if found_sections < 3:
            improvements.append(f"Add missing sections: Experience, Education, Skills")
            score -= 15
        
        # Check for bullet points
        bullet_count = resume.count('•') + resume.count('-') + resume.count('*')
        if bullet_count < 10:
            improvements.append("Use bullet points to highlight achievements")
            score -= 10
        
        # Check for quantifiable achievements
        numbers = ['%', 'percent', 'increased', 'decreased', 'saved', 'reduced', 
                   'improved', 'led', 'managed']
        has_numbers = any(num in resume.lower() for num in numbers)
        
        if not has_numbers:
            improvements.append("Add quantifiable achievements (e.g., 'Increased sales by 20%')")
            score -= 15
        
        return {
            'score': max(0, min(100, score)),
            'improvements': improvements[:3]
        }
    
    def _generate_gpt_feedback(self, resume: str, job_role: str, 
                                job_desc: str, results: Dict) -> str:
        """Generate detailed feedback using GPT"""
        if not openai.api_key:
            return "Enable OpenAI API key for detailed feedback."
        
        try:
            prompt = f"""
            As an expert resume reviewer, provide constructive feedback on this resume for a {job_role} position.
            
            RESUME EXCERPT:
            {resume[:1000]}
            
            JOB ROLE: {job_role}
            CURRENT SCORE: {results['total_score']}%
            
            Provide:
            1. A brief overall assessment (1-2 sentences)
            2. Two specific improvements they should make
            3. One thing they're doing well
            
            Keep it concise and actionable.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"GPT feedback error: {e}")
            return "AI feedback unavailable at this time."