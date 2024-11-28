from typing import Any, Dict, List, Callable
import inspect
import json
class ConverseToolManager:
    def __init__(self):
        self._tools = {}
    def register_tool(self, name, func, description, input_schema):
        self._tools[name] = {
            'function': func,
            'description': description,
            'input_schema': input_schema
        }
    def get_tools(self):
        tool_specs = []
        for name, tool in self._tools.items():
            tool_specs.append({
                'toolSpec': {
                    'name': name,
                    'description': tool['description'],
                    'inputSchema': tool['input_schema']
                }
            })
        return {'tools': tool_specs}
    def execute_tool(self, payload):
        tool_use_id = payload['toolUseId']
        tool_name = payload['name']
        tool_input = payload['input']
        if tool_name not in self._tools:
            raise ValueError(f"Unknown tool: {tool_name}")
        try:
            tool_func = self._tools[tool_name]['function']
            result = tool_func(**tool_input)
            return {
                'toolUseId': tool_use_id,
                'content': [{'text': str(result)}],
                'status': 'success'
            }
        except Exception as e:
            return {
                'toolUseId': tool_use_id,
                'content': [{'text': str(e)}],
                'status': 'error'
            }
    def clear_tools(self):
        """Reset all cyber tools."""
        self._tools.clear()