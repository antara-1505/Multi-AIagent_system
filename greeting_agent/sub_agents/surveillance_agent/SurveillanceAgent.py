import requests
import json
import time
from google.cloud import pubsub_v1
from project_config import PROJECT_ID
class SurveillanceAgent:
    def __init__(self, dataset_path="data/simulated_disaster_data.json"):
        self.publisher = pubsub_v1.PublisherClient()
        self.dataset_path = dataset_path
        print("SurveillanceAgent initialized")

    def publish_alert(self, zone, risk_type, details):
        print(f"Attempting to publish alert: {zone}, {risk_type}, {details}")
        topic_path = self.publisher.topic_path(PROJECT_ID, 'hazard-alerts')
        message = {
            "zone": zone,
            "type": risk_type,
            "details": details,
            "timestamp": time.time()
        }
        future = self.publisher.publish(topic_path, json.dumps(message).encode("utf-8"))
        print(f"Published message ID: {future.result()}")

    def run(self):
        print(f"Running SurveillanceAgent with dataset: {self.dataset_path}")
        with open(self.dataset_path, "r") as f:
            zones = json.load(f)

        for zon in zones:
            print(f"Checking zone: {zon['zone']}")
            if zon["route_status"] == "BLOCKED":
                self.publish_alert(zon["zone"], "Road Blocked", "Simulated road blockage")

            if zon["osm_flooded"]:
                self.publish_alert(zon["zone"], "Flooded Road (OSM)", "Simulated from OSM tags")

            if zon["rainfall_mm"] > 100:
                self.publish_alert(zon["zone"], "Heavy Rain Risk", f"Simulated rainfall: {zon['rainfall_mm']}mm")

# class SurveillanceAgent:
#     def __init__(self, dataset_path="data/simulated_disaster_data.json"):
#         self.publisher = pubsub_v1.PublisherClient()
#         self.dataset_path = dataset_path
#         print("SurveillanceAgent initialized")
   
#     def publish_alert(self, zone, risk_type, details):
#         topic_path = self.publisher.topic_path(PROJECT_ID, 'hazard-alerts')
#         message = {
#             "zone": zone,
#             "type": risk_type,
#             "details": details,
#             "timestamp": time.time()
#         }
#         self.publisher.publish(topic_path, json.dumps(message).encode("utf-8"))
#         print(f"[ALERT] {zone} - {risk_type} | {details}")
#         print(f"Publishing alert: {message}")
    
#     def monitor_routes(watchlist, publish_alert):
#         for zone in watchlist:
#             response = requests.get(f"https://maps.googleapis.com/maps/api/directions/json?origin={zone['start']}&destination={zone['end']}&departure_time=now&key=AIzaSyCjhYl7kOIB1g0NBfXefNPf_vm8zmYUY1Y")
#             data = response.json()
#             if data['status'] != 'OK' or 'warnings' in data['routes'][0]:
#                 publish_alert(zone, "Potential Road Blockage")

#     def run(self):
#         with open(self.dataset_path, "r") as f:
#             zones = json.load(f)

#         for zon in zones:
#             if zon["route_status"] == "BLOCKED":
#                 self.publish_alert(zon["zone"], "Road Blocked", "Simulated road blockage")

#             if zon["osm_flooded"]:
#                 self.publish_alert(zon["zone"], "Flooded Road (OSM)", "Simulated from OSM tags")

#             if zon["rainfall_mm"] > 100:
#                 self.publish_alert(zon["zone"], "Heavy Rain Risk", f"Simulated rainfall: {zon['rainfall_mm']}mm")


#     # def run(self):
#     #     print("SurveillanceAgent is running")
# # def get_supply(self):
# #     return 0
# from google.adk.agents import Agent
# from google.adk.tools.tool_context import ToolContext

# # supply_agent = Agent(
# #     name="surveillance_agent",
# #     model="gemini-2.0-flash",
# #     description="An agent that tells nerdy jokes about various topics.",
# #     instruction="""
# #     you should delegate the task to the manager agent.
# #     """,
# #     tools=[],

# # )