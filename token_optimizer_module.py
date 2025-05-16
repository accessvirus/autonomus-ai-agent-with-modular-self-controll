# token_optimizer_module.py

import logging

class TokenOptimizer:
    """
    A module to help manage and optimize text to fit within token limits
    of Large Language Models.
    """

    def __init__(self, logger: logging.Logger):
        """
        Initializes the TokenOptimizer.

        Args:
            logger (logging.Logger): A logger instance for logging messages.
        """
        self.logger = logger
        self.logger.info("TokenOptimizer initialized.")

    def estimate_token_count(self, text: str, tokenizer_model_name: str = "cl100k_base") -> int:
        """
        Estimates the token count for a given text using a specified tokenizer.
        This is a placeholder and would ideally use a library like tiktoken.

        Args:
            text (str): The input text.
            tokenizer_model_name (str): The name of the tokenizer model to use (e.g., for tiktoken).

        Returns:
            int: The estimated number of tokens.

        Example Usage:
            token_count = optimizer.estimate_token_count("This is a sample text.", "cl100k_base")
            logger.info(f"Estimated tokens: {token_count}")
        """
        self.logger.warning(
            "Placeholder estimate_token_count called. "
            "Actual implementation would use a tokenizer library (e.g., tiktoken)."
        )
        # A very rough approximation: average 4 characters per token.
        # This is NOT accurate and is for placeholder purposes only.
        # For a real implementation, use a library like tiktoken.
        # import tiktoken
        # encoding = tiktoken.get_encoding(tokenizer_model_name)
        # num_tokens = len(encoding.encode(text))
        # return num_tokens
        if not text:
            return 0
        estimated_tokens = (len(text) + 3) // 4 # Ensure rounding up for small strings
        self.logger.debug(f"Roughly estimated token count for '{text[:30]}...' is {estimated_tokens}")
        return estimated_tokens

    def chunk_text_by_tokens(self, text: str, max_tokens_per_chunk: int, tokenizer_model_name: str = "cl100k_base") -> list[str]:
        """
        Splits a large piece of text into smaller chunks, each aiming to be
        below a specified maximum token count.
        This is a placeholder method. A real implementation would require a proper
        tokenizer (like tiktoken for OpenAI models or a similar one for Gemini)
        to accurately count tokens and split the text, ideally on sentence or paragraph boundaries.

        Args:
            text (str): The text to be chunked.
            max_tokens_per_chunk (int): The maximum number of tokens allowed per chunk.
            tokenizer_model_name (str): The name of the tokenizer model to use (e.g., for tiktoken).

        Returns:
            list[str]: A list of text chunks.

        Example Usage:
            large_text = "Some very long text..."
            max_tokens = 500
            chunks = optimizer.chunk_text_by_tokens(large_text, max_tokens)
            for i, chunk in enumerate(chunks):
                logger.info(f"Chunk {i+1} (approx tokens: {optimizer.estimate_token_count(chunk)}): {chunk[:100]}...")
        """
        self.logger.info(
            f"Attempting to chunk text with max_tokens_per_chunk={max_tokens_per_chunk} "
            f"using placeholder logic for tokenizer '{tokenizer_model_name}'."
        )
        self.logger.warning(
            "Placeholder chunk_text_by_tokens called. "
            "Actual implementation needs a proper tokenizer and more sophisticated chunking logic "
            "(e.g., splitting by sentences or paragraphs, handling overlapping chunks if needed)."
        )

        chunks = []
        if not text.strip(): # Handle empty or whitespace-only text
            self.logger.info("Input text is empty, returning empty list of chunks.")
            return []

        # Placeholder logic: Split by words and use estimate_token_count.
        words = text.split()
        current_chunk_words = []
        current_estimated_tokens = 0

        for word in words:
            # Estimate tokens for the current word + a space (common for tokenizers)
            word_plus_space = word + " "
            word_tokens = self.estimate_token_count(word_plus_space, tokenizer_model_name)

            if current_estimated_tokens + word_tokens > max_tokens_per_chunk and current_chunk_words:
                chunks.append(" ".join(current_chunk_words))
                current_chunk_words = [word]
                current_estimated_tokens = self.estimate_token_count(word, tokenizer_model_name) # Re-estimate for the new first word
            else:
                current_chunk_words.append(word)
                current_estimated_tokens += word_tokens
                # Adjust for the last word not having a trailing space in the sum
                if len(current_chunk_words) > 1:
                     current_estimated_tokens = self.estimate_token_count(" ".join(current_chunk_words) + " ", tokenizer_model_name)
                else:
                     current_estimated_tokens = self.estimate_token_count(current_chunk_words[0], tokenizer_model_name)


        if current_chunk_words:
            chunks.append(" ".join(current_chunk_words))

        if not chunks and text: # If text was not empty but no chunks were made (e.g., text too small for loop logic)
             chunks.append(text)

        self.logger.info(f"Text split into {len(chunks)} chunks (placeholder method).")
        return chunks

    def get_module_info(self) -> dict:
        """
        Provides information about the module's capabilities.
        """
        return {
            "module_name": "TokenOptimizer",
            "description": "Provides utilities for managing and optimizing text for LLM token limits, such as token estimation and text chunking.",
            "methods": {
                "estimate_token_count": {
                    "description": "Estimates the token count for a given text. (Placeholder - uses rough character count)",
                    "parameters": {"text": "str", "tokenizer_model_name": "str (optional, e.g., 'cl100k_base')"},
                    "returns": "int (estimated token count)"
                },
                "chunk_text_by_tokens": {
                    "description": "Splits text into chunks based on a maximum token count. (Placeholder - uses rough word/char count based estimation)",
                    "parameters": {"text": "str", "max_tokens_per_chunk": "int", "tokenizer_model_name": "str (optional)"},
                    "returns": "list[str] (list of text chunks)"
                }
            }
        }

