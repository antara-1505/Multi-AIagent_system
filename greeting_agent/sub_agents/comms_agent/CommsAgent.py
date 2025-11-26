import json
import time

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:/VSCode/GoogleADK/config/multi-ai-agent-system-463413-c47d52cb8ac2.json"
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from google.cloud import pubsub_v1
from project_config import PROJECT_ID
from flask import Flask, request, jsonify
from google.cloud import pubsub_v1

app = Flask(__name__)
publisher = pubsub_v1.PublisherClient()

def publish_request(message):
    topic_path = publisher.topic_path(PROJECT_ID, 'comms-requests')
    publisher.publish(topic_path, json.dumps(message).encode('utf-8'))
    print(f"[Comms Alert Published] {message}")

@app.route("/sos", methods=["POST"])
def receive_sos():
    data = request.json
    if not data or 'zone' not in data or 'message' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    comms_msg = {
        "zone": data['zone'],
        "message": data['message'],
        "source": "CIVILIAN_REPORT",
        "timestamp": time.time()
    }

    publish_request(comms_msg)
    return jsonify({"status": "SOS sent"}), 200

@app.route("/status", methods=["GET"])
def health_check():
    return "CommsAgent is running.", 200

# supply_agent = Agent(
#     name="comms_agent",
#     model="gemini-2.0-flash",
#     description="An agent that tells nerdy jokes about various topics.",
#     instruction="""
#     You are the eye of the system, you detects environmental changes and identifies risk zones. 
#     If any risks are found you send alert to the coordinator_agent.
    
#     you should delegate the task to the manager agent.
#     """,
#     tools=[],
# )