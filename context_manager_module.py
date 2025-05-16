# context_manager_module.py

import logging
import json # Needed for __main__ example
# import tiktoken # Would be used in a real implementation for accurate token counting

class ContextManager:
    """
    Manages a conversation context (history) to ensure it stays within
    specified token limits for LLMs, by implementing pruning strategies.
    """

    def __init__(self, logger: logging.Logger, max_tokens: int, tokenizer_name: str = "cl100k_base"):
        """
        Initializes the ContextManager.

        Args:
            logger (logging.Logger): Logger instance.
            max_tokens (int): The maximum number of tokens allowed for the context.
            tokenizer_name (str): Name of the tokenizer model (e.g., for tiktoken).
                                  Used for estimating token counts.
        """
        self.logger = logger
        self.max_tokens = max_tokens
        self.tokenizer_name = tokenizer_name
        self.context_history = []  # List of messages, e.g., {"role": "user", "content": "...", "tokens": N}
        self.current_total_tokens = 0
        # In a real scenario, initialize the tokenizer here. Example:
        # try:
        #     self.tokenizer = tiktoken.get_encoding(tokenizer_name)
        # except Exception as e:
        #     self.logger.error(f"Failed to load tokenizer '{tokenizer_name}': {e}. Using rough estimation.")
        #     self.tokenizer = None
        self.logger.info(f"ContextManager initialized with max_tokens={max_tokens}. Tokenizer: '{tokenizer_name}' (placeholder)." )

    def _estimate_tokens(self, text: str) -> int:
        """
        Placeholder for token estimation.
        A real implementation would use a library like tiktoken for the specific LLM.
        """
        if not text:
            return 0
        # if self.tokenizer:
        #     return len(self.tokenizer.encode(text))
        # Rough estimation: 1 token ~ 4 chars. This is highly inaccurate and model-dependent.
        estimated = (len(text) + 3) // 4
        self.logger.debug(f"Roughly estimated {estimated} tokens for text: '{text[:50]}...'" )
        return estimated

    def add_message(self, role: str, content: str):
        """
        Adds a message to the context history and prunes if necessary.

        Args:
            role (str): The role of the message sender (e.g., "user", "assistant", "system").
            content (str): The content of the message.

        Example Usage:
            context_manager.add_message("user", "What is the weather like?")
            context_manager.add_message("assistant", "It's sunny today!")
        """
        message_tokens = self._estimate_tokens(content)
        self.logger.debug(f"Attempting to add message: role='{role}', content_length={len(content)}, estimated_tokens={message_tokens}")

        # Prune context if adding this message would exceed max_tokens
        self.prune_context_if_needed(additional_tokens_to_add=message_tokens)

        if self.current_total_tokens + message_tokens <= self.max_tokens:
            message = {"role": role, "content": content, "tokens": message_tokens}
            self.context_history.append(message)
            self.current_total_tokens += message_tokens
            self.logger.info(f"Added message from '{role}'. New total tokens: {self.current_total_tokens}")
        else:
            self.logger.warning(
                f"Could not add message from '{role}' (tokens: {message_tokens}). "
                f"Current tokens after pruning: {self.current_total_tokens}, Max tokens: {self.max_tokens}. "
                f"The message itself might be too large for the remaining space or entire context limit."
            )

    def prune_context_if_needed(self, additional_tokens_to_add: int = 0) -> bool:
        """
        Placeholder: Prunes the context history if the total token count
        (including any `additional_tokens_to_add`) exceeds `max_tokens`.
        Current placeholder strategy: Remove oldest messages.
        More advanced strategies could protect system messages or summarize.

        Args:
            additional_tokens_to_add (int): Estimated tokens of a new message about to be added.

        Returns:
            bool: True if pruning was performed, False otherwise.
        """
        pruned = False
        self.logger.debug(
            f"Checking pruning: Current tokens={self.current_total_tokens}, "
            f"Additional to add={additional_tokens_to_add}, Target max tokens={self.max_tokens}"
        )

        while (self.current_total_tokens + additional_tokens_to_add > self.max_tokens) and self.context_history:
            # Basic strategy: remove the oldest message.
            # A more advanced strategy might preserve initial system messages,
            # or summarize older messages, or use a sliding window with summarization.
            removed_message = self.context_history.pop(0)
            self.current_total_tokens -= removed_message["tokens"]
            pruned = True
            self.logger.info(
                f"Pruned oldest message (role: {removed_message['role']}, tokens: {removed_message['tokens']}) "
                f"to make space. New total tokens: {self.current_total_tokens}"
            )
            
        if pruned:
            self.logger.info(f"Context pruned. Current total tokens after pruning: {self.current_total_tokens}")
        return pruned

    def get_context(self) -> list[dict]:
        """
        Returns the current context history, typically for sending to an LLM.
        Each item is a dict like {"role": "user", "content": "..."}.
        """
        return [{"role": msg["role"], "content": msg["content"]} for msg in self.context_history]

    def get_current_token_count(self) -> int:
        """Returns the current total token count of the context history."""
        return self.current_total_tokens

    def clear_context(self):
        """Clears the entire context history."""
        self.context_history = []
        self.current_total_tokens = 0
        self.logger.info("Context history cleared.")

    def get_module_info(self) -> dict:
        """Provides information about the module's capabilities."""
        return {
            "module_name": "ContextManager",
            "description": "Manages conversation context for LLMs, ensuring it stays within token limits using pruning strategies. Uses placeholder token estimation.",
            "methods": {
                "add_message": {
                    "description": "Adds a message (role, content) to context, prunes if needed.",
                    "parameters": {"role": "str", "content": "str"},
                    "returns": "None"
                },
                "prune_context_if_needed": {
                    "description": "Placeholder: Prunes context if total tokens exceed max_tokens. Removes oldest messages.",
                    "parameters": {"additional_tokens_to_add": "int (optional, default 0)"},
                    "returns": "bool (True if pruned)"
                },
                "get_context": {
                    "description": "Returns the list of messages formatted for an LLM.",
                    "parameters": {},
                    "returns": "list[dict]"
                },
                "get_current_token_count": {
                    "description": "Returns the current total estimated tokens in the context.",
                    "parameters": {},
                    "returns": "int"
                },
                "clear_context": {
                    "description": "Clears all messages from the context.",
                    "parameters": {},
                    "returns": "None"
                }
            }
        }

