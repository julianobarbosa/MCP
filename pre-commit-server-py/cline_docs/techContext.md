# Technical Context: Pre-commit MCP Server

## Technology Stack

### Core Technologies
- Python 3.8+
- MCP SDK
- pre-commit framework
- cspell

### Development Tools
- pytest for testing
- flake8 for linting
- black for formatting
- mypy for type checking

## Development Environment

### Setup Requirements
```bash
# Core dependencies
pip install mcp[cli]
pip install pre-commit
pip install cspell

# Development dependencies
pip install pytest
pip install flake8
pip install black
pip install mypy
```

### Configuration Files
1. `pyproject.toml`
   - Project metadata
   - Build settings
   - Tool configurations

2. `.pre-commit-config.yaml`
   - Hook definitions
   - Plugin configurations
   - Execution settings

3. `cspell.json`
   - Dictionary configurations
   - Language settings
   - Custom word lists

## Implementation Details

### MCP Integration
```python
from mcp.server import Server
from mcp.types import CallToolRequestSchema

class PreCommitServer:
    def __init__(self):
        self.server = Server(
            name="pre-commit-server",
            version="1.0.0"
        )
```

### Hook Execution
```python
async def run_checks(self, files: List[str]) -> Dict[str, Any]:
    results = []
    for check in self.enabled_checks:
        result = await check.run(files)
        results.append(result)
    return self._format_results(results)
```

### Dictionary Management
```python
async def update_dictionary(self, words: List[str], lang: str = "en") -> bool:
    try:
        dict_path = self._get_dict_path(lang)
        async with aiofiles.open(dict_path, mode="a+") as f:
            await f.write("\n".join(words))
        return True
    except Exception as e:
        logging.error(f"Dictionary update failed: {str(e)}")
        return False
```

## Performance Considerations

1. Resource Usage
   - Memory: < 200MB per process
   - CPU: Efficient parallel processing
   - Disk: Minimal I/O for dictionary updates

2. Timeouts
   - Hook execution: 30s maximum
   - Dictionary operations: 5s maximum
   - MCP requests: 10s maximum

3. Concurrency
   - Async execution model
   - Process pool for CPU-bound tasks
   - Connection pooling for I/O operations

## Security Implementation

1. Input Validation
   ```python
   def validate_file_path(path: str) -> bool:
       return not any(
           bad_pattern in path
           for bad_pattern in UNSAFE_PATTERNS
       )
   ```

2. Process Isolation
   ```python
   def run_hook(cmd: List[str]) -> subprocess.CompletedProcess:
       return subprocess.run(
           cmd,
           capture_output=True,
           text=True,
           timeout=30,
           check=False
       )
   ```

3. Error Handling
   ```python
   try:
       result = await self._execute_check(files)
   except Exception as e:
       logging.error(f"Check failed: {str(e)}")
       return {
           "status": "error",
           "message": str(e),
           "context": self._get_error_context(e)
       }
   ```

## Dependencies

### Required Packages
- mcp-sdk>=1.0.0
- pre-commit>=3.0.0
- cspell>=6.0.0
- aiofiles>=0.8.0
- pydantic>=2.0.0

### Optional Packages
- rich>=12.0.0 (for enhanced logging)
- uvloop>=0.16.0 (for performance)
- orjson>=3.8.0 (for faster JSON)
