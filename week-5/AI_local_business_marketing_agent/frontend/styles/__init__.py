"""
Styles Package
"""

from pathlib import Path

def load_css():
    """Load custom CSS"""
    css_file = Path(__file__).parent / 'custom.css'
    if css_file.exists():
        with open(css_file, 'r') as f:
            return f.read()
    return ""

__all__ = ['load_css']