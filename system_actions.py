# C:\Users\m.2 SSD\Desktop\lastagent\agent006\system_actions.py
"""
Defines the concrete actions the agent can perform on the system,
such as file I/O, code execution (via SelfModificationSuite), etc.
Evolved from agent005's version."""
import os

class SystemActions:
    def __init__(self, config, logger, advanced_memory_system, self_modification_suite):
        self.config = config
        self.logger = logger
        self.ams = advanced_memory_system
        self.sms = self_modification_suite
        self.logger.info("SystemActions (agent006) initialized.")

    def create_folder(self, folder_path):
        """
        Creates a folder at the specified path.
        Creates parent directories if they don't exist.
        """
        try:
            os.makedirs(folder_path, exist_ok=True)
            self.logger.info(f"SystemActions: Successfully created folder (and any parents): {folder_path}")
            return {"success": True, "path": folder_path}
        except OSError as e:
            self.logger.error(f"SystemActions: Failed to create folder {folder_path}. Error: {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    def create_file(self, file_path, content=""):
        """
        Creates a file at the specified path with the given content.
        Overwrites if the file already exists. Creates parent directories.
        """
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.logger.info(f"SystemActions: Successfully created/updated file: {file_path}")
            return {"success": True, "path": file_path}
        except IOError as e:
            self.logger.error(f"SystemActions: Failed to create/write file {file_path}. Error: {e}", exc_info=True)
            return {"success": False, "error": str(e)}