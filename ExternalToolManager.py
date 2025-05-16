import logging

class ExternalToolManager:
    def __init__(self, logger: logging.Logger):
        """
        Initializes the ExternalToolManager.

        Args:
            logger (logging.Logger): The logger instance for logging messages.
        """
        self.logger = logger
        self.available_tools = {} # Stores registered tools: tool_name -> {handler, description, parameters_schema}
        self.logger.info("ExternalToolManager initialized.")

    def discover_tools(self, tool_directory: str = "tools"):
        """
        Placeholder method for discovering available tools from a specified directory.

        This method is intended to scan a directory for tool definitions (e.g.,
        Python modules acting as plugins, JSON/YAML description files) and
        automatically register them for use by the agent.

        How it might be used:
        The agent's core system could call this method during its initialization phase
        or dynamically if new tool packages are installed or made available.
        For example:
        `tool_manager_instance.discover_tools(tool_directory="C:\\path\\to\\agent_tools_repository")`
        or, using a relative path from the agent's root:
        `tool_manager_instance.discover_tools(tool_directory="core_tools/community_plugins")`

        Args:
            tool_directory (str): The path to the directory where tool definitions
                                  are located. This could be an absolute path or
                                  relative to the agent's working directory.
                                  Defaults to a 'tools' subdirectory.
        """
        self.logger.info(f"Placeholder: Attempting to discover tools from directory: {tool_directory}")
        # TODO: Implement the actual discovery logic. This might involve:
        # 1. Listing files/subdirectories in `tool_directory`.
        # 2. Identifying potential tool modules (e.g., by naming convention or metadata files).
        # 3. For Python-based tools: Dynamically importing modules.
        # 4. For declarative tools (JSON/YAML): Parsing definition files.
        # 5. Extracting necessary information: tool name, handler function/class,
        #    description, expected parameters, etc.
        # 6. Registering valid tools using `self.register_tool()`.
        #
        # Example of what a discovered tool entry in self.available_tools might look like
        # after being processed by a (yet to be implemented) registration mechanism:
        # self.available_tools['advanced_calculator'] = {
        #     'handler': <function advanced_calculator_function>,
        #     'description': 'Performs advanced mathematical operations.',
        #     'parameters_schema': {'operation': 'str', 'operand1': 'float', 'operand2': 'float'}
        # }
        self.logger.warning(f"Tool discovery functionality from '{tool_directory}' is a placeholder and not yet implemented.")
        # For now, this method does nothing beyond logging.
        pass

    def register_tool(self, tool_name: str, tool_handler: callable, description: str, parameters_schema: dict) -> bool:
        """
        Manually registers a new tool or API that the agent can use.

        This method allows for explicit registration of tools, which can be useful
        for core tools or tools that are not discoverable via the `discover_tools` method.

        Args:
            tool_name (str): A unique name for the tool (e.g., "web_search", "file_reader").
            tool_handler (callable): The actual Python function or method that implements
                                     the tool's logic. This callable will be invoked when
                                     `use_tool` is called for this tool.
            description (str): A natural language description of what the tool does,
                               its purpose, and when it might be useful.
            parameters_schema (dict): A dictionary describing the parameters the tool_handler
                                      expects. Keys are parameter names. Values could be
                                      type hints (e.g., str, int), JSON schema, or descriptive
                                      strings. Example:
                                      `{"query": "The search term (string)", "max_results": "Max number of results (int, optional)"}`
        Returns:
            bool: True if registration was successful, False otherwise.
        """
        if not isinstance(tool_name, str) or not tool_name:
            self.logger.error("Tool registration failed: tool_name must be a non-empty string.")
            return False
        if not callable(tool_handler):
            self.logger.error(f"Tool registration failed for '{tool_name}': tool_handler must be callable.")
            return False
        if not isinstance(description, str):
            self.logger.error(f"Tool registration failed for '{tool_name}': description must be a string.")
            return False
        if not isinstance(parameters_schema, dict):
            self.logger.error(f"Tool registration failed for '{tool_name}': parameters_schema must be a dictionary.")
            return False

        if tool_name in self.available_tools:
            self.logger.warning(f"Tool '{tool_name}' is already registered. Overwriting existing definition.")

        self.available_tools[tool_name] = {
            "handler": tool_handler,
            "description": description,
            "parameters_schema": parameters_schema
        }
        self.logger.info(f"Tool '{tool_name}' registered successfully. Description: {description}")
        return True

    def use_tool(self, tool_name: str, **kwargs):
        """
        Executes a registered tool with the given named arguments.

        How it might be used:
        If a "weather_tool" is registered:
        `current_weather = tool_manager_instance.use_tool("weather_tool", city="London", units="celsius")`

        Args:
            tool_name (str): The name of the tool to use (must match a registered tool).
            **kwargs: Keyword arguments to pass to the tool's handler function.
                      These should match the parameters defined in the tool's
                      `parameters_schema` during registration.

        Returns:
            The result of the tool's execution. The type and structure of the result
            depend on the specific tool's implementation.
            Returns an error message string if the tool is not found or if execution fails.
        """
        if tool_name not in self.available_tools:
            self.logger.error(f"Tool '{tool_name}' not found. Available tools: {list(self.available_tools.keys())}")
            return f"Error: Tool '{tool_name}' not found."

        tool_info = self.available_tools[tool_name]
        tool_handler = tool_info["handler"]
        # Basic parameter validation could be enhanced here using parameters_schema
        # For example, checking for required parameters or type mismatches.

        try:
            self.logger.info(f"Attempting to use tool '{tool_name}' with arguments: {kwargs}")
            result = tool_handler(**kwargs)
            self.logger.info(f"Tool '{tool_name}' executed successfully.")
            return result
        except TypeError as te:
            # Catch errors related to incorrect arguments passed to the handler
            self.logger.error(f"TypeError executing tool '{tool_name}': {te}. Check arguments: {kwargs}. Expected by handler: {tool_info.get('parameters_schema', 'N/A')}", exc_info=True)
            return f"Error (TypeError) executing tool '{tool_name}': {te}. Arguments: {kwargs}."
        except Exception as e:
            self.logger.error(f"An unexpected error occurred while executing tool '{tool_name}': {e}", exc_info=True)
            return f"Error (Exception) executing tool '{tool_name}': {str(e)}"

    def list_available_tools(self) -> dict:
        """
        Provides a dictionary of available tools and their descriptions.

        Returns:
            dict: A dictionary where keys are tool names and values are dictionaries
                  containing 'description' and 'parameters_schema'.
                  Example:
                  {
                      "web_search": {
                          "description": "Performs a web search.",
                          "parameters_schema": {"query": "Search term", "limit": "Max results"}
                      }
                  }
        """
        if not self.available_tools:
            self.logger.info("No tools are currently registered.")
            return {}

        tools_summary = {}
        for name, info in self.available_tools.items():
            tools_summary[name] = {
                "description": info["description"],
                "parameters_schema": info["parameters_schema"]
            }
        self.logger.debug(f"Listing available tools: {len(tools_summary)} tools found.")
        return tools_summary
