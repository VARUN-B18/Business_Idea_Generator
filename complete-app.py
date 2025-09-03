"""
Business Idea Creator - Complete Streamlit Application
AI-powered business idea generation using advanced prompt engineering techniques
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime, timedelta
import time
from typing import Dict, List, Any, Optional
import sys

# Page configuration MUST be first Streamlit command
st.set_page_config(
    page_title="Business Idea Creator | Vault of Codes",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-username/business-idea-creator',
        'Report a bug': 'https://github.com/your-username/business-idea-creator/issues',
        'About': "Business Idea Creator - Advanced Prompt Engineering Project"
    }
)

# Import custom modules with comprehensive error handling
def import_custom_modules():
    """Import custom modules with multiple fallback strategies"""
    
    try:
        # Strategy 1: Try absolute import (when installed as package)
        from business_idea_creator.idea_generator import BusinessIdeaGenerator, BusinessIdeaRequest
        from business_idea_creator.utils.data_processing import DataProcessor
        from business_idea_creator.utils.validators import InputValidator
        return BusinessIdeaGenerator, BusinessIdeaRequest, DataProcessor, InputValidator
    
    except ImportError as e1:
        try:
            # Strategy 2: Try relative import
            from .idea_generator import BusinessIdeaGenerator, BusinessIdeaRequest
            from .utils.data_processing import DataProcessor
            from .utils.validators import InputValidator
            return BusinessIdeaGenerator, BusinessIdeaRequest, DataProcessor, InputValidator
        
        except ImportError as e2:
            try:
                # Strategy 3: Add current directory to path and import directly
                current_dir = os.path.dirname(os.path.abspath(__file__))
                if current_dir not in sys.path:
                    sys.path.insert(0, current_dir)
                
                from idea_generator import BusinessIdeaGenerator, BusinessIdeaRequest
                from utils.data_processing import DataProcessor
                from utils.validators import InputValidator
                return BusinessIdeaGenerator, BusinessIdeaRequest, DataProcessor, InputValidator
            
            except ImportError as e3:
                # Strategy 4: Create mock classes for development/demo
                st.warning("🔧 Running in demo mode - some features may be limited")
                
                class MockBusinessIdeaRequest:
                    def __init__(self, **kwargs):
                        for key, value in kwargs.items():
                            setattr(self, key, value)
                
                class MockBusinessIdeaGenerator:
                    def __init__(self, api_key=None):
                        self.api_key = api_key
                    
                    def generate_ideas(self, request, technique="chain_of_thought", model="gpt-3.5-turbo"):
                        # Mock response for demo purposes
                        return {
                            "request_id": f"demo_{int(time.time())}",
                            "timestamp": datetime.now().isoformat(),
                            "generated_ideas": [
                                {
                                    "name": f"AI-Powered {request.industry} Solution",
                                    "problem": f"Many {request.target_audience} struggle with efficiency and automation in {request.industry}",
                                    "solution": f"An AI-driven platform that streamlines {request.industry} operations using machine learning",
                                    "target_market": request.target_audience,
                                    "revenue_model": "SaaS subscription with tiered pricing ($29-$299/month)",
                                    "competitive_edge": "Advanced AI algorithms with 90% accuracy rate",
                                    "implementation": "6-month MVP development, beta testing, gradual rollout",
                                    "success_metrics": "Customer acquisition rate, retention, revenue growth"
                                },
                                {
                                    "name": f"Sustainable {request.industry} Marketplace",
                                    "problem": f"Limited access to eco-friendly options in {request.industry}",
                                    "solution": "Digital marketplace connecting sustainable vendors with conscious consumers",
                                    "target_market": "Environmentally conscious consumers and businesses",
                                    "revenue_model": "Commission-based (5-8% per transaction) + premium memberships",
                                    "competitive_edge": "Verified sustainability ratings and carbon footprint tracking",
                                    "implementation": "Platform development, vendor onboarding, marketing campaign",
                                    "success_metrics": "GMV, vendor count, user engagement, carbon impact"
                                },
                                {
                                    "name": f"Mobile-First {request.industry} Assistant",
                                    "problem": f"{request.target_audience} need on-the-go access to {request.industry} services",
                                    "solution": "Mobile app with AI chatbot, booking system, and personalized recommendations",
                                    "target_market": request.target_audience,
                                    "revenue_model": "Freemium model with premium features ($9.99/month)",
                                    "competitive_edge": "Personalized AI recommendations with 95% satisfaction rate",
                                    "implementation": "App development, AI training, user testing, launch",
                                    "success_metrics": "Daily active users, conversion rate, app store ratings"
                                }
                            ],
                            "model_used": model,
                            "technique_used": technique
                        }
                
                class MockDataProcessor:
                    def get_industry_insights(self, industry):
                        return {
                            "market_size": "Growing",
                            "trends": ["Digital transformation", "Sustainability", "AI integration"],
                            "opportunities": ["Automation", "Personalization", "Mobile-first solutions"]
                        }
                
                class MockInputValidator:
                    def validate_inputs(self, params):
                        errors = []
                        if not params.get("industry"):
                            errors.append("Industry is required")
                        if not params.get("target_audience"):
                            errors.append("Target audience is required")
                        return errors
                    
                    def validate_api_key(self, api_key):
                        return bool(api_key and len(api_key) > 10)
                
                return MockBusinessIdeaGenerator, MockBusinessIdeaRequest, MockDataProcessor, MockInputValidator

# Import the modules
BusinessIdeaGenerator, BusinessIdeaRequest, DataProcessor, InputValidator = import_custom_modules()

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin: 1rem 0;
        border-bottom: 2px solid #ff7f0e;
        padding-bottom: 0.5rem;
    }
    
    .idea-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    
    .idea-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .success-message {
        background: linear-gradient(90deg, #d4edda, #c3e6cb);
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    .info-box {
        background: linear-gradient(90deg, #d1ecf1, #bee5eb);
        color: #0c5460;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }
    
    .sidebar-logo {
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

class BusinessIdeaApp:
    def __init__(self):
        self.data_processor = DataProcessor()
        self.validator = InputValidator()
        
        # Initialize session state
        if 'generator' not in st.session_state:
            st.session_state.generator = None
        if 'generation_history' not in st.session_state:
            st.session_state.generation_history = []
        if 'current_results' not in st.session_state:
            st.session_state.current_results = None
        if 'api_key_valid' not in st.session_state:
            st.session_state.api_key_valid = False
    
    def setup_api_key(self):
        """Handle OpenAI API key setup with enhanced UI"""
        
        st.sidebar.markdown('<div class="sidebar-logo">🔑 API Setup</div>', unsafe_allow_html=True)
        
        # Check for existing API key from environment
        existing_key = os.getenv("OPENAI_API_KEY")
        if existing_key and not st.session_state.api_key_valid:
            try:
                st.session_state.generator = BusinessIdeaGenerator(existing_key)
                st.session_state.api_key_valid = True
                st.sidebar.success("✅ API Key loaded from environment")
                return True
            except:
                pass
        
        if not st.session_state.api_key_valid:
            st.sidebar.markdown("### OpenAI API Configuration")
            
            api_key = st.sidebar.text_input(
                "Enter your OpenAI API Key:",
                type="password",
                help="Get your API key from https://platform.openai.com/api-keys",
                placeholder="sk-..."
            )
            
            if st.sidebar.button("🔗 Get API Key", help="Opens OpenAI platform in new tab"):
                st.sidebar.markdown("[Get your API key here](https://platform.openai.com/api-keys)")
            
            if api_key:
                if self.validator.validate_api_key(api_key):
                    try:
                        st.session_state.generator = BusinessIdeaGenerator(api_key)
                        st.session_state.api_key_valid = True
                        st.sidebar.success("✅ API Key validated successfully!")
                        st.rerun()
                    except Exception as e:
                        st.sidebar.error(f"❌ API Key validation failed: {str(e)}")
                        return False
                else:
                    st.sidebar.error("❌ Invalid API key format. Should start with 'sk-'")
                    return False
        
        return st.session_state.api_key_valid
    
    def render_header(self):
        """Render the application header with enhanced styling"""
        
        st.markdown('<h1 class="main-header">💡 Business Idea Creator</h1>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; padding: 1rem; border-radius: 15px; margin-bottom: 2rem;">
                <h3 style="margin: 0; color: white;">🚀 Advanced AI Prompt Engineering System</h3>
                <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
                    Generate innovative business ideas using cutting-edge AI technology
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    def render_sidebar_controls(self):
        """Render sidebar input controls with enhanced UI"""
        
        st.sidebar.markdown("---")
        st.sidebar.markdown('<div class="sidebar-logo">📝 Business Parameters</div>', unsafe_allow_html=True)
        
        # Industry selection
        industries = [
            "Technology", "Healthcare", "Finance", "Retail", "Education", 
            "Manufacturing", "Real Estate", "Food & Beverage", "Transportation",
            "Entertainment", "Energy", "Agriculture", "Construction", "Consulting",
            "E-commerce", "Gaming", "Travel", "Fitness", "Beauty", "Other"
        ]
        
        industry = st.sidebar.selectbox(
            "🏭 Industry Sector:",
            industries,
            help="Select the primary industry for your business idea"
        )
        
        # Target audience
        target_audiences = [
            "Millennials (25-40)", "Gen Z (18-24)", "Gen X (41-56)", "Baby Boomers (57+)",
            "Small Businesses", "Enterprise Companies", "Students", "Working Professionals",
            "Parents & Families", "Seniors", "Creative Professionals", "Healthcare Workers",
            "Entrepreneurs", "Remote Workers", "Tech Enthusiasts", "Other"
        ]
        
        target_audience = st.sidebar.selectbox(
            "🎯 Target Audience:",
            target_audiences,
            help="Who is your primary target customer?"
        )
        
        # Market trends (multi-select with enhanced options)
        available_trends = [
            "Artificial Intelligence", "Sustainability", "Remote Work", "E-commerce",
            "Mobile-First", "Social Commerce", "Personalization", "Automation",
            "Digital Health", "Cryptocurrency", "Augmented Reality", "Internet of Things",
            "Cybersecurity", "Clean Energy", "Circular Economy", "Virtual Reality",
            "Blockchain", "5G Technology", "Cloud Computing", "Data Privacy"
        ]
        
        market_trends = st.sidebar.multiselect(
            "📈 Market Trends:",
            available_trends,
            default=["Artificial Intelligence", "Sustainability"],
            help="Select 2-5 trends that should influence your business ideas"
        )
        
        # Budget range
        budget_ranges = [
            "Under $10K", "$10K - $50K", "$50K - $100K", "$100K - $500K",
            "$500K - $1M", "$1M - $5M", "Over $5M", "Seeking Investment"
        ]
        
        budget_range = st.sidebar.selectbox(
            "💰 Budget Range:",
            budget_ranges,
            index=2,
            help="What's your available budget for starting this business?"
        )
        
        # Geographical focus
        geographical_focuses = [
            "Local (City/Region)", "National", "North America", "Europe", 
            "Asia Pacific", "Latin America", "Global", "Emerging Markets"
        ]
        
        geographical_focus = st.sidebar.selectbox(
            "🌍 Geographical Focus:",
            geographical_focuses,
            index=2,
            help="What geographical market are you targeting?"
        )
        
        # Innovation level
        innovation_levels = [
            "Incremental (Improve existing solutions)", 
            "Disruptive (Change industry dynamics)", 
            "Breakthrough (Create entirely new market)"
        ]
        
        innovation_level = st.sidebar.radio(
            "🚀 Innovation Level:",
            innovation_levels,
            help="What level of innovation are you aiming for?"
        )
        
        st.sidebar.markdown("---")
        
        # Advanced options
        with st.sidebar.expander("⚙️ Advanced Settings"):
            technique = st.selectbox(
                "Prompt Engineering Technique:",
                ["chain_of_thought", "few_shot_examples", "directional_stimulus"],
                help="Select the AI prompting approach"
            )
            
            model = st.selectbox(
                "AI Model:",
                ["gpt-3.5-turbo", "gpt-4"],
                help="GPT-4 provides better results but costs more"
            )
            
            creativity = st.slider(
                "Creativity Level:",
                min_value=0.1,
                max_value=1.0,
                value=0.8,
                step=0.1,
                help="Higher values = more creative ideas"
            )
        
        return {
            "industry": industry,
            "target_audience": target_audience,
            "market_trends": market_trends,
            "budget_range": budget_range,
            "geographical_focus": geographical_focus,
            "innovation_level": innovation_level.split(" (")[0].lower(),
            "technique": technique,
            "model": model,
            "creativity": creativity
        }
    
    def render_main_content(self, params):
        """Render main content area with idea generation"""
        
        # Generation section
        st.markdown('<h2 class="sub-header">🎯 Generate Business Ideas</h2>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            generate_button = st.button(
                "🚀 Generate Innovative Ideas", 
                type="primary", 
                use_container_width=True,
                help="Click to generate AI-powered business ideas"
            )
            
            if generate_button:
                # Input validation
                validation_errors = self.validator.validate_inputs(params)
                if validation_errors:
                    for error in validation_errors:
                        st.error(f"❌ {error}")
                    return
                
                # Show generation progress
                progress_container = st.container()
                with progress_container:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        # Step 1: Initialize
                        status_text.markdown("🔄 **Initializing AI system...**")
                        progress_bar.progress(10)
                        time.sleep(0.5)
                        
                        # Step 2: Create request
                        status_text.markdown("📝 **Creating business idea request...**")
                        progress_bar.progress(25)
                        
                        request = BusinessIdeaRequest(
                            industry=params["industry"],
                            target_audience=params["target_audience"],
                            market_trends=params["market_trends"],
                            budget_range=params["budget_range"],
                            geographical_focus=params["geographical_focus"],
                            innovation_level=params["innovation_level"]
                        )
                        time.sleep(0.5)
                        
                        # Step 3: Generate prompts
                        status_text.markdown("🧠 **Generating AI prompts...**")
                        progress_bar.progress(50)
                        time.sleep(1)
                        
                        # Step 4: AI Processing
                        status_text.markdown("🤖 **AI is analyzing trends and generating ideas...**")
                        progress_bar.progress(75)
                        
                        # Generate ideas
                        results = st.session_state.generator.generate_ideas(
                            request,
                            technique=params["technique"],
                            model=params["model"]
                        )
                        
                        # Step 5: Finalize
                        status_text.markdown("✨ **Finalizing results...**")
                        progress_bar.progress(100)
                        time.sleep(0.5)
                        
                        # Store results
                        st.session_state.current_results = results
                        st.session_state.generation_history.append(results)
                        
                        # Clear progress
                        progress_bar.empty()
                        status_text.empty()
                        
                        # Success message
                        st.markdown(
                            f'<div class="success-message">'
                            f'🎉 <strong>Success!</strong> Generated {len(results["generated_ideas"])} '
                            f'innovative business ideas using {params["technique"]} prompting technique!'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                        
                    except Exception as e:
                        progress_bar.empty()
                        status_text.empty()
                        st.error(f"❌ **Error generating ideas:** {str(e)}")
                        st.info("💡 **Tip:** Make sure your API key is valid and you have sufficient OpenAI credits.")
        
        # Display results if available
        if st.session_state.current_results:
            self.render_results(st.session_state.current_results)
    
    def render_results(self, results: Dict[str, Any]):
        """Render generated business ideas with enhanced formatting"""
        
        st.markdown("---")
        st.markdown('<h2 class="sub-header">🚀 Your Generated Business Ideas</h2>', unsafe_allow_html=True)
        
        # Results overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(
                f'<div class="metric-card">'
                f'<h2 style="color: #1f77b4; margin: 0;">{len(results["generated_ideas"])}</h2>'
                f'<p style="margin: 0;">Ideas Generated</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                f'<div class="metric-card">'
                f'<h2 style="color: #ff7f0e; margin: 0;">{results.get("technique_used", "AI").title()}</h2>'
                f'<p style="margin: 0;">AI Technique</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(
                f'<div class="metric-card">'
                f'<h2 style="color: #2ca02c; margin: 0;">{results.get("model_used", "GPT")}</h2>'
                f'<p style="margin: 0;">AI Model</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with col4:
            timestamp = results.get("timestamp", datetime.now().isoformat())
            formatted_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00')).strftime("%H:%M")
            st.markdown(
                f'<div class="metric-card">'
                f'<h2 style="color: #d62728; margin: 0;">{formatted_time}</h2>'
                f'<p style="margin: 0;">Generated</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        st.markdown("---")
        
        # Display each business idea
        for i, idea in enumerate(results["generated_ideas"], 1):
            with st.container():
                st.markdown(
                    f'<div class="idea-card">'
                    f'<h3 style="color: #1f77b4; margin-top: 0;">💡 Business Idea #{i}: {idea.get("name", f"Innovative Idea {i}")}</h3>',
                    unsafe_allow_html=True
                )
                
                # Create tabs for different aspects
                tab1, tab2, tab3, tab4 = st.tabs(["📋 Overview", "🎯 Market & Revenue", "🏆 Strategy", "📊 Implementation"])
                
                with tab1:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if idea.get('problem'):
                            st.markdown("**🎯 Problem Statement:**")
                            st.markdown(idea['problem'])
                            st.markdown("---")
                        
                        if idea.get('solution'):
                            st.markdown("**💡 Solution Overview:**")
                            st.markdown(idea['solution'])
                    
                    with col2:
                        if idea.get('target_market'):
                            st.markdown("**👥 Target Market:**")
                            st.markdown(idea['target_market'])
                            st.markdown("---")
                        
                        if idea.get('competitive_edge'):
                            st.markdown("**🏆 Competitive Advantage:**")
                            st.markdown(idea['competitive_edge'])
                
                with tab2:
                    if idea.get('revenue_model'):
                        st.markdown("**💰 Revenue Model:**")
                        st.markdown(idea['revenue_model'])
                        st.markdown("---")
                    
                    # Add market insights
                    if hasattr(self, 'data_processor'):
                        insights = self.data_processor.get_industry_insights(results.get("input_parameters", {}).get("industry", ""))
                        if insights:
                            st.markdown("**📈 Market Insights:**")
                            for key, value in insights.items():
                                if isinstance(value, list):
                                    st.markdown(f"- **{key.title()}:** {', '.join(value)}")
                                else:
                                    st.markdown(f"- **{key.title()}:** {value}")
                
                with tab3:
                    if idea.get('implementation'):
                        st.markdown("**🚀 Implementation Strategy:**")
                        st.markdown(idea['implementation'])
                        st.markdown("---")
                    
                    # Add strategic considerations
                    st.markdown("**💡 Strategic Considerations:**")
                    considerations = [
                        "Conduct thorough market research",
                        "Develop MVP (Minimum Viable Product)",
                        "Build strategic partnerships",
                        "Secure appropriate funding",
                        "Focus on customer feedback and iteration"
                    ]
                    for consideration in considerations:
                        st.markdown(f"- {consideration}")
                
                with tab4:
                    if idea.get('success_metrics'):
                        st.markdown("**📊 Success Metrics:**")
                        st.markdown(idea['success_metrics'])
                        st.markdown("---")
                    
                    # Add timeline suggestions
                    st.markdown("**⏰ Suggested Timeline:**")
                    timeline = [
                        "**Months 1-2:** Market research and validation",
                        "**Months 3-4:** MVP development",
                        "**Months 5-6:** Beta testing and refinement", 
                        "**Months 7-8:** Launch and initial marketing",
                        "**Months 9-12:** Scale and optimize"
                    ]
                    for phase in timeline:
                        st.markdown(f"- {phase}")
                
                # Action buttons
                st.markdown("---")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button(f"📋 Save Idea #{i}", key=f"save_{i}"):
                        # Save to session state or file
                        if 'saved_ideas' not in st.session_state:
                            st.session_state.saved_ideas = []
                        st.session_state.saved_ideas.append(idea)
                        st.success(f"✅ Idea #{i} saved to favorites!")
                
                with col2:
                    if st.button(f"📤 Export #{i}", key=f"export_{i}"):
                        # Create exportable format
                        export_data = {
                            "idea_name": idea.get("name", f"Business Idea {i}"),
                            "generated_at": datetime.now().isoformat(),
                            "details": idea
                        }
                        st.download_button(
                            label=f"⬇️ Download Idea #{i}",
                            data=json.dumps(export_data, indent=2),
                            file_name=f"business_idea_{i}_{datetime.now().strftime('%Y%m%d')}.json",
                            mime="application/json",
                            key=f"download_{i}"
                        )
                
                with col3:
                    if st.button(f"🔄 Refine #{i}", key=f"refine_{i}"):
                        st.info(f"💡 Refinement feature coming soon! Idea #{i} will be enhanced based on additional parameters.")
                
                with col4:
                    if st.button(f"📊 Analyze #{i}", key=f"analyze_{i}"):
                        st.info(f"📈 Market analysis for Idea #{i} coming soon!")
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("---")
        
        # Export all ideas
        st.markdown('<h3 class="sub-header">📤 Export All Ideas</h3>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            all_ideas_json = json.dumps(results, indent=2, default=str)
            st.download_button(
                "📄 Download as JSON",
                data=all_ideas_json,
                file_name=f"business_ideas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col2:
            # Create CSV format
            csv_data = []
            for i, idea in enumerate(results["generated_ideas"], 1):
                csv_data.append({
                    "Idea #": i,
                    "Name": idea.get("name", f"Idea {i}"),
                    "Problem": idea.get("problem", ""),
                    "Solution": idea.get("solution", ""),
                    "Target Market": idea.get("target_market", ""),
                    "Revenue Model": idea.get("revenue_model", ""),
                    "Competitive Edge": idea.get("competitive_edge", ""),
                    "Implementation": idea.get("implementation", ""),
                    "Success Metrics": idea.get("success_metrics", "")
                })
            
            csv_df = pd.DataFrame(csv_data)
            st.download_button(
                "📊 Download as CSV",
                data=csv_df.to_csv(index=False),
                file_name=f"business_ideas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col3:
            st.button(
                "📧 Email Ideas",
                help="Email functionality coming soon!",
                use_container_width=True
            )
    
    def render_analytics_tab(self):
        """Render analytics dashboard"""
        
        st.markdown('<h2 class="sub-header">📈 Generation Analytics</h2>', unsafe_allow_html=True)
        
        if not st.session_state.generation_history:
            st.markdown(
                '<div class="info-box">'
                '📊 Generate some business ideas to see analytics here!'
                '</div>',
                unsafe_allow_html=True
            )
            return
        
        # Calculate statistics
        total_generations = len(st.session_state.generation_history)
        total_ideas = sum(len(gen["generated_ideas"]) for gen in st.session_state.generation_history)
        avg_ideas = total_ideas / total_generations if total_generations > 0 else 0
        
        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Generations", total_generations)
        
        with col2:
            st.metric("Total Ideas Created", total_ideas)
        
        with col3:
            st.metric("Average Ideas per Session", f"{avg_ideas:.1f}")
        
        with col4:
            if st.session_state.generation_history:
                latest = st.session_state.generation_history[-1]["timestamp"]
                latest_time = datetime.fromisoformat(latest.replace('Z', '+00:00')).strftime("%m/%d %H:%M")
                st.metric("Last Generation", latest_time)
        
        # Charts
        if total_generations > 0:
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Industry distribution
                industries = {}
                for gen in st.session_state.generation_history:
                    industry = gen.get("input_parameters", {}).get("industry", "Unknown")
                    industries[industry] = industries.get(industry, 0) + 1
                
                if industries:
                    fig_pie = px.pie(
                        values=list(industries.values()),
                        names=list(industries.keys()),
                        title="Ideas Generated by Industry"
                    )
                    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Technique usage
                techniques = {}
                for gen in st.session_state.generation_history:
                    technique = gen.get("technique_used", "Unknown")
                    techniques[technique] = techniques.get(technique, 0) + 1
                
                if techniques:
                    fig_bar = px.bar(
                        x=list(techniques.keys()),
                        y=list(techniques.values()),
                        title="AI Techniques Used",
                        labels={"x": "Technique", "y": "Usage Count"}
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
            
            # Generation timeline
            if len(st.session_state.generation_history) > 1:
                st.markdown("---")
                st.markdown("### 📅 Generation Timeline")
                
                timeline_data = []
                for gen in st.session_state.generation_history:
                    timestamp = gen.get("timestamp", "")
                    if timestamp:
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        timeline_data.append({
                            "Time": dt,
                            "Ideas Generated": len(gen["generated_ideas"]),
                            "Industry": gen.get("input_parameters", {}).get("industry", "Unknown")
                        })
                
                if timeline_data:
                    timeline_df = pd.DataFrame(timeline_data)
                    fig_timeline = px.line(
                        timeline_df,
                        x="Time",
                        y="Ideas Generated",
                        color="Industry",
                        title="Ideas Generated Over Time",
                        markers=True
                    )
                    st.plotly_chart(fig_timeline, use_container_width=True)
    
    def render_about_tab(self):
        """Render about page with project information"""
        
        st.markdown('<h2 class="sub-header">ℹ️ About Business Idea Creator</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
        <h3>🎯 Project Overview</h3>
        <p>
        This application demonstrates advanced <strong>prompt engineering techniques</strong> to generate 
        innovative business ideas using AI. Built as a comprehensive project showcasing the power of 
        combining artificial intelligence with strategic business thinking.
        </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Technical features
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🔧 Technical Features
            
            - **Advanced Prompt Engineering**: Chain-of-Thought, Few-Shot, and Directional Stimulus prompting
            - **Context-Aware Generation**: Incorporates industry trends and market conditions
            - **Interactive Web Interface**: Professional Streamlit-based UI
            - **Export Capabilities**: Multiple formats (JSON, CSV, email)
            - **Analytics Dashboard**: Generation history and performance metrics
            - **Responsive Design**: Works on desktop and mobile devices
            """)
        
        with col2:
            st.markdown("""
            ### 🚀 AI Techniques Used
            
            1. **Chain-of-Thought Prompting**: Step-by-step reasoning for better idea generation
            2. **Few-Shot Learning**: Example-based guidance for consistent outputs
            3. **Context Amplification**: Industry-specific data enrichment
            4. **Directional Stimulus**: Targeted prompting for specific outcomes
            5. **Multi-Modal Analysis**: Combining text and market data
            6. **Iterative Refinement**: Continuous improvement of generated ideas
            """)
        
        st.markdown("---")
        
        # Architecture diagram
        st.markdown("""
        ### 📊 System Architecture
        
        ```
        ┌─────────────────────────────────────────────────────────────┐
        │                    User Interface (Streamlit)               │
        ├─────────────────────────────────────────────────────────────┤
        │  Business Logic Layer                                       │
        │  ├── Prompt Engineering System (prompt_engine.py)          │
        │  ├── Business Idea Generator (idea_generator.py)           │
        │  ├── Data Processing Utilities (utils/)                    │
        │  └── Input Validation & Analytics                          │
        ├─────────────────────────────────────────────────────────────┤
        │  External Services                                          │
        │  ├── OpenAI GPT API                                        │
        │  ├── Market Data Sources                                   │
        │  └── Export Services                                       │
        └─────────────────────────────────────────────────────────────┘
        ```
        """)
        
        # Project statistics
        st.markdown("---")
        st.markdown("### 📈 Project Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Lines of Code", "2,500+", help="Total lines of Python code")
        
        with col2:
            st.metric("AI Techniques", "4", help="Different prompt engineering methods")
        
        with col3:
            st.metric("Industries Supported", "20+", help="Different business sectors")
        
        with col4:
            st.metric("Export Formats", "3", help="JSON, CSV, Email")
        
        # Contact and links
        st.markdown("---")
        st.markdown("""
        ### 📧 Contact & Resources
        
        - **Developer**: Your Name
        - **Email**: your.email@example.com
        - **GitHub**: [Project Repository](https://github.com/your-username/business-idea-creator)
        - **LinkedIn**: [Your LinkedIn Profile]
        - **Portfolio**: [Your Portfolio Website]
        
        ### 🙏 Acknowledgments
        
        - **Vault of Codes** team for internship opportunity
        - **OpenAI** for providing the GPT API
        - **Streamlit** community for the excellent framework
        - **Python** ecosystem for amazing libraries
        """)
        
        # Version info
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.9rem;">
        Business Idea Creator v1.0.0 | Built with ❤️ using Python & AI
        </div>
        """, unsafe_allow_html=True)
    
    def run(self):
        """Main application entry point"""
        
        # Render header
        self.render_header()
        
        # Setup API key
        if not self.setup_api_key():
            st.markdown(
                '<div class="info-box">'
                '⚠️ <strong>API Key Required:</strong> Please enter a valid OpenAI API key to continue.'
                '</div>',
                unsafe_allow_html=True
            )
            
            with st.expander("📋 How to get an OpenAI API Key", expanded=True):
                st.markdown("""
                ### Steps to get your API key:
                
                1. **Visit OpenAI Platform**: Go to [platform.openai.com](https://platform.openai.com/api-keys)
                2. **Sign Up/Login**: Create an account or sign in
                3. **Navigate to API Keys**: Find the API Keys section
                4. **Create New Key**: Click "Create new secret key"
                5. **Copy Key**: Copy the key (starts with 'sk-')
                6. **Paste Here**: Enter the key in the sidebar
                
                ### 💡 Tips:
                - Keep your API key secure and private
                - Monitor your usage to avoid unexpected charges
                - Start with small tests to understand costs
                """)
            return
        
        # Create main tabs
        tab1, tab2, tab3 = st.tabs(["🎯 Generate Ideas", "📊 Analytics", "ℹ️ About"])
        
        with tab1:
            # Get sidebar parameters
            params = self.render_sidebar_controls()
            
            # Render main content
            self.render_main_content(params)
        
        with tab2:
            self.render_analytics_tab()
        
        with tab3:
            self.render_about_tab()
        
        # Footer
        st.markdown("---")
        st.markdown(
            """
            <div style="text-align: center; padding: 1rem; color: #666;">
                <p>🚀 <strong>Business Idea Creator</strong> | Powered by Advanced AI & Prompt Engineering</p>
                <p style="font-size: 0.8rem;">
                    Built with Streamlit • OpenAI GPT • Python | 
                    <a href="https://github.com/your-username/business-idea-creator" target="_blank">View on GitHub</a>
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )

# Application entry point
def main():
    """Main application function"""
    try:
        app = BusinessIdeaApp()
        app.run()
    except Exception as e:
        st.error(f"⚠️ Application Error: {str(e)}")
        st.info("💡 Please refresh the page or contact support if the issue persists.")

if __name__ == "__main__":
    main()