"""
Assets Package - Static assets (images, logos, etc.)
"""

from pathlib import Path

ASSETS_DIR = Path(__file__).parent

__all__ = ['ASSETS_DIR']