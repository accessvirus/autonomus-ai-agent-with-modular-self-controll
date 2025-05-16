# C:\Users\m.2 SSD\Desktop\lastagent\self_reflection_analyst.py
import logging

class SelfReflectionAnalyst:
    """
    A module to enable the agent to reflect on its performance,
    analyze failures, and suggest improvements or alternative strategies.
    """

    def __init__(self, logger: logging.Logger):
        """
        Initializes the SelfReflectionAnalyst.

        Args:
            logger (logging.Logger): A logger instance for logging messages.
        """
        self.logger = logger
        self.logger.info("SelfReflectionAnalyst initialized.")

    def analyze_recent_performance(self, recent_actions: list, goal_status: dict) -> dict:
        """
        Analyzes recent actions and their outcomes in relation to the current goal.
        This is a placeholder method.

        Actual implementation might involve:
        - Identifying patterns in successful/failed actions.
        - Checking if progress is being made towards the goal.
        - Detecting repetitive failures or loops.
        - Suggesting changes to strategy or parameters.

        Args:
            recent_actions (list): A list of dictionaries, where each dictionary
                                   represents an action taken (e.g.,
                                   {'action_type': 'create_file', 'parameters': {...}, 'outcome': 'success/failure', 'error': '...'}).
            goal_status (dict): Information about the current primary goal,
                                e.g., {'goal_description': '...', 'status': 'in_progress/failed', 'reason_for_failure': '...'}.

        Returns:
            dict: An analysis report, which could include:
                  - 'summary': A brief text summary of the performance.
                  - 'suggestions': A list of actionable suggestions (e.g., "Try alternative tool X", "Modify parameter Y").
                  - 'confidence_score': A score indicating confidence in the current approach.

        Example Usage:
            # analyst = SelfReflectionAnalyst(my_logger)
            # actions = [
            #     {'action_type': 'execute_code', 'parameters': {'code_string': 'print(1/0)'}, 'outcome': 'failure', 'error': 'ZeroDivisionError'},
            #     {'action_type': 'create_file', 'parameters': {'file_path': 'test.txt', 'content': 'hello'}, 'outcome': 'success', 'error': None}
            # ]
            # current_goal_info = {'goal_description': 'Write and test a script.', 'status': 'in_progress'}
            # analysis = analyst.analyze_recent_performance(actions, current_goal_info)
            # if analysis['suggestions']:
            #     my_logger.info(f"Suggestions from reflection: {analysis['suggestions']}")
        """
        self.logger.info(f"Analyzing recent performance for goal: {goal_status.get('goal_description', 'N/A')}")

        # Placeholder logic
        analysis_report = {
            "summary": "Performance analysis placeholder. No specific issues detected or suggestions generated.",
            "suggestions": [],
            "confidence_score": 0.75 # Default confidence
        }

        num_actions = len(recent_actions)
        failures = [action for action in recent_actions if action.get('outcome') == 'failure']
        num_failures = len(failures)

        if num_actions > 0:
            failure_rate = num_failures / num_actions
            analysis_report["summary"] = f"Analyzed {num_actions} actions. Failure rate: {failure_rate:.2%}."
            if failure_rate > 0.5:
                analysis_report["suggestions"].append("High failure rate detected. Review strategy or tool parameters.")
                analysis_report["confidence_score"] = 0.3
            elif num_failures > 0:
                error_messages = [str(f.get('error', 'Unknown error')) for f in failures]
                analysis_report["suggestions"].append(f"Encountered {num_failures} failure(s). Review logs for specific errors: {error_messages}")
                analysis_report["confidence_score"] = 0.5

        if goal_status.get('status') == 'failed':
            analysis_report["summary"] += f" Goal status is 'failed'. Reason: {goal_status.get('reason_for_failure', 'Unknown')}."
            analysis_report["suggestions"].append("Current goal failed. Consider re-evaluating the goal or breaking it down further.")
            analysis_report["confidence_score"] = 0.1


        self.logger.info(f"Performance analysis complete. Summary: {analysis_report['summary']}")
        return analysis_report

    # Another potential placeholder method:
    # def suggest_learning_objective(self, recurring_error_pattern: str) -> str:
    #     """
    #     Based on recurring errors, suggests a learning objective for the agent.
    #     e.g., "Learn to handle API rate limits for service X."
    #     """
    #     self.logger.info(f"Considering learning objective for error pattern: {recurring_error_pattern}")
    #     return f"Placeholder: Consider learning how to better handle '{recurring_error_pattern}'."

if __name__ == '__main__':
    # Example usage (for testing purposes when run directly)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger_main = logging.getLogger(__name__)

    analyst = SelfReflectionAnalyst(logger_main)

    logger_main.info("\n--- Test Case: Mixed Performance ---")
    actions1 = [
        {'action_type': 'execute_code', 'parameters': {'code_string': 'print(1/0)'}, 'outcome': 'failure', 'error': 'ZeroDivisionError: division by zero'},
        {'action_type': 'create_file', 'parameters': {'file_path': 'test.txt', 'content': 'hello'}, 'outcome': 'success', 'error': None},
        {'action_type': 'execute_code', 'parameters': {'code_string': 'x = y'}, 'outcome': 'failure', 'error': 'NameError: name y is not defined'}
    ]
    goal1 = {'goal_description': 'Write and test a script.', 'status': 'in_progress'}
    analysis1 = analyst.analyze_recent_performance(actions1, goal1)
    logger_main.info(f"Analysis 1: {analysis1}")
    assert "High failure rate" in analysis1["suggestions"][0]

    logger_main.info("\n--- Test Case: All Success ---")
    actions2 = [
        {'action_type': 'create_file', 'parameters': {'file_path': 'test.txt', 'content': 'hello'}, 'outcome': 'success', 'error': None},
        {'action_type': 'create_file', 'parameters': {'file_path': 'test2.txt', 'content': 'world'}, 'outcome': 'success', 'error': None}
    ]
    goal2 = {'goal_description': 'Create documentation files.', 'status': 'in_progress'}
    analysis2 = analyst.analyze_recent_performance(actions2, goal2)
    logger_main.info(f"Analysis 2: {analysis2}")
    assert not analysis2["suggestions"] # No suggestions if all success and goal in progress

    logger_main.info("\n--- Test Case: Goal Failed ---")
    actions3 = [
        {'action_type': 'execute_code', 'parameters': {'code_string': 'print(\"ok\")'}, 'outcome': 'success', 'error': None}
    ]
    goal3 = {'goal_description': 'Execute critical task.', 'status': 'failed', 'reason_for_failure': 'External API unresponsive'}
    analysis3 = analyst.analyze_recent_performance(actions3, goal3)
    logger_main.info(f"Analysis 3: {analysis3}")
    assert "Current goal failed" in analysis3["suggestions"][0]
    
    logger_main.info("\nExample tests completed.")
