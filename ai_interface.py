# C:\Users\m.2 SSD\Desktop\lastagent\agent006\ai_interface.py
"""
Handles all interactions with the external Generative AI service (e.g., Gemini).
This would be similar to agent005's version but might be enhanced
to work with richer context from AdvancedMemorySystem.
"""
import google.generativeai as genai
import time
from typing import Optional, List

class GenerativeAIServiceInterface:
    def __init__(self, config, logger, operational_log_buffer: List[str]):
        self.config = config
        self.logger = logger
        self.operational_log_buffer = operational_log_buffer # For including in prompts
        self.api_key = self.config.get("gemini_api_key")
        self.model_name = self.config.get("gemini_model") # Corrected key

        if not self.api_key or self.api_key == "YOUR_GEMINI_API_KEY_HERE":
            self.logger.critical("AI Interface: GEMINI_API_KEY is not set or is a placeholder in config.py.")
            raise ValueError("GEMINI_API_KEY is required for GenerativeAIServiceInterface.")

        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
            self.logger.info(f"GenerativeAIServiceInterface initialized with model: {self.model_name}")
        except Exception as e:
            self.logger.critical(f"AI Interface: Failed to initialize Gemini Model ({self.model_name}): {e}", exc_info=True)
            raise

    def generate_text(self, prompt: str, temperature: float = 0.5, max_retries: int = 3) -> Optional[str]:
        """Generates text using the Gemini model, with retry logic."""
        self.logger.debug(f"AI Interface: Sending prompt to Gemini (first 200 chars): {prompt[:200]}...")
        print(f"\n--- PROMPT TO GEMINI (AI_INTERFACE) ---\n{prompt}\n--- END PROMPT ---") # For debugging

        current_retry = 0
        while current_retry < max_retries:
            try:
                response = self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=temperature
                    )
                )
                generated_text = ""
                if response.parts:
                    text_parts = [part.text for part in response.parts if hasattr(part, 'text')]
                    if text_parts:
                        generated_text = "".join(text_parts)
                elif hasattr(response, 'text') and response.text:
                    generated_text = response.text

                if generated_text:
                    self.logger.debug(f"AI Interface: Gemini response received (first 200 chars): {generated_text[:200]}...")
                    print(f"\n--- RESPONSE FROM GEMINI (AI_INTERFACE) ---\n{generated_text}\n--- END RESPONSE ---") # For debugging
                    return generated_text.strip()

                block_reason_message = "Unknown reason for empty response."
                if response.prompt_feedback and response.prompt_feedback.block_reason:
                    block_reason_message = response.prompt_feedback.block_reason_message or str(response.prompt_feedback.block_reason)
                    self.logger.error(f"AI Interface: Gemini prompt blocked. Reason: {block_reason_message}")
                    return f"ERROR: Prompt blocked by API. Reason: {block_reason_message}"

                self.logger.warning(f"AI Interface: Gemini response was empty. {block_reason_message}. Retrying ({current_retry + 1}/{max_retries})...")
                time.sleep(2 ** (current_retry + 1)) # Exponential backoff
                current_retry += 1
                continue

            except Exception as e:
                current_retry += 1
                self.logger.error(f"AI Interface: Error calling Gemini API (Attempt {current_retry}/{max_retries}): {e}", exc_info=True)
                if current_retry >= max_retries:
                    self.logger.error("AI Interface: Max retries reached for Gemini API call.")
                    return f"ERROR: Max retries reached for Gemini API call: {e}"
                time.sleep(3 * current_retry) # Exponential backoff
        self.logger.info("GenerativeAIServiceInterface (agent006) initialized.")