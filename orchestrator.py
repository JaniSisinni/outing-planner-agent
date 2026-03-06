"""
orchestrator.py — Claude agent loop with tool use.

Manages multi-turn conversation history and handles Claude's tool calls
for weather and maps lookups.
"""

import json
import os
import anthropic
from .prompts import SYSTEM_PROMPT
from tools.tool_registry import TOOL_DEFINITIONS
from tools.weather_tool import WeatherTool
from tools.maps_tool import MapsTool


class OutingAgent:
    """Stateful agent that maintains conversation history per session."""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        self.model = "claude-sonnet-4-20250514"
        self.history: list[dict] = []
        self.weather_tool = WeatherTool()
        self.maps_tool = MapsTool()

    def chat(self, user_message: str) -> str:
        """Send a user message and return Claude's response (with tool use)."""
        self.history.append({"role": "user", "content": user_message})

        while True:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                system=SYSTEM_PROMPT,
                tools=TOOL_DEFINITIONS,
                messages=self.history,
            )

            # Append assistant response to history
            self.history.append({"role": "assistant", "content": response.content})

            # If Claude is done (no tool use), return the text
            if response.stop_reason == "end_turn":
                return self._extract_text(response.content)

            # Handle tool calls
            if response.stop_reason == "tool_use":
                tool_results = self._handle_tool_calls(response.content)
                self.history.append({"role": "user", "content": tool_results})
                continue

            # Fallback
            return self._extract_text(response.content)

    def _handle_tool_calls(self, content_blocks: list) -> list:
        """Process tool calls from Claude."""
        results = []
        for block in content_blocks:
            if block.type != "tool_use":
                continue

            result = self._execute_tool(block.name, block.input)
            results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": json.dumps(result),
            })
        return results

    def _execute_tool(self, tool_name: str, tool_input: dict) -> dict:
        """Execute a single tool and return result."""
        try:
            if tool_name == "get_weather":
                return self.weather_tool.get_weather(**tool_input)
            elif tool_name == "search_places":
                return self.maps_tool.search_places(**tool_input)
            else:
                return {"error": f"Unknown tool: {tool_name}"}
        except ValueError as e:
            return {"error": f"Invalid input: {str(e)}"}
        except Exception as e:
            return {"error": f"Tool failed: {str(e)}"}

    @staticmethod
    def _extract_text(content_blocks: list) -> str:
        return " ".join(
            block.text for block in content_blocks if hasattr(block, "text")
        ).strip()
