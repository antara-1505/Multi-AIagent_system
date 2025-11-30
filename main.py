import os
import base64
import json
from flask import Flask, request, jsonify

from pubsub_client import publish_message
from greeting_agent.handler import handle_greeting  # you'll create this

app = Flask(__name__)

@app.route("/")
def health():
    return "Disaster Response Agent is running!"

@app.route("/pubsub", methods=["POST"])
def pubsub_handler():
    """
    Endpoint for Pub/Sub push subscriptions.
    Cloud Run trigger should point here.
    """
    envelope = request.get_json()
    if not envelope:
        return "Bad Request: no JSON", 400

    # Standard Pub/Sub push format
    if "message" not in envelope:
        return "Bad Request: no message field", 400

    msg = envelope["message"]
    data = {}

    if "data" in msg:
        payload = base64.b64decode(msg["data"]).decode("utf-8")
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            data = {"raw": payload}

    attributes = msg.get("attributes", {}) or {}

    # Simple routing example
    agent_type = attributes.get("agent") or data.get("agent")

    if agent_type == "greeting":
        handle_greeting(data)
    # elif agent_type == "rescue": ...
    # elif agent_type == "food": ...
    else:
        print(f"[WARN] Unknown/unspecified agent_type: {agent_type}, data={data}")

    return "", 204  # Pub/Sub expects 2xx

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
