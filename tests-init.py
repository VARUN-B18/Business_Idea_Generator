# tests/__init__.py
"""
Test package for Business Idea Creator
"""

import sys
import os

# Add src to Python path for testing
project_root = os.path.dirname(os.path.dirname(__file__))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)