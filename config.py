# C:\Users\m.2 SSD\Desktop\lastagent\agent006\config.py
"""
Configuration settings for agent006.
This would be an evolution of agent005's config,
with new settings for the adaptive modules.
"""
from pathlib import Path

SYS_CONF = {
    "agent_name": "Agent006-Adaptive",
    "version": "0.0.1", # This is the agent's internal version, distinct from agent_version_config
    "agent_version_config": "0.3.5-alpha-mono", # Internal version string for display/logging
    "agent_script_name_pattern": r"agent(?:(\d+)\.py|(\d+)\.[\w.-_]+\.py)$", # Regex to find version in filename

    "log_file_path": "C:\\Users\\m.2 SSD\\Desktop\\lastagent\\agent006\\agent006_ops.log",
    "state_file_path": "C:\\Users\\m.2 SSD\\Desktop\\lastagent\\agent006\\agent006_state.json",
    "project_root": str(Path(__file__).parent.parent.resolve()), # Points to C:\Users\m.2 SSD\Desktop\lastagent

    "gemini_api_key": "........add your key here .............", # CRITICAL: Replace with your actual key or load from env
    "gemini_model": "gemini-2.5-pro-exp-03-25", # Using the specified experimental model

    # New config options for agent006 might go here
    "max_operational_cycles": 100,
    "human_approval_required_for_code_execution": True,
}
