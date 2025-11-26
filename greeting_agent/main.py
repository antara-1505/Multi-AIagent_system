import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:/VSCode/GoogleADK/greeting_agent/config/multi-ai-agent-system-463413-c47d52cb8ac2.json"

from sub_agents.surveillance_agent.SurveillanceAgent import SurveillanceAgent
from sub_agents.coordinator_agent import CoordinatorAgent
from sub_agents.rescue_agent import RescueAgent
from sub_agents.supply_agent import SupplyAgent
from sub_agents.comms_agent import CommsAgent

import os
from flask import Flask, request, jsonify

# def run_all_agents():
#     SurveillanceAgent().run()
#     CoordinatorAgent().listen()
#     RescueAgent().listen()
#     SupplyAgent().listen()
#     CommsAgent().listen()

app = Flask(__name__)
@app.route('/surveillance', methods=['POST'])
def surveillance_handler():
    return SurveillanceAgent.handle_request()

@app.route('/coordinator', methods=['POST'])
def coordinator_handler():
    return CoordinatorAgent.handle_request()

@app.route('/rescue', methods=['POST'])
def rescue_handler():
    return RescueAgent.handle_request(request)

@app.route('/supply', methods=['POST'])
def supply_handler():
    return SupplyAgent.handle_request(request)

@app.route('/comms', methods=['POST'])
def comms_handler():
    return CommsAgent.handle_request(request)

@app.route('/health', methods=['GET'])
def health_check():
    print("Disaster response agent is running")
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    # run_all_agents()
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
