"""
AI-Powered Interview Coach using Google Gemini
"""

import json
import re
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class AIInterviewCoach:
    """AI-powered interview preparation"""
    
    def __init__(self, gemini_model):
        self.model = gemini_model
    
    def generate_questions(self, role: str, experience: str, 
                           question_type: str = "mixed", 
                           count: int = 5) -> List[Dict[str, Any]]:
        """
        Generate interview questions using AI
        """
        if not self.model:
            return self._fallback_questions(role, question_type, count)
        
        prompt = self._build_questions_prompt(role, experience, question_type, count)
        
        try:
            response = self.model.generate_content(prompt)
            questions = self._parse_questions_response(response.text)
            return questions if questions else self._fallback_questions(role, question_type, count)
        except Exception as e:
            logger.error(f"Question generation error: {e}")
            return self._fallback_questions(role, question_type, count)
    
    def _build_questions_prompt(self, role: str, experience: str, 
                                question_type: str, count: int) -> str:
        """Build prompt for generating interview questions"""
        experience_map = {
            'entry': 'entry-level (0-2 years)',
            'mid': 'mid-level (3-5 years)',
            'senior': 'senior-level (6+ years)'
        }
        
        exp_text = experience_map.get(experience, 'mid-level')
        
        return f"""
        Generate {count} {question_type} interview questions for a {role} position 
        with {exp_text} experience.
        
        Requirements:
        - Questions should be challenging but fair
        - Mix of technical and behavioral based on type
        - Include expected keywords in answers
        - Provide difficulty level (easy/medium/hard)
        
        Return in EXACT JSON array format:
        [
            {{
                "question": "Question text here",
                "difficulty": "medium",
                "category": "technical",
                "expected_keywords": ["keyword1", "keyword2"],
                "tips": "Helpful tip for answering"
            }}
        ]
        """
    
    def _parse_questions_response(self, response_text: str) -> List[Dict]:
        """Parse Gemini response to extract questions"""
        try:
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        return []
    
    def _fallback_questions(self, role: str, question_type: str, count: int) -> List[Dict]:
        """Fallback question bank"""
        fallback_questions = {
            'technical': [
                {"question": f"What programming languages are you proficient in?", "difficulty": "easy", "category": "technical", "expected_keywords": ["languages", "experience"], "tips": "List your strongest languages first"},
                {"question": "Explain a complex technical problem you solved.", "difficulty": "medium", "category": "technical", "expected_keywords": ["problem", "solution", "result"], "tips": "Use STAR method"},
                {"question": "How do you stay updated with new technologies?", "difficulty": "easy", "category": "technical", "expected_keywords": ["learning", "resources", "courses"], "tips": "Mention specific platforms like Coursera, Udemy"}
            ],
            'behavioral': [
                {"question": "Tell me about yourself.", "difficulty": "easy", "category": "behavioral", "expected_keywords": ["experience", "skills", "goals"], "tips": "Keep it to 2 minutes"},
                {"question": "Describe a challenging project you worked on.", "difficulty": "medium", "category": "behavioral", "expected_keywords": ["challenge", "solution", "result"], "tips": "Focus on your role and impact"},
                {"question": "Why do you want to work here?", "difficulty": "medium", "category": "behavioral", "expected_keywords": ["company", "values", "growth"], "tips": "Research the company first"}
            ],
            'mixed': [
                {"question": f"Tell me about your experience with {role}.", "difficulty": "easy", "category": "behavioral", "expected_keywords": ["experience", "skills"], "tips": "Start with most relevant experience"},
                {"question": "How do you approach problem-solving?", "difficulty": "medium", "category": "technical", "expected_keywords": ["analyze", "solution", "implement"], "tips": "Walk through a real example"},
                {"question": "Describe a time you had to learn a new technology quickly.", "difficulty": "medium", "category": "behavioral", "expected_keywords": ["learning", "technology", "deadline"], "tips": "Show adaptability"}
            ]
        }
        
        questions = fallback_questions.get(question_type, fallback_questions['mixed'])
        return questions[:min(count, len(questions))]
    
    def evaluate_answer(self, question: str, answer: str, 
                        expected_keywords: List[str] = None) -> Dict[str, Any]:
        """
        Evaluate interview answer using AI
        """
        if not self.model:
            return self._fallback_evaluation(answer, question)
        
        prompt = self._build_evaluation_prompt(question, answer, expected_keywords)
        
        try:
            response = self.model.generate_content(prompt)
            evaluation = self._parse_evaluation_response(response.text)
            return evaluation
        except Exception as e:
            logger.error(f"Answer evaluation error: {e}")
            return self._fallback_evaluation(answer, question)
    
    def _build_evaluation_prompt(self, question: str, answer: str, 
                                 expected_keywords: List[str]) -> str:
        """Build prompt for answer evaluation"""
        prompt = f"""
        Evaluate this interview answer:
        
        QUESTION: {question}
        ANSWER: {answer}
        """
        
        if expected_keywords:
            prompt += f"\nEXPECTED KEYWORDS: {', '.join(expected_keywords)}"
        
        prompt += """
        
        Return evaluation in EXACT JSON format:
        {
            "score": 85,
            "strengths": ["Strength 1", "Strength 2"],
            "improvements": ["Improvement 1", "Improvement 2"],
            "feedback": "Overall feedback message",
            "sample_answer": "Brief sample answer structure"
        }
        
        Score should be 0-100 based on:
        - Relevance to question (40%)
        - Completeness and structure (30%)
        - Use of specific examples (20%)
        - Communication clarity (10%)
        """
        return prompt
    
    def _parse_evaluation_response(self, response_text: str) -> Dict[str, Any]:
        """Parse evaluation response"""
        try:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        return self._default_evaluation()
    
    def _default_evaluation(self) -> Dict[str, Any]:
        """Default evaluation when AI fails"""
        return {
            'score': 70,
            'strengths': ['Good attempt'],
            'improvements': ['Add more specific details', 'Use examples'],
            'feedback': 'Keep practicing to improve your answers.',
            'sample_answer': 'Use STAR method to structure your answers'
        }
    
    def _fallback_evaluation(self, answer: str, question: str) -> Dict[str, Any]:
        """Fallback evaluation logic"""
        word_count = len(answer.split())
        
        score = 50
        strengths = []
        improvements = []
        
        if word_count > 50:
            score += 20
            strengths.append("Good detail in your answer")
        else:
            improvements.append("Provide more details and examples")
        
        if any(word in answer.lower() for word in ['example', 'project', 'experience']):
            score += 15
            strengths.append("Included relevant examples")
        
        if any(word in answer.lower() for word in ['i think', 'maybe', 'probably']):
            score -= 10
            improvements.append("Use more confident language")
        
        score = min(100, max(0, score))
        
        return {
            'score': score,
            'strengths': strengths if strengths else ['You provided an answer'],
            'improvements': improvements if improvements else ['Add more specific details'],
            'feedback': f'Score: {score}%. {"Good answer!" if score > 70 else "Keep practicing!"}',
            'sample_answer': 'Structure your answer using the STAR method (Situation, Task, Action, Result)'
        }