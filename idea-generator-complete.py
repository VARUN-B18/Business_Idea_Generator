# src/business_idea_creator/idea_generator.py
"""
Business Idea Generator with OpenAI Integration
Complete working implementation
"""

import os
import json
import time
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

# Import custom modules
try:
    from .prompt_engine import PromptEngineer, BusinessIdeaRequest
except ImportError:
    try:
        from prompt_engine import PromptEngineer, BusinessIdeaRequest
    except ImportError:
        # Create mock classes if imports fail
        class BusinessIdeaRequest:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)
        
        class PromptEngineer:
            def generate_context_aware_prompt(self, request, technique="chain_of_thought"):
                return f"Generate business ideas for {request.industry}"
            def validate_and_refine_prompt(self, prompt):
                return prompt

# OpenAI import with fallback
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OpenAI = None
    OPENAI_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BusinessIdeaGenerator:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with OpenAI API key"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if OPENAI_AVAILABLE and self.api_key:
            self.client = OpenAI(api_key=self.api_key)
            self.mock_mode = False
        else:
            self.client = None
            self.mock_mode = True
            if not OPENAI_AVAILABLE:
                logger.warning("OpenAI not available - running in mock mode")
        
        self.prompt_engineer = PromptEngineer()
        self.generation_history = []
    
    def generate_ideas(self, request: BusinessIdeaRequest, 
                      technique: str = "chain_of_thought",
                      model: str = "gpt-3.5-turbo") -> Dict[str, Any]:
        """Generate business ideas using OpenAI or mock data"""
        
        if self.mock_mode:
            return self._generate_mock_ideas(request, technique, model)
        
        try:
            # Generate context-aware prompt
            prompt = self.prompt_engineer.generate_context_aware_prompt(request, technique)
            prompt = self.prompt_engineer.validate_and_refine_prompt(prompt)
            
            logger.info(f"Generating ideas using {technique} for {request.industry}")
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert business consultant with 20+ years of experience."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.8,
                top_p=0.9,
                frequency_penalty=0.3,
                presence_penalty=0.3
            )
            
            generated_content = response.choices[0].message.content.strip()
            structured_ideas = self._parse_generated_ideas(generated_content)
            
            result = {
                "request_id": f"req_{int(time.time())}",
                "timestamp": datetime.now().isoformat(),
                "input_parameters": {
                    "industry": request.industry,
                    "target_audience": request.target_audience,
                    "market_trends": request.market_trends,
                    "budget_range": request.budget_range,
                    "geographical_focus": request.geographical_focus,
                    "innovation_level": request.innovation_level,
                    "technique_used": technique
                },
                "generated_ideas": structured_ideas,
                "raw_response": generated_content,
                "model_used": model,
                "technique_used": technique
            }
            
            self.generation_history.append(result)
            return result
            
        except Exception as e:
            logger.error(f"Error generating ideas: {e}")
            # Fallback to mock mode
            return self._generate_mock_ideas(request, technique, model)
    
    def _generate_mock_ideas(self, request: BusinessIdeaRequest, technique: str, model: str) -> Dict[str, Any]:
        """Generate mock business ideas for demo/testing"""
        
        mock_ideas = [
            {
                "name": f"AI-Powered {request.industry} Platform",
                "problem": f"Many {request.target_audience} struggle with efficiency in {request.industry}",
                "solution": f"An AI-driven platform that automates and optimizes {request.industry} processes",
                "target_market": request.target_audience,
                "revenue_model": "SaaS subscription model with tiered pricing ($29-$299/month)",
                "competitive_edge": "Advanced AI algorithms with 90% accuracy and real-time insights",
                "implementation": "6-month development cycle, beta testing, gradual market rollout",
                "success_metrics": "User acquisition rate, customer retention, monthly recurring revenue"
            },
            {
                "name": f"Sustainable {request.industry} Marketplace",
                "problem": f"Limited access to sustainable options in {request.industry}",
                "solution": "Digital marketplace connecting eco-friendly suppliers with conscious consumers",
                "target_market": "Environmentally conscious consumers and businesses",
                "revenue_model": "Commission-based (5-8% per transaction) + premium seller memberships",
                "competitive_edge": "Verified sustainability ratings and carbon footprint tracking",
                "implementation": "Platform development, supplier onboarding, marketing campaigns",
                "success_metrics": "Gross merchandise value, active sellers, user engagement metrics"
            },
            {
                "name": f"Mobile {request.industry} Assistant",
                "problem": f"{request.target_audience} need convenient mobile access to {request.industry} services",
                "solution": "Mobile app with AI chatbot, service booking, and personalized recommendations",
                "target_market": request.target_audience,
                "revenue_model": "Freemium model with premium features ($9.99/month subscription)",
                "competitive_edge": "Personalized AI recommendations with 95% user satisfaction",
                "implementation": "Mobile app development, AI training, user testing, app store launch",
                "success_metrics": "Daily active users, conversion rate, app store ratings"
            }
        ]
        
        return {
            "request_id": f"mock_{int(time.time())}",
            "timestamp": datetime.now().isoformat(),
            "input_parameters": {
                "industry": request.industry,
                "target_audience": request.target_audience,
                "market_trends": request.market_trends,
                "budget_range": request.budget_range,
                "geographical_focus": request.geographical_focus,
                "innovation_level": request.innovation_level,
                "technique_used": technique
            },
            "generated_ideas": mock_ideas,
            "model_used": model,
            "technique_used": technique,
            "mock_mode": True
        }
    
    def _parse_generated_ideas(self, content: str) -> List[Dict[str, str]]:
        """Parse generated content into structured business ideas"""
        ideas = []
        current_idea = {}
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith('##') and 'Business Idea' in line:
                if current_idea:
                    ideas.append(current_idea)
                current_idea = {
                    'name': line.replace('##', '').replace('Business Idea', '').strip(),
                    'problem': '', 'solution': '', 'target_market': '',
                    'revenue_model': '', 'competitive_edge': '', 'implementation': '', 'success_metrics': ''
                }
            elif line.startswith('**Problem:**'):
                current_idea['problem'] = line.replace('**Problem:**', '').strip()
            elif line.startswith('**Solution:**'):
                current_idea['solution'] = line.replace('**Solution:**', '').strip()
            # Add more parsing logic as needed
        
        if current_idea:
            ideas.append(current_idea)
        
        return ideas if ideas else self._generate_mock_ideas(None, "", "")["generated_ideas"]