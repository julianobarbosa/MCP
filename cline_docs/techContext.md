# Technical Context

## General MCP Server Requirements
- MCP SDK must be available
- Servers run on stdio transport only
- Execute permissions required for server scripts

## Pre-Commit Server (Python)

### Technologies Used
- Python 3.x
- MCP SDK (`mcp[cli]`)
- pre-commit >= 3.5.0

### Development Setup
1. Python environment with required dependencies:
   ```
   mcp[cli]
   pre-commit>=3.5.0
   ```

2. The server requires:
   - A properly configured pre-commit installation
   - Access to `.cspell.json` and `.cspell-pt-br.json` for dictionary management
   - Execute permissions on the Python script

### Technical Constraints
1. The server runs on stdio transport only
2. Dictionary files must be accessible in the working directory:
   - `.cspell.json` for English
   - `.cspell-pt-br.json` for Portuguese
3. The pre-commit binary must be available in the system PATH
4. The server assumes pre-commit hooks are properly configured in the project

### Error Handling
1. Pre-commit execution errors are captured and returned with error details
2. Dictionary file operations handle:
   - Missing files
   - Invalid JSON
   - File access errors

### Architecture Decisions
1. Uses async/await for operation handling
2. Implements stdio transport for MCP communication
3. Uses subprocess for pre-commit execution
4. Maintains sorted word lists in dictionaries