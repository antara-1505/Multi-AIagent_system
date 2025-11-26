from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

import base64
import json
import time
from flask import Flask, request
from google.cloud import firestore, pubsub_v1
from project_config import PROJECT_ID

app = Flask(__name__)
db = firestore.Client()
publisher = pubsub_v1.PublisherClient()

@app.route("/", methods=["POST"])
def handle_pubsub_event():
    envelope = request.get_json()
    if not envelope or "message" not in envelope:
        return "Invalid Pub/Sub message", 400

    message = envelope["message"]
    payload = base64.b64decode(message["data"]).decode("utf-8")
    data = json.loads(payload)

    print(f"[Coordinator Received] {data}")

    zone = data.get("zone")
    risk_type = data.get("type")

    # Save incoming alert to Firestore
    db.collection("alerts").add(data)

    # Decide which agent to assign
    if "Flood" in risk_type or "Blocked" in risk_type:
        assign_agent(zone, "Rescue")
    if "Rain" in risk_type:
        assign_agent(zone, "Supply")

    return "OK", 200

def assign_agent(zone, agent_type):
    task = {
        "agent": agent_type,
        "zone": zone,
        "priority": "High",
        "timestamp": time.time()
    }
    topic_path = publisher.topic_path(PROJECT_ID, 'task-assignments')
    publisher.publish(topic_path, json.dumps(task).encode("utf-8"))
    print(f"[Task Assigned] {agent_type} to {zone}")



# supply_agent = Agent(
#     name="coordinator_agent",
#     model="gemini-2.0-flash",
#     description="An agent that tells nerdy jokes about various topics.",
#     instruction="""
    
#     you should delegate the task to the manager agent.
#     """,
#     tools=[],

# )



