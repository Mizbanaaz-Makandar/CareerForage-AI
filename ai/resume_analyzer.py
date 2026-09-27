"""
AI-Powered Resume Analyzer using Google Gemini
"""

import json
import re
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class AIResumeAnalyzer:
    """AI-powered resume analysis for ATS compatibility"""
    
    def __init__(self, gemini_model):
        self.model = gemini_model
    
    def analyze_resume(self, resume_text: str, job_role: str, 
                       job_description: str = "") -> Dict[str, Any]:
        """
        Comprehensive AI-powered resume analysis
        
        Args:
            resume_text: Extracted text from resume
            job_role: Target job role
            job_description: Optional job description for better matching
        
        Returns:
            Dictionary with analysis results
        """
        if not self.model:
            return self._fallback_analysis(resume_text, job_role)
        
        # Build prompt for Gemini
        prompt = self._build_analysis_prompt(resume_text, job_role, job_description)
        
        try:
            response = self.model.generate_content(prompt)
            analysis = self._parse_analysis_response(response.text)
            return analysis
        except Exception as e:
            logger.error(f"AI analysis error: {e}")
            return self._fallback_analysis(resume_text, job_role)
    
    def _build_analysis_prompt(self, resume_text: str, job_role: str, 
                               job_description: str) -> str:
        """Build prompt for resume analysis"""
        prompt = f"""
        You are an expert ATS (Applicant Tracking System) resume analyzer.
        Analyze this resume for a {job_role} position.
        
        RESUME:
        {resume_text[:3000]}
        """
        
        if job_description:
            prompt += f"\n\nJOB DESCRIPTION:\n{job_description[:1500]}"
        
        prompt += """
        
        Provide a comprehensive analysis in EXACT JSON format:
        {
            "total_score": 85,
            "semantic_score": 82,
            "skills_match": 78,
            "format_score": 90,
            "strengths": [
                "Strong technical skills in Python",
                "Good use of action verbs"
            ],
            "improvements": [
                "Add more quantifiable achievements",
                "Include industry-specific keywords"
            ],
            "suggested_keywords": ["Django", "REST API", "Microservices"],
            "detailed_feedback": "Your resume shows strong technical skills...",
            "missing_skills": ["Docker", "Kubernetes"],
            "ats_tips": "Use standard section headers like 'Work Experience'"
        }
        
        Be specific, actionable, and professional.
        """
        return prompt
    
    def _parse_analysis_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini response to extract JSON"""
        try:
            # Try to find JSON in response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        # Return default structure if parsing fails
        return self._default_analysis()
    
    def _default_analysis(self) -> Dict[str, Any]:
        """Default analysis when AI fails"""
        return {
            'total_score': 70,
            'semantic_score': 65,
            'skills_match': 60,
            'format_score': 75,
            'strengths': ['Resume submitted for analysis'],
            'improvements': ['Add more keywords', 'Quantify achievements'],
            'suggested_keywords': ['Experience', 'Skills', 'Projects'],
            'detailed_feedback': 'AI analysis unavailable. Using fallback analysis.',
            'missing_skills': [],
            'ats_tips': 'Use standard resume format'
        }
    
    def _fallback_analysis(self, resume_text: str, job_role: str) -> Dict[str, Any]:
        """Fallback analysis when AI is unavailable"""
        # Simple keyword matching
        job_lower = job_role.lower()
        score = 60
        
        keywords = {
            'python': ['python', 'django', 'flask', 'pandas'],
            'java': ['java', 'spring', 'hibernate'],
            'javascript': ['javascript', 'react', 'vue', 'angular']
        }
        
        matched_keywords = []
        for role, kw_list in keywords.items():
            if role in job_lower:
                matched_keywords = kw_list
                break
        
        if not matched_keywords:
            matched_keywords = ['experience', 'skills', 'projects']
        
        matches = sum(1 for kw in matched_keywords if kw in resume_text.lower())
        score = 50 + (matches / len(matched_keywords)) * 50
        
        return {
            'total_score': int(score),
            'semantic_score': int(score),
            'skills_match': int(score * 0.9),
            'format_score': 70,
            'strengths': ['Basic structure present'],
            'improvements': ['Add more relevant keywords'],
            'suggested_keywords': matched_keywords,
            'detailed_feedback': f'Your resume matches {int(score)}% of keywords for {job_role}.',
            'missing_skills': [kw for kw in matched_keywords if kw not in resume_text.lower()],
            'ats_tips': 'Use action verbs and quantify achievements'
        }