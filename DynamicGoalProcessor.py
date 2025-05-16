# C:\Users\m.2 SSD\Desktop\lastagent\agent006\DynamicGoalProcessor.py
"""
DynamicGoalProcessor (DGP) for agent006.

Manages the agent's goals with flexibility, allowing for dynamic
re-prioritization, sophisticated decomposition, and contingency planning.
"""

class DynamicGoalProcessor:
    def __init__(self, logger):
        self.logger = logger
        self.goals = [] # List of goal objects/dictionaries
        self.current_primary_goal = None
        self.logger.info("DynamicGoalProcessor initialized.")

    def set_primary_goal(self, goal_description, priority=10):
        new_goal = {"description": goal_description, "priority": priority, "status": "active", "sub_goals": []}
        self.goals.append(new_goal)
        self.current_primary_goal = new_goal # Simplified for now
        self.logger.info(f"DGP: New primary goal set: {goal_description} with priority {priority}")

    def get_current_highest_priority_goal(self):
        if not self.goals:
            return None
        # Simple highest priority, could be more complex
        active_goals = [g for g in self.goals if g.get("status") == "active"]
        return max(active_goals, key=lambda g: g.get("priority", 0)) if active_goals else None

    def update_goal_status(self, goal_description, new_status, reason=""):
        for goal in self.goals:
            if goal["description"] == goal_description:
                goal["status"] = new_status
                self.logger.info(f"DGP: Goal '{goal['description']}' status updated to '{new_status}'. Reason: {reason}")
                # If it was the primary goal and now completed/failed,
                # current_primary_goal might need re-evaluation if we had multiple active goals
                # or a queue. For now, get_current_highest_priority_goal handles finding the next active one.
                if self.current_primary_goal and self.current_primary_goal["description"] == goal_description:
                    if new_status not in ["active", "pending"]: # e.g., completed, failed, paused
                        pass # self.current_primary_goal will be naturally replaced by the next call to get_current_highest_priority_goal
                return
        self.logger.warning(f"DGP: Goal '{goal_description}' not found for status update to '{new_status}'.")