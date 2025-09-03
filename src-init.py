# src/business_idea_creator/__init__.py
"""
Business Idea Creator Package
AI-powered business idea generation using advanced prompt engineering
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Package-level imports with error handling
try:
    from .prompt_engine import PromptEngineer, BusinessIdeaRequest
    from .idea_generator import BusinessIdeaGenerator
    from .utils.validators import InputValidator
    from .utils.data_processing import DataProcessor
    
    __all__ = [
        'PromptEngineer',
        'BusinessIdeaRequest',
        'BusinessIdeaGenerator', 
        'InputValidator',
        'DataProcessor'
    ]
except ImportError:
    # Allow imports to fail during development/installation
    pass