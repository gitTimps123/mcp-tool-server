# mcp-tool-server

MCP server exposing backend tools (database lookup, ticket creation, notifications) for LLM tool-calling.

## Tools exposed

- `lookup_record` — look up a record by id in a backend store.
- `create_ticket` — create a support ticket with a subject and message.
- `send_notification` — send a notification to a recipient channel.

## How an LLM client calls them

An LLM client connects to this server, lists the available tools, and calls a tool by name with its arguments. The server runs the matching Python function and returns the result to the client, which can then continue the conversation using that result.

## Stack

- Python
- MCP
- FastAPI

## How to run

```bash
pip install -r requirements.txt
python server.py
```
