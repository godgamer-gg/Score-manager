import sys
import os
import site

# Get the directory containing this script
base_dir = os.path.dirname(os.path.abspath(__file__))

# Add the base directory to Python's path
sys.path.insert(0, base_dir)

# Create a .pth file in the site-packages directory
with open(os.path.join(site.getsitepackages()[0], "score-manager.pth"), "w") as f:
    f.write(base_dir)
