"""MCP-style tool server: backend tools an LLM client can call.

The tools are plain Python functions with a small registry, so an
MCP-compatible client can list them and call them by name.
"""

from fastapi import FastAPI

app = FastAPI(title="mcp-tool-server")

RECORDS = {
    "1001": {"id": "1001", "type": "ticket", "status": "open"},
    "1002": {"id": "1002", "type": "ticket", "status": "closed"},
}

TOOLS = {}


def tool(name):
    def register(func):
        TOOLS[name] = func
        return func
    return register


@tool("lookup_record")
def lookup_record(record_id: str):
    """Look up a record by id in a backend store."""
    return RECORDS.get(record_id, {"error": "record not found"})


@tool("create_ticket")
def create_ticket(subject: str, message: str):
    """Create a support ticket with a subject and message."""
    ticket_id = str(1000 + len(RECORDS) + 1)
    RECORDS[ticket_id] = {"id": ticket_id, "subject": subject, "message": message, "status": "open"}
    return RECORDS[ticket_id]


@tool("send_notification")
def send_notification(channel: str, message: str):
    """Send a notification to a recipient channel."""
    return {"channel": channel, "message": message, "sent": True}


@app.get("/tools")
def list_tools():
    return {"tools": sorted(TOOLS)}


@app.post("/tools/{name}")
def call_tool(name: str, payload: dict):
    func = TOOLS.get(name)
    if func is None:
        return {"error": "unknown tool"}
    return func(**payload)
