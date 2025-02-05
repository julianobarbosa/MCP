# Product Context: MCP Servers

## Overview
This project contains implementations of various Model Context Protocol (MCP) servers that extend the capabilities of the MCP ecosystem.

## Servers

### Pre-Commit Server (Python)

#### Why this project exists
This project exists to provide a Model Context Protocol (MCP) server that integrates pre-commit functionality into the MCP ecosystem. It allows running pre-commit hooks and managing spell-checking dictionaries through MCP tools.

#### Problems it solves
1. Enables running pre-commit checks through MCP tools
2. Provides spell-checking dictionary management capabilities
3. Integrates code quality tooling into the MCP ecosystem
4. Allows selective running of specific hooks or all hooks
5. Supports automatic fixing of issues where possible

#### How it should work
The server exposes two main tools:

1. `run_checks`:
   - Can run specific pre-commit hooks or all hooks
   - Supports checking specific files or all files
   - Can attempt to automatically fix issues
   - Returns output from the pre-commit process

2. `add_words`:
   - Adds words to cspell dictionaries
   - Supports multiple language dictionaries (en, pt-BR)
   - Maintains sorted word lists
   - Prevents duplicate entries
