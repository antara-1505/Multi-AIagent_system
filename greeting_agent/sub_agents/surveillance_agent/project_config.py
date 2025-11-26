# project_config.py

import os

# Google Cloud project ID
PROJECT_ID = os.getenv("PROJECT_ID", "multi-ai-agent-system-463413")

# Pub/Sub Topics
TOPIC_HAZARD_ALERTS = "hazard-alerts"
TOPIC_TASK_ASSIGNMENTS = "task-assignments"
TOPIC_COMMS_REQUESTS = "comms-requests"

# Firestore Collections
FIRESTORE_MISSIONS_COLLECTION = "missions"
FIRESTORE_INVENTORY_COLLECTION = "inventory"

# Default Coordinates (for testing/demo)
DEFAULT_LOCATION = {
    "lat": 22.5726,
    "lng": 88.3639  # Kolkata, for example
}