# ChatGPT MCP Server

A Model Context Protocol (MCP) server that enables AI assistants to interact with the ChatGPT desktop app on macOS.

## Features

- Send prompts to ChatGPT from any MCP-compatible AI assistant
- Built with Python and FastMCP

**Note:** This server only supports English text input. Non-English characters may not work properly.

## Installation

### Prerequisites
- macOS
- ChatGPT desktop app installed and running
- Python 3.10+
- uv package manager

## For Claude Code Users

Simply run:
```bash
claude mcp add chatgpt-mcp uvx chatgpt-mcp
```

That's it! You can start using ChatGPT commands in Claude Code.

## For Other MCP Clients

### Step 1: Install the MCP Server

#### Option A: Install from PyPI (Recommended)
```bash
# Install with uv
uv add chatgpt-mcp
```

#### Option B: Manual Installation
```bash
# Clone the repository
git clone https://github.com/xncbf/chatgpt-mcp
cd chatgpt-mcp

# Install dependencies with uv
uv sync
```

### Step 2: Configure Your MCP Client

If installed from PyPI, add to your MCP client configuration:
```json
{
  "mcpServers": {
    "chatgpt": {
      "command": "uvx",
      "args": ["chatgpt-mcp"]
    }
  }
}
```

If manually installed, add to your MCP client configuration:
```json
{
  "mcpServers": {
    "chatgpt": {
      "command": "uv",
      "args": ["run", "chatgpt-mcp"],
      "cwd": "/path/to/chatgpt-mcp"
    }
  }
}
```

## Usage

1. **Open ChatGPT desktop app** and make sure it's running
2. **Open your MCP client** (Claude Code, etc.)
3. **Use ChatGPT commands** in your AI assistant:
   - "Send a message to ChatGPT"
   - "Create a new ChatGPT conversation"
   - "Get my ChatGPT conversations"

The AI assistant will automatically use the appropriate MCP tools to interact with ChatGPT.

## Available Tools

### ask_chatgpt
Send a prompt to ChatGPT and receive the response.

```python
ask_chatgpt(prompt="Hello, ChatGPT!")
```

### get_chatgpt_response
Get the latest response from ChatGPT after sending a message.

```python
get_chatgpt_response()
```

## License

MIT
