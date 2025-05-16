# C:\Users\m.2 SSD\Desktop\lastagent\agent006\SelfModificationSuite.py
"""
SelfModificationSuite (SMS) for agent006.

This module provides a robust and safer framework for the agent
to modify its own codebase and capabilities, including secure code
execution and version management.
"""
import sys
import subprocess
import os
import tempfile

class SelfModificationSuite:
    def __init__(self, logger):
        self.logger = logger
        self.logger.info("SelfModificationSuite initialized.")

    def execute_sandboxed_code(self, code_string: str, human_approval_required: bool = True) -> dict:
        self.logger.warning(f"SMS: Attempting to execute code. WARNING: Current execution is NOT TRULY SANDBOXED and carries security risks.")
        
        if human_approval_required:
            print(f"\n--- SMS: HUMAN APPROVAL REQUIRED FOR CODE EXECUTION ---")
            print("The agent proposes to execute the following Python code:")
            print("```python")
            print(code_string)
            print("```")
            approval = input("Approve execution? (yes/no): ").strip().lower()
            if approval != "yes":
                self.logger.info("SMS: Code execution denied by human.")
                return {"success": False, "error": "Execution denied by human."}

        tmp_file_path = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding='utf-8') as tmp_code_file:
                tmp_code_file.write(code_string)
                tmp_file_path = tmp_code_file.name
            
            # Use sys.executable to ensure it's the same Python interpreter
            command = [sys.executable, tmp_file_path]
            self.logger.info(f"SMS: Running command: {' '.join(command)}")
            process = subprocess.run(command, capture_output=True, text=True, timeout=60, encoding='utf-8')

            if process.returncode == 0:
                self.logger.info(f"SMS: Code execution success. Output:\n{process.stdout[:500]}")
                return {"success": True, "output": process.stdout, "stderr": process.stderr}
            else:
                error_output = f"Error (code {process.returncode}):\nStderr: {process.stderr}\nStdout: {process.stdout}"
                self.logger.error(f"SMS: Code execution error.\n{error_output}")
                return {"success": False, "error": error_output, "stdout": process.stdout, "stderr": process.stderr}
        except subprocess.TimeoutExpired:
            self.logger.error("SMS: Code execution timed out.")
            return {"success": False, "error": "Execution timed out."}
        except Exception as e:
            self.logger.error(f"SMS: Sandboxed code execution failed: {e}", exc_info=True)
            return {"success": False, "error": str(e)}
        finally:
            if tmp_file_path and os.path.exists(tmp_file_path):
                try:
                    os.remove(tmp_file_path)
                except Exception as e_del:
                    self.logger.warning(f"SMS: Failed to delete temp code file {tmp_file_path}: {e_del}")

    def apply_code_changes(self, file_path, new_code_content):
        self.logger.info(f"SMS: Applying code changes to {file_path}. CAUTION ADVISED.")
        # Placeholder for version control, testing, and safe application of changes
        try:
            with open(file_path, 'w') as f:
                f.write(new_code_content)
            return True
        except Exception as e:
            self.logger.error(f"SMS: Failed to apply code changes to {file_path}: {e}", exc_info=True)
            return False