import sys
from pathlib import Path

# A workaround for tests not automatically setting
# root/src/ as the current working directory
path_to_src = Path(__file__).parent.parent / "one_max_genetic_algorithm_python"
sys.path.insert(0, str(path_to_src))
