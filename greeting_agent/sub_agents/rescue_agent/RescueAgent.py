from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

import base64
import json
import time
from flask import Flask, request
from google.cloud import firestore
import requests

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:/VSCode/GoogleADK/config/multi-ai-agent-system-463413-c47d52cb8ac2.json"

app = Flask(__name__)
db = firestore.Client()

GOOGLE_MAPS_API_KEY = "AIzaSyCjhYl7kOIB1g0NBfXefNPf_vm8zmYUY1Y"

@app.route("/", methods=["POST"])
def handle_task():
    envelope = request.get_json()
    if not envelope or "message" not in envelope:
        return "Invalid Pub/Sub message", 400

    message = envelope["message"]
    payload = base64.b64decode(message["data"]).decode("utf-8")
    task = json.loads(payload)

    print(f"[Rescue Task Received] {task}")

    if task.get("agent") != "Rescue":
        return "Ignored - Not a Rescue Task", 200

    zone = task["zone"]
    simulate_rescue_mission(zone)

    return "OK", 200

def simulate_rescue_mission(zone):
    # Example origin and destination for simulation
    origin = "22.5726,88.3639"  # Kolkata center
    destination = "22.57,88.36"  # Simulated zone (replace with actual from Firestore if needed)

    # Use Google Maps Directions API to simulate routing
    response = requests.get(
        "https://maps.googleapis.com/maps/api/directions/json",
        params={
            "origin": origin,
            "destination": destination,
            "departure_time": "now",
            "key": GOOGLE_MAPS_API_KEY
        }
    )
    data = response.json()
    duration = "Unknown"
    if data.get("routes"):
        duration = data["routes"][0]["legs"][0]["duration"]["text"]

    # Save mission progress to Firestore
    db.collection("missions").add({
        "zone": zone,
        "type": "Rescue",
        "status": "Completed",
        "eta": duration,
        "timestamp": time.time()
    })

    print(f"[Rescue Completed] Zone: {zone}, ETA: {duration}")

# supply_agent = Agent(
#     name="rescue_agent",
#     model="gemini-2.0-flash",
#     description="An agent that tells nerdy jokes about various topics.",
#     instruction="""
    
#     you should delegate the task to the manager agent.
#     """,
#     tools=[],
# )