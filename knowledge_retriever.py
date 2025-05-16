# C:\Users\m.2 SSD\Desktop\lastagent\knowledge_retriever.py
import logging
import json
import os

class KnowledgeRetriever:
    """
    A module for storing and retrieving knowledge or information.
    Initially, this will use a simple file-based storage (JSON).
    """

    def __init__(self, logger: logging.Logger, knowledge_file_path: str = "knowledge_base.json"):
        """
        Initializes the KnowledgeRetriever.

        Args:
            logger (logging.Logger): A logger instance for logging messages.
            knowledge_file_path (str): Path to the JSON file used as the knowledge base.
                                       Defaults to 'knowledge_base.json' in the project root if relative,
                                       or uses the absolute path if provided.
        """
        self.logger = logger
        self.project_root = r"C:\Users\m.2 SSD\Desktop\lastagent" # Agent's working directory
        
        if os.path.isabs(knowledge_file_path):
            self.knowledge_file = knowledge_file_path
        else:
            self.knowledge_file = os.path.join(self.project_root, knowledge_file_path)

        self.knowledge_base = self._load_knowledge()
        self.logger.info(f"KnowledgeRetriever initialized. Knowledge base file: {self.knowledge_file}")

    def _load_knowledge(self) -> dict:
        """
        Loads the knowledge base from the JSON file.
        If the file doesn't exist, it returns an empty dictionary.
        """
        try:
            if os.path.exists(self.knowledge_file):
                with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.logger.info(f"Knowledge base loaded successfully from {self.knowledge_file}")
                    return data
            else:
                self.logger.info(f"Knowledge base file {self.knowledge_file} not found. Starting with an empty base.")
                return {}
        except json.JSONDecodeError:
            self.logger.error(f"Error decoding JSON from {self.knowledge_file}. Starting with an empty base.")
            return {}
        except Exception as e:
            self.logger.error(f"Failed to load knowledge base from {self.knowledge_file}: {e}. Starting with an empty base.")
            return {}

    def _save_knowledge(self):
        """
        Saves the current knowledge base to the JSON file.
        """
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.knowledge_file), exist_ok=True)
            with open(self.knowledge_file, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_base, f, indent=4, ensure_ascii=False)
            self.logger.info(f"Knowledge base saved successfully to {self.knowledge_file}")
        except Exception as e:
            self.logger.error(f"Failed to save knowledge base to {self.knowledge_file}: {e}")

    def store_fact(self, key: str, value: any, category: str = "general") -> bool:
        """
        Stores a piece of information (a fact) in the knowledge base.
        Facts are stored under categories, and then by key.

        Args:
            key (str): The unique identifier for the fact within its category.
            value (any): The information to store. Can be any JSON-serializable type.
            category (str): An optional category for the fact. Defaults to "general".

        Returns:
            bool: True if storage was successful (or if data was unchanged), False otherwise (currently always True on attempt).

        Example Usage:
            # kr = KnowledgeRetriever(my_logger)
            # kr.store_fact("capital_of_france", "Paris", category="geography")
            # kr.store_fact("llm_model_used", "Gemini-Pro", category="agent_config")
        """
        self.logger.info(f"Attempting to store fact: category='{category}', key='{key}'")
        if category not in self.knowledge_base:
            self.knowledge_base[category] = {}
        
        if key in self.knowledge_base[category] and self.knowledge_base[category][key] == value:
            self.logger.info(f"Fact with key='{key}' and same value already exists in category='{category}'. No update needed.")
            return True

        self.knowledge_base[category][key] = value
        self._save_knowledge() # Consider if save errors should make this return False
        self.logger.info(f"Fact stored/updated: category='{category}', key='{key}'")
        return True

    def retrieve_fact(self, key: str, category: str = "general") -> any:
        """
        Retrieves a piece of information from the knowledge base by category and key.

        Args:
            key (str): The key of the fact to retrieve.
            category (str): The category of the fact. Defaults to "general".

        Returns:
            any: The stored value if found, otherwise None.

        Example Usage:
            # capital = kr.retrieve_fact("capital_of_france", category="geography")
            # if capital:
            #     print(f"The capital of France is {capital}.")
        """
        self.logger.info(f"Attempting to retrieve fact: category='{category}', key='{key}'")
        if category in self.knowledge_base and key in self.knowledge_base[category]:
            value = self.knowledge_base[category][key]
            # Avoid logging potentially large values directly
            value_preview = str(value)[:100] + ('...' if len(str(value)) > 100 else '')
            self.logger.info(f"Fact retrieved: category='{category}', key='{key}', value_preview='{value_preview}'")
            return value
        else:
            self.logger.warning(f"Fact not found: category='{category}', key='{key}'")
            return None

    def search_knowledge(self, query_term: str, search_in_keys: bool = True, search_in_values: bool = True, top_k: int = 5) -> list:
        """
        Performs a basic case-insensitive search for a term within keys and/or string values in the knowledge base.
        (Placeholder for more advanced search functionality like semantic search or full-text indexing).

        Args:
            query_term (str): The term to search for.
            search_in_keys (bool): Whether to search in the keys of the facts.
            search_in_values (bool): Whether to search in the string values of the facts.
            top_k (int): The maximum number of results to return.

        Returns:
            list: A list of matching entries, where each entry is a dict 
                  {'category': str, 'key': str, 'value': any}.

        Example Usage:
            # results = kr.search_knowledge("Paris")
            # config_settings = kr.search_knowledge("model", search_in_values=False)
        """
        self.logger.info(f"Performing naive search for term: '{query_term}', top_k={top_k}")
        results = []
        query_lower = query_term.lower()

        for category, items in self.knowledge_base.items():
            for key, value in items.items():
                found = False
                if search_in_keys and query_lower in key.lower():
                    found = True
                if not found and search_in_values and isinstance(value, str) and query_lower in value.lower():
                    found = True
                
                if found:
                    results.append({"category": category, "key": key, "value": value})
                    if len(results) >= top_k:
                        break
            if len(results) >= top_k:
                break
        
        if not results:
            self.logger.info(f"No results found for term: '{query_term}' with current naive search settings.")
        else:
            self.logger.info(f"Found {len(results)} results for term: '{query_term}'")
        return results

