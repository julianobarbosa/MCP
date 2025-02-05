#!/usr/bin/env python3

"""MCP server implementation for running pre-commit hooks.

This module provides a server that integrates with Model Context Protocol (MCP)
to enable running pre-commit hooks and managing spell check dictionaries.
"""

import asyncio
import json
import subprocess
import sys
from typing import Any, Dict, List, Optional

from mcp.sdk.server.transport import create_stdio_transport
from mcp.server import Server
from mcp.types import (
    CallToolRequestSchema,
    ErrorCode,
    ListToolsRequestSchema,
    McpError,
)


class PreCommitServer:
    """Server for managing pre-commit hooks and spell check dictionaries via MCP."""

    def __init__(self):
        """Initialize PreCommitServer with default configuration."""
        self.server = Server(
            name="pre-commit-server", version="0.1.0", capabilities={"tools": {}}
        )
        self._setup_handlers()

    def _setup_handlers(self):
        """Set up request handlers for the MCP server."""

        @self.server.request_handler(ListToolsRequestSchema)
        async def handle_list_tools(request):
            return {
                "tools": [
                    {
                        "name": "run_checks",
                        "description": (
                            "Run pre-commit checks on specified files or all files"
                        ),
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "hook": {
                                    "type": "string",
                                    "description": (
                                        "Specific hook to run (e.g., 'cspell', 'stylua'). "
                                        "Leave empty to run all hooks."
                                    ),
                                },
                                "files": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": (
                                        "List of files to check. "
                                        "Leave empty to check all files."
                                    ),
                                },
                                "fix": {
                                    "type": "boolean",
                                    "description": "Attempt to automatically fix issues when possible",
                                },
                            },
                        },
                    },
                    {
                        "name": "add_words",
                        "description": "Add words to cspell dictionary",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "words": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "List of words to add to dictionary",
                                },
                                "language": {
                                    "type": "string",
                                    "description": "Target language dictionary (e.g., 'en', 'pt-BR')",
                                    "default": "en",
                                },
                            },
                            "required": ["words"],
                        },
                    },
                ]
            }

        @self.server.request_handler(CallToolRequestSchema)
        async def handle_call_tool(request):
            if request.params.name == "run_checks":
                return await self._run_checks(request.params.arguments)
            elif request.params.name == "add_words":
                return await self._add_words(request.params.arguments)
            else:
                raise McpError(
                    ErrorCode.MethodNotFound, f"Unknown tool: {request.params.name}"
                )

    async def _run_checks(self, args: Dict[str, Any]):
        """Run pre-commit checks on specified files.

        Args:
            args: Dictionary containing hook name, files list, and fix flag.

        Returns:
            Dictionary containing check results and any error information.
        """
        hook: Optional[str] = args.get("hook")
        files: List[str] = args.get("files", [])
        fix: bool = args.get("fix", False)

        cmd = ["pre-commit", "run"]
        if hook:
            cmd.append(hook)
        if fix:
            cmd.append("--fix")
        if files:
            cmd.extend(["--files"] + files)
        else:
            cmd.append("--all-files")

        try:
            process = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return {
                "content": [{"type": "text", "text": process.stdout + process.stderr}]
            }
        except subprocess.CalledProcessError as e:
            return {
                "content": [{"type": "text", "text": e.stdout + e.stderr}],
                "isError": True,
            }

    async def _add_words(self, args: Dict[str, Any]):
        """Add words to the cspell dictionary.

        Args:
            args: Dictionary containing words to add and target language.

        Returns:
            Dictionary containing operation result and any error information.
        """
        words: List[str] = args["words"]
        language: str = args.get("language", "en")
        dictionary_file = (
            ".cspell-pt-br.json" if language == "pt-BR" else ".cspell.json"
        )

        try:
            with open(dictionary_file, "r") as f:
                dictionary = json.load(f)

            if "words" not in dictionary:
                dictionary["words"] = []

            new_words = [word for word in words if word not in dictionary["words"]]
            if new_words:
                dictionary["words"].extend(new_words)
                dictionary["words"].sort()

                with open(dictionary_file, "w") as f:
                    json.dump(dictionary, f, indent=2)

                return {
                    "content": [{
                        "type": "text",
                        "text": f"Added {len(new_words)} new words to {dictionary_file}",
                    }]
                }
            else:
                return {"content": [{"type": "text", "text": "No new words to add"}]}
        except Exception as e:
            return {
                "content": [
                    {"type": "text", "text": f"Error updating dictionary: {str(e)}"}
                ],
                "isError": True,
            }

    async def run(self):
        """Start the MCP server using stdio transport."""
        stdio_transport = create_stdio_transport()
        await self.server.connect(stdio_transport)
        print("Pre-commit MCP server running on stdio", file=sys.stderr)


if __name__ == "__main__":
    server = PreCommitServer()
    asyncio.run(server.run())
