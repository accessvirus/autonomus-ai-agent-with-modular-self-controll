# C:\Users\m.2 SSD\Desktop\lastagent\agent006\logger_setup.py
import logging
import sys
from collections import deque

# Configuration for the operational context log buffer
MAX_OPERATIONAL_CONTEXT_LOG_ENTRIES = 100 # Example value, configure as needed
OPERATIONAL_CONTEXT_LOG_BUFFER = deque(maxlen=MAX_OPERATIONAL_CONTEXT_LOG_ENTRIES)

class ContextualLogger(logging.Logger):
    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=1):
        # Add to operational context buffer
        # Create a basic LogRecord. Note: filename, lineno, funcname will be placeholders
        # as findCaller() is typically called later in the standard logging process.
        log_entry = self.makeRecord(self.name, level, "(unknown file)", 0, msg, args, exc_info, func="(unknown function)")

        # Attempt to format this record for the buffer.
        # Default to the basic message string.
        formatted_message_for_buffer = log_entry.getMessage()

        if self.handlers and len(self.handlers) > 0:
            first_handler = self.handlers[0]
            if first_handler.formatter:
                try:
                    # Use the first handler's formatter (e.g., console_handler's formatter).
                    # This formatter should ideally not rely on fields like filename/lineno
                    # if they are critical, as they are placeholders in log_entry here.
                    # The default console_formatter ('%(asctime)s - %(levelname)s - %(message)s') is fine.
                    formatted_message_for_buffer = first_handler.formatter.format(log_entry)
                except Exception:
                    # If formatting fails for any reason, the basic message (already set) will be used.
                    pass
        OPERATIONAL_CONTEXT_LOG_BUFFER.append(formatted_message_for_buffer)

        # Call the original _log method to continue the standard logging process.
        # super()._log will eventually call findCaller() to get correct file/line info
        # for the LogRecord that gets passed to the handlers.
        super()._log(level, msg, args, exc_info, extra, stack_info, stacklevel)

logging.setLoggerClass(ContextualLogger)

sys_logger = logging.getLogger('Agent006SystemLogger')
sys_logger.setLevel(logging.DEBUG)

# Console Handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
sys_logger.addHandler(console_handler)

# File Handler
try:
    file_handler = logging.FileHandler('C:\\Users\\m.2 SSD\\Desktop\\lastagent\\agent006\\agent006_ops.log', mode='a')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
    file_handler.setFormatter(file_formatter)
    sys_logger.addHandler(file_handler)
except Exception as e:
    sys_logger.error(f"Failed to initialize file logger: {e}", exc_info=True)

# Override print to capture its output into the operational context buffer
_original_print = print
def contextual_print(*args, **kwargs):
    # Construct the message string
    message = " ".join(map(str, args))
    OPERATIONAL_CONTEXT_LOG_BUFFER.append(f"PRINT: {message}")
    _original_print(*args, **kwargs)

__builtins__['print'] = contextual_print

sys_logger.info("Logger setup complete for agent006. Print statements are now contextually logged.")