import openai
import google.generativeai as genai
from typing import List, Dict, Any
import numpy as np
from app.config import settings
import json

class AIService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        genai.configure(api_key=settings.GOOGLE_AI_API_KEY)
        self.gemini_model = genai.GenerativeModel('gemini-pro')
    
    async def get_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using OpenAI"""
        try:
            response = await openai.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []
    
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of feedback"""
        prompt = f"""Analyze the sentiment of this feedback and return ONLY a JSON response:

Feedback: {text}

Return format:
{{
    "sentiment": "positive|neutral|negative",
    "score": 0.0-1.0,
    "emotion": "frustrated|confused|happy|requesting|complaining"
}}"""
        
        try:
            response = self.gemini_model.generate_content(prompt)
            result = json.loads(response.text)
            return result
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return {"sentiment": "neutral", "score": 0.5, "emotion": "neutral"}
    
    async def extract_issues(self, text: str) -> List[Dict[str, Any]]:
        """Extract specific issues from feedback"""
        prompt = f"""Extract specific technical issues from this feedback. Return ONLY a JSON array:

Feedback: {text}

Return format:
[
    {{
        "issue": "brief issue description",
        "category": "login|payment|performance|crash|ui|feature_request|other",
        "severity": "critical|major|minor",
        "keywords": ["keyword1", "keyword2"]
    }}
]

If no clear issue, return empty array []."""
        
        try:
            response = self.gemini_model.generate_content(prompt)
            issues = json.loads(response.text)
            return issues if isinstance(issues, list) else []
        except Exception as e:
            print(f"Error extracting issues: {e}")
            return []
    
    async def categorize_issue(self, issue_text: str) -> str:
        """Categorize an issue into predefined categories"""
        prompt = f"""Categorize this issue into ONE category. Return ONLY the category name:

Issue: {issue_text}

Categories:
- authentication (login, signup, OTP, verification)
- payment (transactions, billing, refunds)
- performance (slow, lag, loading)
- crash (app crashes, freezes)
- ui_ux (design, layout, navigation)
- feature_request (new features, improvements)
- connectivity (network, sync issues)
- battery (battery drain, power issues)
- storage (disk space, cache)
- other

Return ONLY the category name, nothing else."""
        
        try:
            response = self.gemini_model.generate_content(prompt)
            category = response.text.strip().lower()
            return category
        except Exception as e:
            print(f"Error categorizing issue: {e}")
            return "other"
    
    async def generate_priority_summary(self, issues: List[Dict]) -> str:
        """Generate actionable priority summary"""
        prompt = f"""Based on these issues, generate a concise priority summary for developers:

Issues:
{json.dumps(issues, indent=2)}

Format:
**Immediate Action Required:**
- [issue] (X% of complaints, affecting Y users)

**Next Sprint:**
- [issue] (X% of complaints)

**Monitor:**
- [issue] (trending up/down)

Keep it brief and actionable."""
        
        try:
            response = self.gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating summary: {e}")
            return "Unable to generate summary"
    
    async def suggest_fix(self, issue_description: str, affected_segments: Dict) -> str:
        """Suggest potential fix for an issue"""
        prompt = f"""Suggest a technical fix for this issue:

Issue: {issue_description}
Affected: {json.dumps(affected_segments)}

Provide:
1. Likely root cause
2. Suggested fix
3. Testing steps

Keep it concise and technical."""
        
        try:
            response = self.gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error suggesting fix: {e}")
            return "Unable to generate suggestion"