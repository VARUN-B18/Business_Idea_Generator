"""
Advanced Prompt Engineering System for Business Idea Generation
Implements multiple prompt engineering techniques including:
- Chain-of-thought prompting
- Few-shot learning
- Context amplification
- Directional stimulus prompting
"""

import json
import os
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class BusinessIdeaRequest:
    industry: str
    target_audience: str
    market_trends: List[str]
    budget_range: str
    geographical_focus: str
    innovation_level: str  # "incremental", "disruptive", "breakthrough"

class PromptEngineer:
    def __init__(self):
        self.base_templates = self._load_prompt_templates()
        self.industry_contexts = self._load_industry_data()
        
    def _load_prompt_templates(self) -> Dict[str, str]:
        """Load pre-crafted prompt templates for different scenarios"""
        templates = {
            "chain_of_thought": """
            Let's think about this business idea generation step by step:
            
            1. First, analyze the industry: {industry}
               - Current market conditions and size
               - Major players and competitive landscape
               - Emerging opportunities and gaps
            
            2. Next, understand the target audience: {target_audience}
               - Demographics and psychographics
               - Pain points and unmet needs
               - Spending behaviors and preferences
            
            3. Then, consider market trends: {trends}
               - How these trends impact the industry
               - Opportunities they create
               - Potential disruptions they may cause
            
            4. Finally, generate innovative business ideas that:
               - Address specific customer pain points
               - Leverage identified market trends
               - Are feasible within {budget_range} budget
               - Focus on {geographical_focus} market
               - Represent {innovation_level} innovation
            
            Based on this analysis, generate 3-5 unique business ideas with:
            - Clear value proposition
            - Target customer description
            - Revenue model
            - Competitive advantage
            - Implementation roadmap
            """,
            
            "few_shot_examples": """
            Here are examples of successful business ideas generated for similar contexts:
            
            Example 1: Industry: Healthcare, Target: Millennials
            Idea: Telemedicine platform for mental health with AI-powered mood tracking
            Value Prop: Accessible, affordable mental healthcare with personalized insights
            
            Example 2: Industry: E-commerce, Target: Small businesses  
            Idea: AI-powered inventory management system with demand forecasting
            Value Prop: Reduce waste and stockouts through predictive analytics
            
            Example 3: Industry: Education, Target: Working professionals
            Idea: Micro-learning platform with VR simulations for skill development
            Value Prop: Learn complex skills through immersive, bite-sized experiences
            
            Now, generate similar innovative ideas for:
            Industry: {industry}
            Target Audience: {target_audience}
            Market Trends: {trends}
            Budget: {budget_range}
            Focus: {geographical_focus}
            Innovation Level: {innovation_level}
            """,
            
            "directional_stimulus": """
            Generate innovative business ideas that incorporate these specific elements:
            
            MUST INCLUDE:
            - Sustainability focus
            - Technology integration  
            - Scalable business model
            - Clear differentiation
            - Social impact component
            
            INDUSTRY CONTEXT: {industry}
            TARGET MARKET: {target_audience}
            TRENDING FACTORS: {trends}
            INVESTMENT LEVEL: {budget_range}
            GEOGRAPHIC SCOPE: {geographical_focus}
            INNOVATION APPROACH: {innovation_level}
            
            For each idea, structure the response with:
            1. Business Name & Tagline
            2. Problem Statement
            3. Solution Overview
            4. Value Proposition
            5. Target Customer Profile
            6. Revenue Streams (minimum 2)
            7. Competitive Landscape Analysis
            8. Technology Stack Required
            9. Go-to-Market Strategy
            10. Growth Projections (3-year outlook)
            """
        }
        return templates
    
    def _load_industry_data(self) -> Dict[str, Any]:
        """Load industry-specific context data"""
        return {
            "technology": {
                "key_trends": ["AI/ML", "Cloud Computing", "Cybersecurity", "IoT"],
                "pain_points": ["Data privacy", "Digital transformation", "Skills gap"],
                "opportunities": ["Automation", "Personalization", "Efficiency"],
                "market_size": "$5.2T globally"
            },
            "healthcare": {
                "key_trends": ["Telemedicine", "Wearables", "Personalized medicine"],
                "pain_points": ["Access to care", "Cost management", "Data integration"],
                "opportunities": ["Preventive care", "Remote monitoring", "AI diagnostics"],
                "market_size": "$4.3T globally"
            },
            "retail": {
                "key_trends": ["E-commerce", "Omnichannel", "Sustainability"],
                "pain_points": ["Customer acquisition", "Inventory management", "Competition"],
                "opportunities": ["Personalization", "AR/VR shopping", "Social commerce"],
                "market_size": "$26T globally"
            },
            "finance": {
                "key_trends": ["Fintech", "Digital payments", "Cryptocurrency"],
                "pain_points": ["Regulation", "Security", "User experience"],
                "opportunities": ["Financial inclusion", "Automated investing", "DeFi"],
                "market_size": "$22.5T globally"
            },
            "education": {
                "key_trends": ["Online learning", "Micro-credentials", "VR/AR"],
                "pain_points": ["Accessibility", "Engagement", "Cost"],
                "opportunities": ["Personalized learning", "Skills-based training", "Global reach"],
                "market_size": "$7.3T globally"
            }
        }
    
    def generate_context_aware_prompt(self, request: BusinessIdeaRequest, 
                                      technique: str = "chain_of_thought") -> str:
        """Generate context-aware prompts using specified technique"""
        
        # Get industry-specific context
        industry_context = self.industry_contexts.get(
            request.industry.lower(), 
            self.industry_contexts.get("technology", {})
        )
        
        # Enhance trends with industry context
        enhanced_trends = request.market_trends + industry_context.get("key_trends", [])
        trends_text = ", ".join(enhanced_trends[:5])  # Limit to top 5 trends
        
        # Select appropriate template
        template = self.base_templates.get(technique, self.base_templates["chain_of_thought"])
        
        # Format prompt with request data
        formatted_prompt = template.format(
            industry=request.industry,
            target_audience=request.target_audience,
            trends=trends_text,
            budget_range=request.budget_range,
            geographical_focus=request.geographical_focus,
            innovation_level=request.innovation_level
        )
        
        # Add meta instructions for better AI performance
        meta_instructions = f"""
        CONTEXT ENHANCEMENT:
        Industry Size: {industry_context.get('market_size', 'Growing market')}
        Key Pain Points: {', '.join(industry_context.get('pain_points', []))}
        Major Opportunities: {', '.join(industry_context.get('opportunities', []))}
        
        IMPORTANT INSTRUCTIONS:
        - Be specific and actionable in your recommendations
        - Avoid generic business ideas already saturated in the market
        - Consider current economic conditions and post-pandemic trends
        - Include ESG (Environmental, Social, Governance) considerations
        - Provide realistic timelines and resource requirements
        - Consider regulatory and compliance requirements
        - Focus on customer pain points that are currently underserved
        - Generate ideas that are innovative yet feasible
        
        """
        
        return meta_instructions + formatted_prompt
    
    def validate_and_refine_prompt(self, prompt: str) -> str:
        """Apply prompt validation and refinement techniques"""
        
        # Check prompt length (optimal range: 200-1000 words)
        word_count = len(prompt.split())
        if word_count < 200:
            prompt += "\n\nPlease provide detailed explanations and specific examples for each business idea."
        elif word_count > 1000:
            # Summarize if too long
            prompt = prompt[:4000] + "\n\nPlease provide concise but comprehensive responses."
        
        # Add result format specification
        format_instruction = """
        
        FORMAT YOUR RESPONSE AS:
        
        ## Business Idea #[Number]: [Name]
        
        **Problem:** [What problem does this solve?]
        **Solution:** [How does it solve the problem?]
        **Target Market:** [Who will buy this?]
        **Revenue Model:** [How will it make money?]
        **Competitive Edge:** [What makes it unique?]
        **Implementation:** [Key steps to launch]
        **Success Metrics:** [How to measure success]
        
        Repeat for each business idea (generate 3-5 ideas).
        
        ADDITIONAL REQUIREMENTS:
        - Each idea should be distinct and innovative
        - Include specific numbers where possible (market size, pricing, etc.)
        - Consider scalability and long-term viability
        - Address potential challenges and mitigation strategies
        """
        
        return prompt + format_instruction