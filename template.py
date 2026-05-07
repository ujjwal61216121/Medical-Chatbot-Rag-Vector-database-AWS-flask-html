# import os
# from pathlib import Path
# import logging

# logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')


# list_of_files = [
#     "src/__init__.py",
#     "src/helper.py",
#     "src/prompt.py",
#     ".env",
#     "setup.py",
#     "research/trials.ipynb",
#     "app.py",
#     "store_index.py",
#     "static/.gitkeep",
#     "templates/chat.html"

# ]


# for filepath in list_of_files:
#    filepath = Path(filepath)
#    filedir, filename = os.path.split(filepath)

#    if filedir !="":
#       os.makedirs(filedir, exist_ok=True)
#       logging.info(f"Creating directory; {filedir} for the file {filename}")

#    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
#       with open(filepath, 'w') as f:
#          pass
#          logging.info(f"Creating empty file: {filepath}")

#    else:
#       logging.info(f"{filename} is already created")
      
      
import os
import logging
from pathlib import Path

# =========================
# LOGGING CONFIG
# =========================

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s'
)

# =========================
# PROJECT FILE STRUCTURE
# =========================

list_of_files = [
    "src/__init__.py",
    "src/helper.py",
    "src/prompt.py",
    ".env",
    "setup.py",
    "research/trials.ipynb",
    "app.py",
    "store_index.py",
    "static/.gitkeep",
    "templates/chat.html"
]

# =========================
# CREATE FILES & DIRECTORIES
# =========================

for filepath in list_of_files:

    filepath = Path(filepath)

    filedir = filepath.parent
    filename = filepath.name

    # Create directories
    if filedir != Path("."):
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Created directory: {filedir}")

    # Create empty file if not exists
    if not filepath.exists() or filepath.stat().st_size == 0:

        filepath.touch(exist_ok=True)

        logging.info(f"Created file: {filepath}")

    else:
        logging.info(f"File already exists: {filename}")    