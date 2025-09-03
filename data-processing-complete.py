# src/business_idea_creator/utils/data_processing.py
"""
Data processing utilities for Business Idea Creator
"""

import json
from typing import List, Dict, Any

class DataProcessor:
    def __init__(self):
        self.industry_data = self._create_default_industry_data()
        self.market_trends = self._load_market_trends()
    
    def _create_default_industry_data(self) -> Dict[str, Any]:
        """Create default industry data"""
        return {
            "technology": {
                "market_size": "5.2T",
                "growth_rate": 0.08,
                "key_players": ["Microsoft", "Apple", "Google", "Amazon"],
                "pain_points": ["Data privacy", "Skills gap", "Digital transformation"],
                "opportunities": ["AI automation", "Edge computing", "Quantum computing"]
            },
            "healthcare": {
                "market_size": "4.3T", 
                "growth_rate": 0.06,
                "key_players": ["Johnson & Johnson", "Pfizer", "UnitedHealth"],
                "pain_points": ["Access to care", "Rising costs", "Aging population"],
                "opportunities": ["Telemedicine", "AI diagnostics", "Personalized medicine"]
            },
            "finance": {
                "market_size": "22.5T",
                "growth_rate": 0.05,
                "key_players": ["JPMorgan", "Bank of America", "Wells Fargo"],
                "pain_points": ["Regulation", "Cybersecurity", "Digital transformation"],
                "opportunities": ["Fintech", "Digital payments", "Robo-advisors"]
            },
            "retail": {
                "market_size": "26T",
                "growth_rate": 0.04,
                "key_players": ["Amazon", "Walmart", "Alibaba"],
                "pain_points": ["E-commerce competition", "Supply chain", "Customer experience"],
                "opportunities": ["Omnichannel", "Personalization", "Sustainability"]
            }
        }
    
    def _load_market_trends(self) -> List[Dict[str, Any]]:
        """Load current market trends data"""
        return [
            {"trend": "AI Integration", "growth_rate": 0.45, "relevance_score": 0.9},
            {"trend": "Sustainability", "growth_rate": 0.32, "relevance_score": 0.85},
            {"trend": "Remote Work", "growth_rate": 0.28, "relevance_score": 0.75},
            {"trend": "E-commerce", "growth_rate": 0.41, "relevance_score": 0.8},
            {"trend": "Digital Health", "growth_rate": 0.38, "relevance_score": 0.88}
        ]
    
    def get_industry_insights(self, industry: str) -> Dict[str, Any]:
        """Get insights for specific industry"""
        return self.industry_data.get(industry.lower(), {})
    
    def analyze_market_trends(self, trends: List[str]) -> Dict[str, Any]:
        """Analyze selected market trends"""
        trend_analysis = {}
        
        for trend in trends:
            # Find matching trend data
            for trend_data in self.market_trends:
                if trend.lower() in trend_data["trend"].lower():
                    trend_analysis[trend] = {
                        "growth_potential": trend_data["growth_rate"],
                        "market_relevance": trend_data["relevance_score"],
                        "recommendation": self._get_trend_recommendation(trend_data)
                    }
                    break
        
        return trend_analysis
    
    def _get_trend_recommendation(self, trend_data: Dict[str, Any]) -> str:
        """Generate recommendation based on trend data"""
        if trend_data["relevance_score"] > 0.8:
            return "High priority - integrate into core business model"
        elif trend_data["relevance_score"] > 0.6:
            return "Medium priority - consider for future development"
        else:
            return "Low priority - monitor for future opportunities"