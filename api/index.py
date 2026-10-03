from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Mouse Control API")

class MouseCommand(BaseModel):
    action: str  # e.g., "move", "click"
    x: int = 0
    y: int = 0

# In-memory store for demonstration (use a database or Redis for production)
latest_command = {"action": "none", "x": 0, "y": 0}

@app.get("/")
def home():
    return {"status": "Vercel Python Mouse Control API is live!"}

@app.post("/api/command")
def set_command(cmd: MouseCommand):
    global latest_command
    latest_command = cmd.dict()
    return {"success": True, "command": latest_command}

@app.get("/api/command")
def get_command():
    return latest_command