if __name__ == '__main__':
    # Example Usage for direct testing of the module
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    test_logger = logging.getLogger("ContextManagerTest")

    manager = ContextManager(test_logger, max_tokens=10) # Low token limit for easy testing
    test_logger.info(f"Module Info: {json.dumps(manager.get_module_info(), indent=2)}")

    manager.add_message("user", "Hello")      # Est. 2 tokens (len 5)
    test_logger.info(f"Context: {manager.get_context()}, Tokens: {manager.get_current_token_count()}")

    manager.add_message("assistant", "World")  # Est. 2 tokens (len 5). Total: 4
    test_logger.info(f"Context: {manager.get_context()}, Tokens: {manager.get_current_token_count()}")

    manager.add_message("user", "This is a test") # Est. 4 tokens (len 14). Total: 8
    test_logger.info(f"Context: {manager.get_context()}, Tokens: {manager.get_current_token_count()}")

    test_logger.info("--- Adding message that should trigger pruning (current 8, adding 3, max 10) ---")
    manager.add_message("assistant", "Another one") # Est. 3 tokens (len 11). Current 8 + 3 = 11 > 10.
                                                 # Prunes "Hello" (-2). Context becomes 6. Then 6 + 3 = 9.
    test_logger.info(f"Context: {manager.get_context()}, Tokens: {manager.get_current_token_count()}")
    # Expected context: [World, This is a test, Another one], Tokens: 2+4+3 = 9

    test_logger.info("--- Adding another message that should trigger more pruning (current 9, adding 4, max 10) ---")
    manager.add_message("user", "Final message") # Est. 4 tokens (len 13). Current 9 + 4 = 13 > 10.
                                              # Prunes "World" (-2). Context becomes 7. 7 + 4 = 11 > 10.
                                              # Prunes "This is a test" (-4). Context becomes 3. Then 3 + 4 = 7.
    test_logger.info(f"Context: {manager.get_context()}, Tokens: {manager.get_current_token_count()}")
    # Expected context: [Another one, Final message], Tokens: 3+4 = 7

    test_logger.info("--- Testing adding a message too large for an empty context ---")
    manager.clear_context()
    manager.add_message("user", "This single message is far too long for the tiny context limit of ten tokens") # Est. 18 tokens (len 71)
    test_logger.info(f"Context: {manager.get_context()}, Tokens: {manager.get_current_token_count()}")
    # Expected: Empty context, warning logged, tokens 0.

    test_logger.info("--- Testing with a system message (current pruning doesn't specifically protect it) ---")
    manager.clear_context()
    manager.add_message("system", "You are helpful.") # Est. 4 tokens (len 16)
    manager.add_message("user", "Hi")               # Est. 1 token (len 2). Total 5
    manager.add_message("assistant", "Hello there")  # Est. 3 tokens (len 11). Total 8
    manager.add_message("user", "Question")         # Est. 2 tokens (len 8). Total 10.
    test_logger.info(f"Context before next prune: {manager.get_context()}, Tokens: {manager.get_current_token_count()}")
    
    manager.add_message("assistant", "Answer is long") # Est. 4 tokens (len 14). Current 10 + 4 = 14 > 10.
                                                 # Prunes "You are helpful." (-4). Context 6. Then 6 + 4 = 10.
    test_logger.info(f"Context after 'Answer is long': {manager.get_context()}, Tokens: {manager.get_current_token_count()}")
    # Expected: [Hi, Hello there, Question, Answer is long], Tokens: 1+3+2+4 = 10

    test_logger.info("ContextManager test complete.")
