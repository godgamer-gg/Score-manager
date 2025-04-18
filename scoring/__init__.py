import os
import sys

# Add the directory containing this package to Python's path
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# Import the ScoreManager class
from .scoreManager import ScoreManager
