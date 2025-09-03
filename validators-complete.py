# src/business_idea_creator/utils/validators.py
"""
Input validation utilities for Business Idea Creator
"""

from typing import List, Dict, Any
import re

class InputValidator:
    def __init__(self):
        self.required_fields = [
            "industry", "target_audience", "market_trends", 
            "budget_range", "geographical_focus", "innovation_level"
        ]
    
    def validate_inputs(self, params: Dict[str, Any]) -> List[str]:
        """Validate input parameters and return list of errors"""
        errors = []
        
        # Check required fields
        for field in self.required_fields:
            if not params.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Validate market trends
        if params.get("market_trends"):
            if len(params["market_trends"]) < 1:
                errors.append("Please select at least 1 market trend")
            elif len(params["market_trends"]) > 8:
                errors.append("Please select no more than 8 market trends")
        
        # Validate text inputs
        text_fields = ["industry", "target_audience", "geographical_focus"]
        for field in text_fields:
            if params.get(field) and len(params[field].strip()) < 2:
                errors.append(f"{field} must be at least 2 characters long")
        
        return errors
    
    def sanitize_text_input(self, text: str) -> str:
        """Sanitize text input to prevent injection attacks"""
        if not text:
            return ""
        
        # Remove potentially harmful characters
        sanitized = re.sub(r'[<>"\']', '', text)
        return sanitized.strip()
    
    def validate_api_key(self, api_key: str) -> bool:
        """Validate OpenAI API key format"""
        if not api_key:
            return False
        
        # OpenAI API keys start with 'sk-' and are typically 51 characters
        return api_key.startswith('sk-') and len(api_key) >= 20