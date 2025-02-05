# System Patterns

## General MCP Server Patterns
### Request Handler Pattern
```python
@server.request_handler(SchemaType)
async def handle_request(request):
    return {
        "content": [
            {
                "type": "text",
                "text": "response content"
            }
        ],
        "isError": bool  # optional
    }
```

### Error Handling Pattern
1. Try-except blocks around operations
2. Return standardized error responses
3. Include relevant error details
4. Proper error categorization

## Pre-Commit Server (Python)
### Code Organization
1. Single server class pattern (`PreCommitServer`)
2. Separation of tool handlers into distinct methods
3. Consistent error handling and response formatting

### Tool Implementation Pattern
1. Input Schema Definition:
   ```python
   {
       "type": "object",
       "properties": {
           "paramName": {
               "type": "type",
               "description": "description"
           }
       },
       "required": ["requiredParams"]  # optional
   }
   ```

2. Command Construction Pattern:
   ```python
   cmd = ["base", "command"]
   if optional_param:
       cmd.append(optional_param)
   cmd.extend(["--flag"] + values)
   ```

### Dictionary Management Pattern
1. Load existing dictionary
2. Ensure "words" list exists
3. Add new words (avoiding duplicates)
4. Sort word list
5. Save updated dictionary

### Error Handling Pattern
1. Try-except blocks around operations
2. Capture and format subprocess errors
3. Return standardized error responses
4. Include both stdout and stderr in responses