if __name__ == '__main__':
    # Example Usage (for testing the module directly)
    logger = logging.getLogger("TokenOptimizerTest")
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    optimizer = TokenOptimizer(logger)

    # Test get_module_info
    logger.info(f"Module Info: {optimizer.get_module_info()}")

    # Test estimate_token_count
    sample_text_short = "This is a test."
    tokens_short = optimizer.estimate_token_count(sample_text_short)
    logger.info(f"Estimated tokens for '{sample_text_short}': {tokens_short} (Expected: ~4-5)")

    empty_text_tokens = optimizer.estimate_token_count("")
    logger.info(f"Estimated tokens for empty string: {empty_text_tokens} (Expected: 0)")

    # Test chunk_text_by_tokens
    sample_text_long = (
        "This is a longer piece of text that is intended to be split into several chunks. "
        "Large language models often have input token limits, and it's crucial to "
        "manage these limits effectively. This module aims to provide tools for such management. "
        "By chunking text, we can process documents that would otherwise exceed the model's capacity. "
        "The accuracy of chunking depends heavily on the tokenizer used. This placeholder uses a very "
        "simple approach. A real implementation would integrate with libraries like tiktoken for OpenAI "
        "models or specific tokenizers for other models like Gemini or Claude. Proper handling of "
        "sentence boundaries and semantic meaning during chunking is also important for context preservation."
    )
    max_tokens_test = 20 # Set a small max_tokens for testing the chunking logic
    logger.info(f"\nOriginal long text (approx tokens: {optimizer.estimate_token_count(sample_text_long)}): \n{sample_text_long}")

    chunks = optimizer.chunk_text_by_tokens(sample_text_long, max_tokens_per_chunk=max_tokens_test)
    logger.info(f"\nText chunked into {len(chunks)} pieces (max_tokens_per_chunk={max_tokens_test}):")
    for i, chunk_item in enumerate(chunks):
        chunk_tokens = optimizer.estimate_token_count(chunk_item)
        logger.info(f"  Chunk {i+1} (approx tokens: {chunk_tokens}): '{chunk_item}'")
        if chunk_tokens > max_tokens_test:
            logger.error(f"    ERROR: Chunk {i+1} exceeds max_tokens_test! ({chunk_tokens} > {max_tokens_test})")

    # Test with text smaller than max_tokens
    small_text = "Short text, fits well."
    chunks_small = optimizer.chunk_text_by_tokens(small_text, max_tokens_per_chunk=max_tokens_test)
    logger.info(f"\nText chunked (small text, {len(chunks_small)} pieces):")
    for i, chunk_item in enumerate(chunks_small):
        chunk_tokens = optimizer.estimate_token_count(chunk_item)
        logger.info(f"  Chunk {i+1} (approx tokens: {chunk_tokens}): '{chunk_item}'")
        if chunk_tokens > max_tokens_test and len(small_text.split()) > 1: # only error if it was splittable
             logger.error(f"    ERROR: Chunk {i+1} exceeds max_tokens_test! ({chunk_tokens} > {max_tokens_test})")

    # Test with empty text
    empty_text = ""
    chunks_empty = optimizer.chunk_text_by_tokens(empty_text, max_tokens_per_chunk=max_tokens_test)
    logger.info(f"\nText chunked (empty text, {len(chunks_empty)} pieces):")
    if not chunks_empty:
        logger.info("  Result: [] (empty list as expected for empty input)")
    else:
        logger.warning(f"  Unexpected result for empty text: {chunks_empty}")

    # Test with text that might be tricky for token estimation
    tricky_text = "word word word word word word word word word word word word"
    # estimate_token_count("word ") = 2. 10 words * 2 = 20. 11th word makes it 22.
    # max_tokens = 20. Should split after 10 words.
    chunks_tricky = optimizer.chunk_text_by_tokens(tricky_text, max_tokens_per_chunk=10)
    logger.info(f"\nText chunked (tricky text, {len(chunks_tricky)} pieces, max_tokens=10):")
    for i, chunk_item in enumerate(chunks_tricky):
        chunk_tokens = optimizer.estimate_token_count(chunk_item)
        logger.info(f"  Chunk {i+1} (approx tokens: {chunk_tokens}): '{chunk_item}'")
