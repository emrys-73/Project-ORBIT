import logging
import sys

# Configure root logger
logger = logging.getLogger("obsidian_ai_logger")
logger.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

# Format logs
formatter = logging.Formatter("[%(levelname)s] %(asctime)s | %(name)s | %(message)s")
console_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(console_handler)
