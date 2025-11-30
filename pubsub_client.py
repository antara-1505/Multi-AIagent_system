import os
import json
from google.cloud import pubsub_v1

PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "multi-ai-agent-system-463413")

publisher = pubsub_v1.PublisherClient()

def publish_message(topic_name: str, message: dict):
    """
    Publish a JSON-serializable dict to a Pub/Sub topic.
    """
    topic_path = publisher.topic_path(PROJECT_ID, topic_name)
    data = json.dumps(message).encode("utf-8")
    future = publisher.publish(topic_path, data=data)
    # Optional: future.result() if you want to block
    print(f"[PUB] topic={topic_name} message={message}")
    return future