# C:\Users\m.2 SSD\Desktop\lastagent\dynamic_prompt_constructor.py
import logging

class DynamicPromptConstructor:
    """
    A module to dynamically construct and adapt prompts for LLMs,
    managing token limits by selectively including or summarizing components.
    """

    def __init__(self, logger: logging.Logger, tokenizer_func=None):
        """
        Initializes the DynamicPromptConstructor.

        Args:
            logger (logging.Logger): A logger instance for logging messages.
            tokenizer_func (callable, optional): A function that takes a string
                                                 and returns its token count.
                                                 If None, a simple character-based
                                                 estimation might be used as a fallback.
        """
        self.logger = logger
        self.tokenizer_func = tokenizer_func
        if self.tokenizer_func is None:
            self.logger.warning("No tokenizer_func provided. Prompt optimization will rely on character counts, which is inaccurate.")
        self.logger.info("DynamicPromptConstructor initialized.")

    def _estimate_tokens(self, text: str) -> int:
        """Estimates token count. Uses tokenizer_func if available, otherwise falls back to char count."""
        if self.tokenizer_func:
            try:
                return self.tokenizer_func(text)
            except Exception as e:
                self.logger.error(f"Error using provided tokenizer_func: {e}. Falling back to char count.")
                return len(text) // 4 # Rough estimate: 4 chars per token
        return len(text) // 4 # Rough estimate: 4 chars per token, highly inaccurate

    def build_and_optimize_prompt(self, components: dict, max_tokens: int, priority_order: list = None) -> str:
        """
        Constructs a prompt from various components and optimizes it to fit within max_tokens.

        This is a placeholder method. Actual implementation would involve:
        - Iteratively adding components based on priority.
        - Summarizing or truncating components if the total token count exceeds max_tokens.
        - More sophisticated strategies for deciding what to cut or shorten (e.g., keeping newest history).

        Args:
            components (dict): A dictionary of prompt components, e.g.,
                               {
                                   'system_message': "You are a helpful assistant.",
                                   'history': [
                                       {'role': 'user', 'content': 'Hello'},
                                       {'role': 'assistant', 'content': 'Hi there!'}
                                   ],
                                   'retrieved_knowledge': "Some relevant facts...",
                                   'user_query': "What is the weather like?",
                                   'task_instructions': "Provide a concise answer."
                               }
            max_tokens (int): The maximum number of tokens allowed for the final prompt.
            priority_order (list, optional): A list of keys from 'components' dict,
                                             specifying the order of importance.
                                             Components earlier in the list are prioritized.
                                             Default order: user_query, system_message, task_instructions, history, retrieved_knowledge.

        Returns:
            str: The final constructed and optimized prompt string.

        Example Usage:
            # constructor = DynamicPromptConstructor(my_logger, my_tokenizer_func)
            # prompt_parts = {
            #     'system_message': "You are an AI expert in Python.",
            #     'history': [{'role':'user', 'content':'Tell me about lists.'}],
            #     'user_query': "How do I reverse a list?"
            # }
            # final_prompt = constructor.build_and_optimize_prompt(prompt_parts, max_tokens=500)
            # # Use final_prompt with an LLM
        """
        self.logger.info(f"Attempting to build prompt with max_tokens: {max_tokens}")
        
        if priority_order is None:
            priority_order = ['user_query', 'system_message', 'task_instructions', 'history', 'retrieved_knowledge']

        final_prompt_elements = []
        current_tokens = 0
        
        processed_components = {}

        # Iterate through components by priority
        for key in priority_order:
            if key not in components or not components[key]:
                continue

            component_content = components[key]
            temp_prompt_str = ""

            if key == 'history' and isinstance(component_content, list):
                # Process history: add recent turns first until token limit for history is hit
                # This is a simplified history processing logic
                history_buffer = []
                for turn in reversed(component_content):
                    turn_str = f"{turn.get('role', 'unknown').capitalize()}: {str(turn.get('content', ''))}\n"
                    turn_tokens = self._estimate_tokens(turn_str)
                    if current_tokens + self._estimate_tokens("\n".join(history_buffer) + turn_str) <= max_tokens:
                        history_buffer.insert(0, turn_str) # Prepend to maintain order
                    else:
                        self.logger.info(f"History limit reached while adding turn: '{str(turn.get('content', ''))[:30]}...'")
                        break
                if history_buffer:
                    temp_prompt_str = "\n".join(history_buffer)
            elif isinstance(component_content, str):
                temp_prompt_str = component_content
            elif isinstance(component_content, list): # e.g. list of retrieved docs
                temp_prompt_str = "\n".join(map(str, component_content))
            else:
                temp_prompt_str = str(component_content)

            # Add formatting based on key (very basic)
            formatted_component_str = ""
            if key == 'system_message':
                formatted_component_str = temp_prompt_str
            elif key == 'user_query':
                formatted_component_str = f"User: {temp_prompt_str}"
            elif key == 'task_instructions':
                formatted_component_str = f"Instructions: {temp_prompt_str}"
            elif key == 'retrieved_knowledge':
                formatted_component_str = f"Context: {temp_prompt_str}"
            elif key == 'history': # Already formatted
                formatted_component_str = temp_prompt_str
            else: # Generic component
                 formatted_component_str = temp_prompt_str

            component_tokens = self._estimate_tokens(formatted_component_str + "\n") # Account for newline separator

            if current_tokens + component_tokens <= max_tokens:
                final_prompt_elements.append(formatted_component_str)
                current_tokens += component_tokens
                processed_components[key] = component_content
            else:
                self.logger.warning(f"Component '{key}' ('{str(component_content)[:50]}...') cannot fit fully. Tokens needed: {component_tokens}, remaining: {max_tokens - current_tokens}. Omitting or needs truncation/summarization strategy.")
                # Placeholder: In a real scenario, attempt to truncate/summarize this component if critical.
                # For now, if it doesn't fit, it's omitted (unless it's the first critical one).
                if not final_prompt_elements and (key == 'user_query' or key == 'system_message'): # Critical first component
                     # Attempt to truncate critical first component
                     available_chars_approx = (max_tokens - current_tokens) * 3
                     truncated_content = formatted_component_str[:available_chars_approx]
                     final_prompt_elements.append(truncated_content)
                     current_tokens += self._estimate_tokens(truncated_content + "\n")
                     self.logger.info(f"Critial component '{key}' truncated to fit.")
                break # Stop adding components if one doesn't fit (simplistic)

        final_prompt = "\n\n".join(final_prompt_elements).strip() # Use double newline for better separation
        
        final_tokens_estimate = self._estimate_tokens(final_prompt)
        self.logger.info(f"Final prompt constructed. Estimated tokens: {final_tokens_estimate}/{max_tokens}. Length: {len(final_prompt)} chars.")
        
        if final_tokens_estimate > max_tokens:
            self.logger.error(f"Constructed prompt ({final_tokens_estimate} tokens) STILL exceeds max_tokens ({max_tokens}) despite logic. This indicates an issue with estimation or placeholder logic.")
            # Fallback: Aggressively truncate the entire prompt (BAD for production)
            if self.tokenizer_func is None: # Character-based truncation
                 chars_to_keep = max_tokens * 3 # Very rough estimate for char count
                 if len(final_prompt) > chars_to_keep:
                     final_prompt = final_prompt[:chars_to_keep]
                     self.logger.warning(f"Forcefully truncated entire prompt to approx {chars_to_keep} chars.")
            # If tokenizer_func exists, a token-based truncation would be better here.

        return final_prompt

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger_main = logging.getLogger(__name__)

    # Dummy tokenizer for testing (counts words, very basic)
    def simple_word_tokenizer(text: str) -> int:
        return len(text.split())

    constructor_wt = DynamicPromptConstructor(logger_main, tokenizer_func=simple_word_tokenizer)

    logger_main.info("\n--- Test Case 1: Basic Prompt --- ")
    components1 = {
        'system_message': "You are a helpful AI assistant.",
        'user_query': "What is the current weather in London?"
    }
    prompt1 = constructor_wt.build_and_optimize_prompt(components1, max_tokens=20)
    logger_main.info(f"""Prompt 1 ({constructor_wt._estimate_tokens(prompt1)} tokens):\n{prompt1}""")
    assert constructor_wt._estimate_tokens(prompt1) <= 20

    logger_main.info("\n--- Test Case 2: With History and Knowledge, Token Limit --- ")
    components2 = {
        'system_message': "You are a knowledgeable historian.",
        'history': [
            {'role': 'user', 'content': 'Tell me about the Roman Empire.'},
            {'role': 'assistant', 'content': 'The Roman Empire was vast and influential, lasting for centuries.'}
        ],
        'retrieved_knowledge': "Key dates: Founding 753 BC, Fall of West 476 AD. Julius Caesar was a pivotal figure.",
        'user_query': "Who was Julius Caesar in relation to the Roman Empire? Provide details from the context.",
        'task_instructions': "Be concise and use the provided context."
    }
    # Max tokens set to force some components to be prioritized/omitted/truncated by a real implementation
    prompt2 = constructor_wt.build_and_optimize_prompt(components2, max_tokens=50) 
    logger_main.info(f"""Prompt 2 ({constructor_wt._estimate_tokens(prompt2)} tokens):\n{prompt2}""")
    assert "Julius Caesar" in prompt2 # User query should be there
    assert "historian" in prompt2 # System message likely there
    assert constructor_wt._estimate_tokens(prompt2) <= 50

    logger_main.info("\n--- Test Case 3: No Tokenizer (Fallback Character Estimation) --- ")
    constructor_no_tok = DynamicPromptConstructor(logger_main)
    components3 = {
        'system_message': "This is a system message that is quite long to test character based estimation and truncation if it happens to be necessary.",
        'user_query': "This is a shorter user query."
    }
    # max_tokens * 4 chars/token = 40 chars approx. System message is longer.
    prompt3 = constructor_no_tok.build_and_optimize_prompt(components3, max_tokens=15) 
    logger_main.info(f"""Prompt 3 (Est. tokens by chars: {constructor_no_tok._estimate_tokens(prompt3)}):\n{prompt3}""")
    # Check if the user query (higher priority after system message) is present
    assert "shorter user query" in prompt3 
    # The system message might be truncated or omitted by the placeholder logic.

    logger_main.info("\nExample tests completed.")
