import logging
import sys

# Disable any existing handlers
logging.getLogger().handlers = []

# Configure root logger
logging.getLogger().setLevel(logging.DEBUG)  # Set root logger to DEBUG

# Create logger
logger = logging.getLogger("obsidian_ai_logger")
logger.setLevel(logging.DEBUG)
logger.propagate = False  # Don't propagate to root logger to avoid duplicate messages

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

# Format logs with more detail
formatter = logging.Formatter("[%(levelname)s] %(asctime)s | %(name)s | %(message)s")
console_handler.setFormatter(formatter)

# Add handler to both loggers
logger.addHandler(console_handler)
logging.getLogger().addHandler(console_handler)

# Ensure all our modules log at DEBUG level
for module in ['common', 'embeddings', 'topics']:
    mod_logger = logging.getLogger(module)
    mod_logger.setLevel(logging.DEBUG)
    mod_logger.propagate = True
