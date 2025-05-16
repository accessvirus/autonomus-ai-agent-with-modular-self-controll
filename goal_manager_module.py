# goal_manager_module.py

import logging
import uuid # For generating unique goal IDs
from enum import Enum
from typing import List, Dict, Optional, Any
import json # For example usage in __main__

class GoalStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"

class GoalManager:
    """
    Manages a list of goals, their priorities, dependencies, and status.
    Helps the agent decide which goal to pursue next.
    """

    def __init__(self, logger: logging.Logger):
        """
        Initializes the GoalManager.

        Args:
            logger (logging.Logger): A logger instance for logging messages.
        """
        self.logger = logger
        self.goals: Dict[str, Dict[str, Any]] = {} # goal_id: {description, priority, status, dependencies, notes, sub_tasks}
        self.logger.info("GoalManager initialized.")

    def add_goal(self, description: str, priority: int = 0, goal_id: Optional[str] = None,
                 dependencies: Optional[List[str]] = None, notes: Optional[str] = None) -> str:
        """
        Adds a new goal to the manager.

        Args:
            description (str): A clear description of the goal.
            priority (int, optional): Priority of the goal (higher value means higher priority). Defaults to 0.
            goal_id (Optional[str], optional): A specific ID for the goal. If None, a UUID is generated. Defaults to None.
            dependencies (Optional[List[str]], optional): A list of goal IDs that this goal depends on. Defaults to None.
            notes (Optional[str], optional): Any additional notes for the goal. Defaults to None.

        Returns:
            str: The ID of the added goal.
        """
        if not description:
            self.logger.error("Goal description cannot be empty.")
            raise ValueError("Goal description cannot be empty.")

        new_goal_id = goal_id if goal_id else str(uuid.uuid4())
        if new_goal_id in self.goals:
            self.logger.warning(f"Goal ID {new_goal_id} already exists. Goal not added.")
            # Depending on desired behavior, could raise error or update existing goal
            return new_goal_id

        self.goals[new_goal_id] = {
            "description": description,
            "priority": priority,
            "status": GoalStatus.PENDING.value,
            "dependencies": dependencies if dependencies else [],
            "notes": notes if notes else "",
            "sub_tasks": [] # Placeholder for potential sub-tasks from a task planner
        }
        self.logger.info(f"Added new goal: ID='{new_goal_id}', Description='{description}', Priority={priority}")
        return new_goal_id

    def get_goal(self, goal_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a goal by its ID.

        Args:
            goal_id (str): The ID of the goal to retrieve.

        Returns:
            Optional[Dict[str, Any]]: The goal dictionary (including its ID) if found, else None.
        """
        goal_data = self.goals.get(goal_id)
        if not goal_data:
            self.logger.warning(f"Goal with ID '{goal_id}' not found.")
            return None
        return {"id": goal_id, **goal_data} # Include the ID in the returned dict

    def update_goal_status(self, goal_id: str, status: GoalStatus, notes: Optional[str] = None) -> bool:
        """
        Updates the status of an existing goal.

        Args:
            goal_id (str): The ID of the goal to update.
            status (GoalStatus): The new status for the goal.
            notes (Optional[str], optional): Additional notes for this status update. Defaults to None.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        if goal_id not in self.goals:
            self.logger.error(f"Cannot update status for non-existent goal ID: {goal_id}")
            return False
        
        if not isinstance(status, GoalStatus):
            self.logger.error(f"Invalid status type: {type(status)}. Must be GoalStatus enum.")
            return False

        self.goals[goal_id]["status"] = status.value
        if notes:
            current_notes = self.goals[goal_id].get("notes", "")
            self.goals[goal_id]["notes"] = (current_notes + f"\nStatus Update ({status.value}): {notes}").strip()
            
        self.logger.info(f"Updated goal '{goal_id}' status to {status.value}.")
        return True

    def list_goals(self, status_filter: Optional[GoalStatus] = None) -> List[Dict[str, Any]]:
        """
        Lists all goals, optionally filtered by status.

        Args:
            status_filter (Optional[GoalStatus], optional): Filter goals by this status. Defaults to None (all goals).

        Returns:
            List[Dict[str, Any]]: A list of goal dictionaries, each including its ID.
        """
        all_goals_with_ids = [{ "id": gid, **gdata} for gid, gdata in self.goals.items()]
        if status_filter:
            if not isinstance(status_filter, GoalStatus):
                self.logger.warning(f"Invalid status_filter: {status_filter}. Returning all goals.")
                return all_goals_with_ids
            return [goal for goal in all_goals_with_ids if goal["status"] == status_filter.value]
        return all_goals_with_ids

    def get_next_goal_placeholder(self) -> Optional[Dict[str, Any]]:
        """
        Placeholder: Selects the next goal to pursue based on a simple strategy.
        A real implementation would consider priorities, dependencies, resource availability, etc.
        This placeholder will simply pick the first PENDING goal with the highest priority
        whose dependencies (if any) are met (COMPLETED).

        Returns:
            Optional[Dict[str, Any]]: The next goal dictionary (including ID) to work on, or None if no suitable goal is found.
        
        Example Usage:
            # goal_manager = GoalManager(logger)
            # # ... add goals ...
            # next_actionable_goal = goal_manager.get_next_goal_placeholder()
            # if next_actionable_goal:
            #     logger.info(f"Next goal to pursue: {next_actionable_goal['description']}")
            # else:
            #     logger.info("No actionable goals at the moment.")
        """
        self.logger.info("Attempting to select next goal (placeholder logic).")
        self.logger.warning(
            "Placeholder get_next_goal_placeholder called. "
            "Actual implementation would involve more sophisticated prioritization and dependency checking."
        )

        actionable_goals = []
        for goal_id, goal_data in self.goals.items():
            if goal_data["status"] == GoalStatus.PENDING.value:
                dependencies_met = True
                if goal_data.get("dependencies"):
                    for dep_id in goal_data["dependencies"]:
                        dep_goal = self.goals.get(dep_id)
                        if not dep_goal or dep_goal["status"] != GoalStatus.COMPLETED.value:
                            dependencies_met = False
                            self.logger.debug(f"Goal '{goal_id}' dependency '{dep_id}' not met (status: {dep_goal['status'] if dep_goal else 'Not Found'}).")
                            break 
                if dependencies_met:
                    actionable_goals.append({"id": goal_id, **goal_data})
        
        if not actionable_goals:
            self.logger.info("No actionable pending goals found.")
            return None

        # Sort by priority (descending)
        actionable_goals.sort(key=lambda g: g["priority"], reverse=True)
        
        selected_goal = actionable_goals[0]
        self.logger.info(f"Selected next goal (placeholder): ID='{selected_goal['id']}', Description='{selected_goal['description']}'")
        return selected_goal

    def get_module_info(self) -> dict:
        """
        Provides information about the module's capabilities.
        """
        return {
            "module_name": "GoalManager",
            "description": "Manages agent goals, including their status, priority, and dependencies. Provides placeholder logic for selecting the next actionable goal.",
            "methods": {
                "add_goal": {
                    "description": "Adds a new goal to the manager.",
                    "parameters": {
                        "description": "str (Goal description)",
                        "priority": "int (Optional, default 0)",
                        "goal_id": "str (Optional, auto-generated if None)",
                        "dependencies": "list[str] (Optional, list of prerequisite goal IDs)",
                        "notes": "str (Optional, additional notes)"
                    },
                    "returns": "str (Goal ID)"
                },
                "get_goal": {
                    "description": "Retrieves a goal by its ID.",
                    "parameters": {"goal_id": "str"},
                    "returns": "dict or None (Goal details or None if not found)"
                },
                "update_goal_status": {
                    "description": "Updates the status of a goal (e.g., PENDING, ACTIVE, COMPLETED, FAILED, PAUSED).",
                    "parameters": {
                        "goal_id": "str", 
                        "status": "GoalStatus enum value (e.g., GoalStatus.COMPLETED)",
                        "notes": "str (Optional, notes for the status update)"
                    },
                    "returns": "bool (True if successful)"
                },
                "list_goals": {
                    "description": "Lists all goals, optionally filtered by status.",
                    "parameters": {"status_filter": "GoalStatus enum value (Optional)"},
                    "returns": "list[dict] (List of goal dictionaries)"
                },
                "get_next_goal_placeholder": {
                    "description": "Placeholder: Selects the next actionable PENDING goal based on priority and met dependencies.",
                    "parameters": {},
                    "returns": "dict or None (The selected goal or None)"
                }
            }
        }

if __name__ == '__main__':
    # Example Usage (for testing the module directly)
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    test_logger = logging.getLogger("GoalManagerTest")
    
    manager = GoalManager(test_logger)
    test_logger.info(f"Module Info: {json.dumps(manager.get_module_info(), indent=2)}")

    # Add some goals
    gid1 = manager.add_goal("Setup project environment", priority=10)
    gid2 = manager.add_goal("Develop core feature A", priority=5, dependencies=[gid1])
    gid3 = manager.add_goal("Write documentation for feature A", priority=2, dependencies=[gid2])
    gid4 = manager.add_goal("Research alternative solutions", priority=1)

    test_logger.info(f"\nAll goals initially: {json.dumps(manager.list_goals(), indent=2)}")

    # Test get_next_goal_placeholder and status updates
    test_logger.info("\n--- Testing get_next_goal_placeholder and status updates ---")
    
    next_goal = manager.get_next_goal_placeholder()
    if next_goal:
        test_logger.info(f"First next goal: {next_goal['description']} (ID: {next_goal['id']})") # Expected: Setup project environment
        assert next_goal['id'] == gid1
        manager.update_goal_status(next_goal['id'], GoalStatus.COMPLETED, "Environment setup complete.")
    else:
        test_logger.error("Did not get gid1 as first goal.")

    next_goal = manager.get_next_goal_placeholder()
    if next_goal:
        test_logger.info(f"Second next goal: {next_goal['description']} (ID: {next_goal['id']})") # Expected: Develop core feature A (gid2) or Research (gid4)
                                                                                             # gid2 depends on gid1 (now COMPLETED), gid4 has no deps. gid2 has higher priority.
        assert next_goal['id'] == gid2
        manager.update_goal_status(next_goal['id'], GoalStatus.ACTIVE, "Development of Feature A in progress.")
    else:
        test_logger.error("Did not get gid2 as second goal after gid1 completion.")
    
    next_goal = manager.get_next_goal_placeholder() # gid2 is ACTIVE, so it should pick gid4
    if next_goal:
        test_logger.info(f"Third next goal: {next_goal['description']} (ID: {next_goal['id']})") # Expected: Research alternative solutions
        assert next_goal['id'] == gid4
        manager.update_goal_status(next_goal['id'], GoalStatus.COMPLETED, "Research done.")
    else:
        test_logger.error("Did not get gid4 as third goal.")

    # Complete gid2 to unblock gid3
    manager.update_goal_status(gid2, GoalStatus.COMPLETED, "Feature A developed and tested.")
    next_goal = manager.get_next_goal_placeholder()
    if next_goal:
        test_logger.info(f"Fourth next goal: {next_goal['description']} (ID: {next_goal['id']})") # Expected: Write documentation for feature A
        assert next_goal['id'] == gid3
        manager.update_goal_status(next_goal['id'], GoalStatus.COMPLETED, "Documentation written.")
    else:
        test_logger.error("Did not get gid3 as fourth goal.")

    test_logger.info(f"\nGoals with PENDING status: {json.dumps(manager.list_goals(GoalStatus.PENDING), indent=2)}")
    test_logger.info(f"Goal details for {gid1}: {json.dumps(manager.get_goal(gid1), indent=2)}")
    test_logger.info(f"Goal details for {gid2}: {json.dumps(manager.get_goal(gid2), indent=2)}")

    test_logger.info("\nGoalManager test complete.")
