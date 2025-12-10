"""Enhancement modules for advanced fake news detection"""

# Only import visual detector for now (other modules have dependency issues)
try:
    from .visual_detector import VisualFakeNewsDetector
except ImportError as e:
    print(f"Warning: Could not import VisualFakeNewsDetector: {e}")
    VisualFakeNewsDetector = None

__all__ = ['VisualFakeNewsDetector']
