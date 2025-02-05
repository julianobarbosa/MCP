# Active Context

##  For spell-checking
### Current State
The pre-commit server is operational and provides two main tools:
1. `run_checks` - For executing pre-commit hooks
2. `add_words` - For managing spell-check dictionaries

### Recent Changes
Initial implementation includes:
- Basic server setup with stdio transport
- Pre-commit hook execution functionality
- Dictionary management for spell checking
- Support for English and Portuguese dictionaries
- Error handling for both tools

### Next Steps
Potential improvements:
1. Add support for:
   - Hook configuration management
   - Additional dictionary languages
   - Custom hook parameters
2. Enhance error reporting with:
   - More detailed error categories
   - Structured error responses
   - Hook-specific error handling
3. Implement:
   - Hook status reporting
   - Performance metrics
   - Caching mechanisms for dictionary operations