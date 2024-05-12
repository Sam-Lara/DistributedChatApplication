import os
import sys

# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory
parent_dir = os.path.dirname(current_dir)
# Construct the path to the 'src' directory
src_dir = os.path.join(parent_dir, 'src')
print(src_dir)
# Add the 'src' directory to the Python path
sys.path.append(src_dir)

# Now you can import modules from the 'src' directory
from peer import Peer


Peer("boof").start_server(10000)
