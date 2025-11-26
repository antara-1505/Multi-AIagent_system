import random, json

def generate_zones(n=10):
    zones = []
    for i in range(n):
        zones.append({
            "zone": f"Zone {chr(65+i)}",
            "coordinates": [round(random.uniform(18.0, 28.0), 4), round(random.uniform(72.0, 88.0), 4)],
            "route_status": random.choice(["BLOCKED", "CONGESTED", "CLEAR"]),
            "osm_flooded": random.choice([True, False]),
            "rainfall_mm": random.randint(10, 200)
        })
    with open("data/simulated_disaster_data.json", "w") as f:
        json.dump(zones, f, indent=2)



generate_zones()