if __name__ == '__main__':
    # Example usage (for testing purposes when run directly)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main_logger = logging.getLogger(__name__)

    # Use a temporary file for testing
    test_kb_filename = "temp_test_knowledge_base.json"
    # Ensure project root is correct for test file creation if KnowledgeRetriever uses it
    # For this direct test, we can place it in the current directory.
    if os.path.exists(test_kb_filename):
        os.remove(test_kb_filename)

    retriever = KnowledgeRetriever(main_logger, knowledge_file_path=test_kb_filename)

    main_logger.info("\n--- Test Case: Store and Retrieve Facts ---")
    retriever.store_fact("agent_version", "1.0.2", category="system_info")
    retriever.store_fact("last_error", "None", category="runtime_stats")
    retriever.store_fact("api_endpoint_status", {"gemini": "operational", "weather_api": "degraded"}, category="external_services")

    version = retriever.retrieve_fact("agent_version", category="system_info")
    main_logger.info(f"Retrieved agent_version: {version}")
    assert version == "1.0.2"

    status = retriever.retrieve_fact("api_endpoint_status", category="external_services")
    main_logger.info(f"Retrieved api_endpoint_status: {status}")
    assert status["weather_api"] == "degraded"

    non_existent = retriever.retrieve_fact("unknown_key", category="system_info")
    assert non_existent is None

    main_logger.info("\n--- Test Case: Search Knowledge ---")
    retriever.store_fact("user_preference_language", "English", category="user_settings")
    retriever.store_fact("system_language", "English (US)", category="system_info")

    search_results_lang = retriever.search_knowledge("language")
    main_logger.info(f"Search for 'language': {search_results_lang}")
    assert len(search_results_lang) >= 2 # Should find in keys

    search_results_english = retriever.search_knowledge("English")
    main_logger.info(f"Search for 'English': {search_results_english}")
    assert len(search_results_english) >= 2 # Should find in values
    
    search_results_system_key = retriever.search_knowledge("system", search_in_values=False)
    main_logger.info(f"Search for 'system' in keys only: {search_results_system_key}")
    assert len(search_results_system_key) == 2 # system_info, system_language

    main_logger.info("\n--- Test Case: File Persistence ---")
    del retriever # Delete instance to ensure data is saved
    retriever_reloaded = KnowledgeRetriever(main_logger, knowledge_file_path=test_kb_filename)
    reloaded_version = retriever_reloaded.retrieve_fact("agent_version", category="system_info")
    main_logger.info(f"Reloaded agent_version: {reloaded_version}")
    assert reloaded_version == "1.0.2"

    main_logger.info("\nExample tests completed.")

    # Clean up the test file
    if os.path.exists(test_kb_filename):
        os.remove(test_kb_filename)
