import logging
from colorama import Fore, Style


# Custom Formatter for colored logs
class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.ERROR: Fore.RED + Style.BRIGHT,
        logging.WARNING: Fore.YELLOW + Style.BRIGHT,
        logging.INFO: Fore.BLUE + Style.BRIGHT,
        logging.DEBUG: Fore.CYAN,
        25: Fore.GREEN + Style.BRIGHT,  # Success level (custom)
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelno, "")
        reset = Style.RESET_ALL
        log_fmt = f"{log_color}[%(levelname)s] %(message)s{reset}"
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# Add custom log level for success
SUCCESS_LEVEL = 25
logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")


# Custom logger functions
def log_success(self, message, *args, **kwargs):
    if self.isEnabledFor(SUCCESS_LEVEL):
        self._log(SUCCESS_LEVEL, message, args, **kwargs)


logging.Logger.success = log_success


def setup_logger(name="app_logger", level=logging.DEBUG):  # Set default level to DEBUG
    logger = logging.getLogger(name)
    logger.setLevel(level)  # Set logger level
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColorFormatter())
    logger.addHandler(console_handler)
    return logger
