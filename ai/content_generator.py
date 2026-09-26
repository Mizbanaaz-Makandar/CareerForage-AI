"""
AI-Powered Content Generator using Google Gemini
"""

import json
import re
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class AIContentGenerator:
    """AI-powered resume content generation"""
    
    def __init__(self, gemini_model):
        self.model = gemini_model
    
    def generate_summary(self, name: str, role: str, experience: int, 
                         skills: List[str]) -> str:
        """Generate professional summary"""
        if not self.model:
            return self._fallback_summary(role, experience, skills)
        
        skills_str = ', '.join(skills[:5]) if skills else 'relevant skills'
        
        prompt = f"""
        Write a professional resume summary for:
        Name: {name}
        Target Role: {role}
        Experience: {experience} years
        Key Skills: {skills_str}
        
        Requirements:
        - 2-3 sentences only
        - ATS-friendly
        - Professional and compelling
        - Include key achievements or impact
        
        Return ONLY the summary text, no other content.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            logger.error(f"Summary generation error: {e}")
            return self._fallback_summary(role, experience, skills)
    
    def _fallback_summary(self, role: str, experience: int, skills: List[str]) -> str:
        """Fallback summary"""
        skills_str = ', '.join(skills[:3]) if skills else 'technical skills'
        return f"Experienced {role} with {experience} years of expertise in {skills_str}. Proven track record of delivering high-quality solutions and driving business value through technical excellence."
    
    def enhance_bullet_points(self, job_title: str, company: str, 
                              description: str, role: str) -> List[str]:
        """Enhance bullet points with AI"""
        if not self.model or not description:
            return [description]
        
        prompt = f"""
        Improve these resume bullet points for a {role} position.
        
        Job Title: {job_title}
        Company: {company}
        Original: {description}
        
        Requirements:
        - Use strong action verbs
        - Add quantifiable achievements (add numbers where possible)
        - Results-oriented language
        - Return 3-4 bullet points
        
        Return as JSON array of strings.
        """
        
        try:
            response = self.model.generate_content(prompt)
            bullets = json.loads(response.text)
            return bullets if isinstance(bullets, list) else [description]
        except Exception as e:
            logger.error(f"Bullet enhancement error: {e}")
            return [description]
    
    def suggest_skills(self, role: str, current_skills: List[str]) -> Dict[str, List[str]]:
        """Suggest skills to add based on role"""
        if not self.model:
            return self._fallback_skills(role, current_skills)
        
        current_str = ', '.join(current_skills) if current_skills else 'none'
        
        prompt = f"""
        For a {role} position, suggest skills to add to a resume.
        
        Current skills: {current_str}
        
        Return in JSON format:
        {{
            "technical": ["skill1", "skill2", "skill3", "skill4", "skill5"],
            "soft": ["skill1", "skill2", "skill3"],
            "emerging": ["skill1", "skill2"]
        }}
        
        Only include skills not already mentioned if possible.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            logger.error(f"Skill suggestion error: {e}")
            return self._fallback_skills(role, current_skills)
    
    def _fallback_skills(self, role: str, current_skills: List[str]) -> Dict[str, List[str]]:
        """Fallback skill suggestions"""
        role_lower = role.lower()
        current_lower = [s.lower() for s in current_skills]
        
        skill_db = {
            'python': {
                'technical': ['Django', 'Flask', 'FastAPI', 'Pandas', 'NumPy', 'SQLAlchemy'],
                'soft': ['Problem Solving', 'Team Collaboration', 'Communication'],
                'emerging': ['AI/ML', 'Cloud Computing']
            },
            'javascript': {
                'technical': ['React', 'Vue.js', 'Angular', 'Node.js', 'TypeScript', 'Redux'],
                'soft': ['Communication', 'Attention to Detail', 'Creativity'],
                'emerging': ['WebAssembly', 'Serverless']
            },
            'data': {
                'technical': ['Python', 'SQL', 'Machine Learning', 'TensorFlow', 'Tableau', 'Statistics'],
                'soft': ['Analytical Thinking', 'Storytelling', 'Business Acumen'],
                'emerging': ['LLM', 'MLOps']
            }
        }
        
        category = 'python'
        for key in skill_db:
            if key in role_lower:
                category = key
                break
        
        skills = skill_db.get(category, {
            'technical': ['Leadership', 'Project Management', 'Strategic Planning'],
            'soft': ['Communication', 'Teamwork', 'Adaptability'],
            'emerging': ['Agile', 'Digital Transformation']
        })
        
        # Filter out already mentioned skills
        for key in skills:
            skills[key] = [s for s in skills[key] if s.lower() not in current_lower]
        
        return skills