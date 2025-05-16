# structured_memory_manager.py

import logging
import json
import os

class StructuredMemoryManager:
    """
    A module to provide more structured memory management capabilities for the agent,
    allowing for storage, retrieval, and searching of information with persistence.
    """

    def __init__(self, logger: logging.Logger, memory_file_path: str = "agent_memory.json"):
        """
        Initializes the StructuredMemoryManager.

        Args:
            logger (logging.Logger): A logger instance for logging messages.
            memory_file_path (str): Path to the file where memory will be persisted.
                                    If relative, it's typically relative to the agent's working directory.
                                    The module itself is in the project root, but its data files might be elsewhere.
                                    For simplicity, this example will place it in the current working directory.
        """
        self.logger = logger
        self.memory = {}
        # Construct absolute path for memory file if it's relative, assuming project root as base for data files for now.
        if not os.path.isabs(memory_file_path):
            # This assumes the agent's root directory is the intended base for data files.
            # If this module is part of a larger agent structure, this path might need adjustment
            # or be passed in as an absolute path by the agent's core.
            # For this self-contained example, we'll assume it's okay in CWD or a specified path.
            # Let's default to placing it in the same directory as this module for simplicity in this context.
            # However, the prompt's working directory is C:\Users\m.2 SSD\Desktop\lastagent
            # So, a relative path 'agent_memory.json' would resolve there.
            self.memory_file_path = os.path.join(os.path.dirname(__file__), memory_file_path) if '__file__' in globals() else memory_file_path
            # A safer default for an autonomous agent might be to place it in its designated working dir:
            # self.memory_file_path = os.path.join("C:\\Users\\m.2 SSD\\Desktop\\lastagent", memory_file_path)
        else:
            self.memory_file_path = memory_file_path

        self._load_memory_from_file()
        self.logger.info(f"StructuredMemoryManager initialized. Memory file target: {self.memory_file_path}")

    def _resolve_memory_file_path(self, relative_path: str) -> str:
        """Resolves the memory file path, defaulting to the agent's project root if relative."""
        if os.path.isabs(relative_path):
            return relative_path
        # Assuming the agent's project root is 'C:\Users\m.2 SSD\Desktop\lastagent'
        # This should ideally be passed in or configured globally for the agent.
        project_root = "C:\\Users\\m.2 SSD\\Desktop\\lastagent"
        return os.path.join(project_root, relative_path)

    def __init__(self, logger: logging.Logger, memory_file_name: str = "agent_persistent_memory.json"):
        self.logger = logger
        self.memory = {}
        # Ensure memory_file_path is absolute and in the project root directory.
        self.memory_file_path = self._resolve_memory_file_path(memory_file_name)
        self._load_memory_from_file()
        self.logger.info(f"StructuredMemoryManager initialized. Memory file: {self.memory_file_path}")

    def _load_memory_from_file(self):
        """
        Loads memory from a JSON file if it exists. This is a placeholder for robust error handling.
        """
        self.logger.debug(f"Attempting to load memory from {self.memory_file_path}")
        try:
            if os.path.exists(self.memory_file_path):
                with open(self.memory_file_path, 'r', encoding='utf-8') as f:
                    self.memory = json.load(f)
                self.logger.info(f"Memory loaded successfully from {self.memory_file_path}")
            else:
                self.logger.info(f"No existing memory file found at {self.memory_file_path}. Starting with empty memory.")
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding JSON from {self.memory_file_path}: {e}. Starting with empty memory.")
            self.memory = {}
        except Exception as e:
            self.logger.error(f"Error loading memory from {self.memory_file_path}: {e}. Starting with empty memory.")
            self.memory = {}

    def _save_memory_to_file(self):
        """
        Saves the current memory state to a JSON file. This is a placeholder for robust error handling.
        """
        self.logger.debug(f"Attempting to save memory to {self.memory_file_path}")
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.memory_file_path), exist_ok=True)
            with open(self.memory_file_path, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, indent=4)
            self.logger.info(f"Memory saved successfully to {self.memory_file_path}")
        except Exception as e:
            self.logger.error(f"Error saving memory to {self.memory_file_path}: {e}")

    def store_data(self, key: str, value: any) -> bool:
        """
        Stores a key-value pair in the structured memory.
        Overwrites the value if the key already exists. Value must be JSON serializable.

        Args:
            key (str): The key under which to store the data.
            value (any): The data to store (must be JSON serializable).

        Returns:
            bool: True if storage was successful, False otherwise.

        Example Usage:
            success = memory_manager.store_data("user_preference_theme", "dark_mode")
            if success:
                logger.info("Theme preference stored.")
        """
        self.logger.info(f"Storing data with key: '{key}'")
        if not isinstance(key, str) or not key.strip():
            self.logger.error("Key must be a non-empty string.")
            return False
        try:
            json.dumps(value) # Test serializability before modifying memory
            self.memory[key] = value
            self._save_memory_to_file()
            self.logger.debug(f"Data stored successfully for key '{key}'.")
            return True
        except TypeError as te:
            self.logger.error(f"Failed to store data for key '{key}': Value is not JSON serializable. Error: {te}")
            return False
        except Exception as e:
            self.logger.error(f"An unexpected error occurred while storing data for key '{key}': {e}")
            return False

    def retrieve_data(self, key: str) -> any:
        """
        Retrieves data from the structured memory using its key.

        Args:
            key (str): The key of the data to retrieve.

        Returns:
            any: The stored value, or None if the key is not found or key is invalid.

        Example Usage:
            theme = memory_manager.retrieve_data("user_preference_theme")
            if theme is not None:
                logger.info(f"User theme: {theme}")
        """
        self.logger.info(f"Retrieving data for key: '{key}'")
        if not isinstance(key, str):
            self.logger.warning("Key for retrieval must be a string. Returning None.")
            return None
        value = self.memory.get(key)
        if value is not None:
            self.logger.debug(f"Data retrieved for key '{key}'.")
        else:
            self.logger.debug(f"No data found for key '{key}'.")
        return value

    def search_memory_placeholder(self, query_term: str) -> dict:
        """
        Placeholder: A very basic search in memory keys and string values.
        This method demonstrates a potential capability. A real implementation would need
        more sophisticated indexing and search logic (e.g., full-text, semantic).

        Args:
            query_term (str): The term to search for (case-insensitive).

        Returns:
            dict: A dictionary of key-value pairs where the key or string value contains the query_term.

        Example Usage:
            search_results = memory_manager.search_memory_placeholder("task")
            for k, v in search_results.items():
                logger.info(f"Found match: {k} -> {v}")
        """
        self.logger.info(f"Executing placeholder search for term: '{query_term}'")
        self.logger.warning("search_memory_placeholder is a basic placeholder. For production, implement advanced search.")
        if not isinstance(query_term, str) or not query_term.strip():
            self.logger.warning("Search query term must be a non-empty string.")
            return {}
        
        results = {}
        qt_lower = query_term.lower()
        for key, value in self.memory.items():
            if qt_lower in key.lower():
                results[key] = value
            elif isinstance(value, str) and qt_lower in value.lower():
                results[key] = value
        self.logger.debug(f"Placeholder search found {len(results)} items for '{query_term}'.")
        return results

    def forget_data(self, key: str) -> bool:
        """
        Removes a key-value pair from the structured memory.

        Args:
            key (str): The key of the data to forget.

        Returns:
            bool: True if data was found and removed, False otherwise.
        """
        self.logger.info(f"Attempting to forget data for key: '{key}'")
        if not isinstance(key, str):
            self.logger.warning("Key for forgetting data must be a string. No action taken.")
            return False
        if key in self.memory:
            del self.memory[key]
            self._save_memory_to_file()
            self.logger.debug(f"Data for key '{key}' forgotten successfully.")
            return True
        else:
            self.logger.debug(f"No data found for key '{key}' to forget.")
            return False

    def get_all_keys(self) -> list[str]:
        """Returns a list of all keys currently stored in memory."""
        return list(self.memory.keys())

    def get_module_info(self) -> dict:
        """
        Provides information about the module's capabilities.
        """
        return {
            "module_name": "StructuredMemoryManager",
            "description": "Manages structured data (key-value pairs) for the agent, with JSON file persistence. Includes placeholder for advanced search.",
            "methods": {
                "store_data": {
                    "description": "Stores a JSON-serializable key-value pair and persists to file.",
                    "parameters": {"key": "str", "value": "any (JSON serializable)"},
                    "returns": "bool (True on success)"
                },
                "retrieve_data": {
                    "description": "Retrieves data by key.",
                    "parameters": {"key": "str"},
                    "returns": "any (stored value or None)"
                },
                "search_memory_placeholder": {
                    "description": "Placeholder: Basic case-insensitive search for a term in keys and string values.",
                    "parameters": {"query_term": "str"},
                    "returns": "dict (matching key-value pairs)"
                },
                "forget_data": {
                    "description": "Removes data by key and persists change.",
                    "parameters": {"key": "str"},
                    "returns": "bool (True if key existed and was removed)"
                },
                "get_all_keys": {
                    "description": "Returns a list of all keys in memory.",
                    "parameters": {},
                    "returns": "list[str]"
                }
            }
        }

