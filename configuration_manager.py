import logging
import json
import os

class ConfigurationManager:
    """
    Manages application or agent configuration settings.
    Allows loading from and saving to a JSON configuration file,
    and provides methods to get and set configuration values, including nested ones.
    """

    def __init__(self, logger: logging.Logger, config_file_path: str = "config.json"):
        """
        Initializes the ConfigurationManager.

        Args:
            logger (logging.Logger): A logger instance for logging messages.
            config_file_path (str): Path to the JSON configuration file.
                                    Defaults to 'config.json' in the current working directory.
        """
        self.logger = logger
        self.config_file_path = config_file_path
        self.config_data = {}
        self.logger.info(f"ConfigurationManager initialized with config file: {self.config_file_path}")
        self.load_settings()

    def _get_nested_dict(self, keys: list, create_if_missing: bool = False) -> tuple[dict | None, str | None]:
        """
        Helper function to traverse or create nested dictionaries.
        Returns the parent dictionary of the target key and the final key.
        """
        current_level = self.config_data
        for i in range(len(keys) - 1):
            key = keys[i]
            if key not in current_level:
                if create_if_missing:
                    current_level[key] = {}
                else:
                    return None, None
            if not isinstance(current_level[key], dict):
                if create_if_missing:
                    # Overwrite if not a dict and creation is allowed (potentially dangerous)
                    self.logger.warning(f"Overwriting non-dict key '{key}' with a new dictionary.")
                    current_level[key] = {}
                else:
                    self.logger.error(f"Key '{key}' exists but is not a dictionary.")
                    return None, None
            current_level = current_level[key]
        return current_level, keys[-1]

    def get_setting(self, key_path: str, default: any = None) -> any:
        """
        Retrieves a setting using a dot-separated key path (e.g., "database.host").

        This is a placeholder method in terms of advanced error handling or type checking,
        but provides basic functionality for retrieving nested settings.

        Args:
            key_path (str): The dot-separated path to the setting.
            default (any, optional): The value to return if the setting is not found. Defaults to None.

        Returns:
            any: The value of the setting, or the default value if not found.

        Example Usage:
            # config_manager = ConfigurationManager(logger, "my_app_config.json")
            # db_host = config_manager.get_setting("database.host", "localhost")
            # api_key = config_manager.get_setting("external_services.weather_api.key")
            # if api_key:
            #     print(f"Using API key: {api_key}")
            # else:
            #     print("Weather API key not found.")
        """
        self.logger.debug(f"Attempting to get setting: '{key_path}' with default: {default}")
        keys = key_path.split('.')
        
        parent_dict, final_key = self._get_nested_dict(keys, create_if_missing=False)

        if parent_dict is not None and final_key is not None and final_key in parent_dict:
            value = parent_dict[final_key]
            self.logger.info(f"Retrieved setting '{key_path}': {value}")
            return value
        else:
            self.logger.info(f"Setting '{key_path}' not found. Returning default value: {default}")
            return default

    def set_setting(self, key_path: str, value: any) -> bool:
        """
        Sets a configuration value using a dot-separated key path (e.g., "database.port").
        If the path includes non-existent nested dictionaries, they will be created.

        This is a placeholder method in terms of complex validation, but allows setting values.

        Args:
            key_path (str): The dot-separated path to the setting.
            value (any): The value to set for the configuration key.

        Returns:
            bool: True if the setting was successfully set, False otherwise (though current placeholder always returns True).

        Example Usage:
            # config_manager.set_setting("user_preferences.theme", "dark")
            # config_manager.set_setting("timeouts.network", 30)
            # config_manager.save_settings() # Important to persist changes
        """
        self.logger.debug(f"Attempting to set setting: '{key_path}' to value: {value}")
        keys = key_path.split('.')
        
        parent_dict, final_key = self._get_nested_dict(keys, create_if_missing=True)

        if parent_dict is not None and final_key is not None:
            parent_dict[final_key] = value
            self.logger.info(f"Set setting '{key_path}' to: {value}")
            return True
        else:
            self.logger.error(f"Failed to set setting '{key_path}' due to path traversal/creation issue.")
            return False

    def load_settings(self) -> bool:
        """
        Loads configuration settings from the JSON file specified by self.config_file_path.
        If the file does not exist, it logs a message and continues with empty config_data.

        Returns:
            bool: True if settings were loaded or file doesn't exist (graceful), False on a load error.
        """
        if os.path.exists(self.config_file_path):
            try:
                with open(self.config_file_path, 'r') as f:
                    self.config_data = json.load(f)
                self.logger.info(f"Successfully loaded configuration from {self.config_file_path}")
                return True
            except json.JSONDecodeError as e:
                self.logger.error(f"Error decoding JSON from {self.config_file_path}: {e}")
                self.config_data = {} # Reset to empty on error
                return False
            except Exception as e:
                self.logger.error(f"Failed to load configuration from {self.config_file_path}: {e}")
                self.config_data = {} # Reset to empty on error
                return False
        else:
            self.logger.info(f"Configuration file {self.config_file_path} not found. Starting with empty configuration.")
            self.config_data = {}
            return True # Not an error if file doesn't exist, just means fresh config

    def save_settings(self) -> bool:
        """
        Saves the current configuration settings to the JSON file specified by self.config_file_path.

        Returns:
            bool: True if settings were successfully saved, False otherwise.
        """
        try:
            with open(self.config_file_path, 'w') as f:
                json.dump(self.config_data, f, indent=4)
            self.logger.info(f"Successfully saved configuration to {self.config_file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save configuration to {self.config_file_path}: {e}")
            return False

    # Potential future methods:
    # def remove_setting(self, key_path: str) -> bool:
    #     pass
    # def has_setting(self, key_path: str) -> bool:
    #     pass
