import logging
import json
import os # Added import for os module
from typing import Any, Dict, List, Optional, Tuple

class KnowledgeBaseManager:
    """
    Manages an in-memory knowledge base for the agent.
    Allows storing, retrieving, updating, and querying facts or pieces of information.
    This module aims to provide a structured way for the agent to manage its understanding
    of the world, tasks, and learned data.
    """

    def __init__(self, logger: logging.Logger, persistence_file: Optional[str] = None):
        """
        Initializes the KnowledgeBaseManager.

        Args:
            logger (logging.Logger): A logger instance for logging messages.
            persistence_file (Optional[str]): Path to a JSON file for persisting 
                                              and loading the knowledge base. 
                                              If None, knowledge is only in-memory.
        """
        self.logger = logger
        self._knowledge: Dict[str, Dict[str, Any]] = {}  # Category -> {Key: Value}
        self.persistence_file = persistence_file
        self.logger.info(f"KnowledgeBaseManager initialized. Persistence file: {persistence_file}")
        if self.persistence_file:
            self._load_knowledge()

    def store_fact(self, category: str, key: str, value: Any) -> bool:
        """
        Stores a fact (key-value pair) into a specified category in the knowledge base.
        If the category doesn't exist, it will be created.
        If the key already exists in the category, its value will be updated.

        Args:
            category (str): The category to store the fact under (e.g., 'environment', 'user_prefs').
            key (str): The key identifying the fact.
            value (Any): The value of the fact to be stored.

        Returns:
            bool: True if the fact was successfully stored/updated, False otherwise.
        
        Example Usage:
            # kb_manager = KnowledgeBaseManager(logger)
            # kb_manager.store_fact("user_preferences", "theme", "dark")
            # kb_manager.store_fact("environment_state", "current_location", "C:/Users/agent/work")
        """
        self.logger.debug(f"Attempting to store fact in category '{category}', key '{key}'.")
        if not isinstance(category, str) or not category.strip():
            self.logger.error("Category must be a non-empty string.")
            return False
        if not isinstance(key, str) or not key.strip():
            self.logger.error("Key must be a non-empty string.")
            return False

        if category not in self._knowledge:
            self._knowledge[category] = {}
        
        self._knowledge[category][key] = value
        self.logger.info(f"Stored/Updated fact in category '{category}', key '{key}'.")
        if self.persistence_file:
            self._save_knowledge() # Persist after each change for simplicity in placeholder
        return True

    def retrieve_fact(self, category: str, key: str, default: Optional[Any] = None) -> Optional[Any]:
        """
        Retrieves a fact by its category and key from the knowledge base.

        Args:
            category (str): The category of the fact.
            key (str): The key identifying the fact.
            default (Optional[Any]): The value to return if the fact is not found. Defaults to None.

        Returns:
            Optional[Any]: The value of the fact, or the default value if not found.

        Example Usage:
            # theme = kb_manager.retrieve_fact("user_preferences", "theme", "light")
            # location = kb_manager.retrieve_fact("environment_state", "current_location")
            # if location:
            #     print(f"Current location: {location}")
        """
        self.logger.debug(f"Attempting to retrieve fact from category '{category}', key '{key}'.")
        if category in self._knowledge and key in self._knowledge[category]:
            value = self._knowledge[category][key]
            self.logger.info(f"Retrieved fact from category '{category}', key '{key}'.")
            return value
        else:
            self.logger.info(f"Fact not found in category '{category}', key '{key}'. Returning default.")
            return default

    def query_knowledge(self, query_string: str, category_filter: Optional[str] = None) -> List[Tuple[str, str, Any]]:
        """
        (Placeholder) Queries the knowledge base based on a query string and optional category filter.
        This is a very basic placeholder. A real implementation would involve more sophisticated
        query parsing and matching logic (e.g., keyword search, semantic search if NLP integrated).

        Args:
            query_string (str): The search term or query.
            category_filter (Optional[str]): If provided, limits the search to this category.

        Returns:
            List[Tuple[str, str, Any]]: A list of matching facts, where each fact is a tuple 
                                         (category, key, value). Returns an empty list if no matches.
        
        Example Usage:
            # results = kb_manager.query_knowledge("API_KEY", category_filter="credentials")
            # for cat, k, v in results:
            #     print(f"Found in {cat}: {k} = {v}")
            # 
            # all_user_data = kb_manager.query_knowledge("user", category_filter="user_preferences")
        """
        self.logger.info(f"Placeholder: Querying knowledge with query: '{query_string}', category filter: {category_filter}")
        results: List[Tuple[str, str, Any]] = []
        
        # Placeholder logic: simple substring match in key or stringified value.
        search_term = query_string.lower()

        for category, facts in self._knowledge.items():
            if category_filter and category_filter != category:
                continue
            for key, value in facts.items():
                if search_term in key.lower() or (isinstance(value, str) and search_term in value.lower()):
                    results.append((category, key, value))
        
        if results:
            self.logger.info(f"Query found {len(results)} potential matches.")
        else:
            self.logger.info("Query found no matches.")
        return results

    def _save_knowledge(self) -> bool:
        """
        (Internal) Saves the current knowledge base to the persistence file if configured.
        """
        if not self.persistence_file:
            return False
        try:
            with open(self.persistence_file, 'w') as f:
                json.dump(self._knowledge, f, indent=4)
            self.logger.info(f"Knowledge base successfully saved to {self.persistence_file}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save knowledge base to {self.persistence_file}: {e}")
            return False

    def _load_knowledge(self) -> bool:
        """
        (Internal) Loads the knowledge base from the persistence file if configured and file exists.
        """
        if not self.persistence_file or not os.path.exists(self.persistence_file):
            self.logger.info(f"Persistence file {self.persistence_file} not found or not configured. Starting with empty knowledge base.")
            self._knowledge = {}
            return False
        try:
            with open(self.persistence_file, 'r') as f:
                self._knowledge = json.load(f)
            self.logger.info(f"Knowledge base successfully loaded from {self.persistence_file}")
            return True
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding JSON from {self.persistence_file}: {e}. Initializing empty knowledge base.")
            self._knowledge = {}
            return False
        except Exception as e:
            self.logger.error(f"Failed to load knowledge base from {self.persistence_file}: {e}. Initializing empty knowledge base.")
            self._knowledge = {}
            return False

    # Potential future methods:
    # def delete_fact(self, category: str, key: str) -> bool:
    #     pass
    # def list_categories(self) -> List[str]:
    #     pass
    # def list_facts_in_category(self, category: str) -> Dict[str, Any]:
    #     pass