if __name__ == '__main__':
    # This block is for direct testing of the module.
    # It assumes the module is in the project root: C:\Users\m.2 SSD\Desktop\lastagent
    # The memory file will also be created in/read from this root.
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    test_logger = logging.getLogger("StructuredMemoryManagerTest")

    # The memory file will be 'C:\Users\m.2 SSD\Desktop\lastagent\test_agent_memory.json'
    test_memory_filename = "test_agent_memory.json"
    manager = StructuredMemoryManager(test_logger, memory_file_name=test_memory_filename)

    test_logger.info(f"Module Info: {json.dumps(manager.get_module_info(), indent=2)}")

    # Clean up any previous test file
    if os.path.exists(manager.memory_file_path):
        os.remove(manager.memory_file_path)
        test_logger.info(f"Removed old test memory file: {manager.memory_file_path}")
    manager = StructuredMemoryManager(test_logger, memory_file_name=test_memory_filename) # Re-initialize after delete

    # Test store and retrieve
    manager.store_data("agent_name", "Agent006")
    manager.store_data("agent_version", 0.2)
    manager.store_data("active_goals", ["enhance_capabilities", "monitor_system"])
    test_logger.info(f"Agent Name: {manager.retrieve_data('agent_name')}")
    test_logger.info(f"Agent Version: {manager.retrieve_data('agent_version')}")
    test_logger.info(f"Active Goals: {manager.retrieve_data('active_goals')}")
    test_logger.info(f"Non-existent key 'status': {manager.retrieve_data('status')}")

    # Test search (placeholder)
    test_logger.info(f"Search for 'agent': {manager.search_memory_placeholder('agent')}")
    test_logger.info(f"Search for 'system': {manager.search_memory_placeholder('system')}") # Should find in 'active_goals' if it were string

    # Test forget
    manager.forget_data("agent_version")
    test_logger.info(f"Agent Version after forget: {manager.retrieve_data('agent_version')}")
    test_logger.info(f"All keys: {manager.get_all_keys()}")

    # Test persistence
    test_logger.info("--- Testing Persistence ---")
    del manager
    manager_reloaded = StructuredMemoryManager(test_logger, memory_file_name=test_memory_filename)
    test_logger.info(f"Reloaded Agent Name: {manager_reloaded.retrieve_data('agent_name')}")
    test_logger.info(f"Reloaded Active Goals: {manager_reloaded.retrieve_data('active_goals')}")
    test_logger.info(f"All keys after reload: {manager_reloaded.get_all_keys()}")

    # Clean up test file
    if os.path.exists(manager_reloaded.memory_file_path):
        os.remove(manager_reloaded.memory_file_path)
        test_logger.info(f"Cleaned up test memory file: {manager_reloaded.memory_file_path}")

    test_logger.info("StructuredMemoryManager test complete.")
