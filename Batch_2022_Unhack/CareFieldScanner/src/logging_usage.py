from custom_logging import setup_logger

# Setup the logger
logger = setup_logger()

logger.info(f"Attempting to read the input file ...")
logger.success(f"Successfully parsed the input file .")
logger.error(f"Error during point generation or rotation")
