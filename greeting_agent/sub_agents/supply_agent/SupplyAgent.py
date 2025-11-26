from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext


import base64
import json
import time
from flask import Flask, request
from google.cloud import firestore

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:/VSCode/GoogleADK/config/multi-ai-agent-system-463413-c47d52cb8ac2.json"

app = Flask(__name__)
db = firestore.Client()

@app.route("/", methods=["POST"])
def handle_task():
    envelope = request.get_json()
    if not envelope or "message" not in envelope:
        return "Invalid Pub/Sub message", 400

    message = envelope["message"]
    payload = base64.b64decode(message["data"]).decode("utf-8")
    task = json.loads(payload)

    print(f"[Supply Task Received] {task}")

    if task.get("agent") != "Supply":
        return "Ignored - Not a Supply Task", 200

    zone = task["zone"]
    deliver_supplies(zone)

    return "OK", 200

def deliver_supplies(zone):
    # Simulate checking inventory
    inventory_ref = db.collection("inventory").document("main")
    inventory = inventory_ref.get().to_dict() or {}

    if inventory.get("med_kit", 0) > 0:
        inventory_ref.update({"med_kit": firestore.Increment(-1)})
        status = "Delivered"
    else:
        status = "Out of Stock"

    # Log supply delivery attempt
    db.collection("missions").add({
        "zone": zone,
        "type": "Supply",
        "status": status,
        "timestamp": time.time()
    })

    print(f"[Supply Delivery] Zone: {zone}, Status: {status}")


# supply_agent = Agent(
#     name="supply_agent",
#     model="gemini-2.0-flash",
#     description="An agent that tells nerdy jokes about various topics.",
#     instruction="""
    
#     you should delegate the task to the manager agent.
#     """,
#     tools=[],

# )
