import websocket
import json
import time

# UPDATE THIS ID to match the delivery you see in your logs (e.g., 57)
DELIVERY_ID = "58"
ws_url = f"ws://127.0.0.1:8000/ws/tracking/{DELIVERY_ID}/"


def simulate_movement():
    try:
        print(f"Connecting to: {ws_url}")
        ws = websocket.create_connection(ws_url)
        print(f"✅ Connected! Simulating movement for Delivery #{DELIVERY_ID}...")

        # Starting point (Near KNUST)
        start_lat, start_lng = 6.6745, -1.5715
        # Target point (Destination)
        dest_lat, dest_lng = 6.6885, -1.6015

        steps = 15
        for i in range(steps + 1):
            # Calculate the next step's coordinates
            current_lat = start_lat + (dest_lat - start_lat) * (i / steps)
            current_lng = start_lng + (dest_lng - start_lng) * (i / steps)

            payload = {
                "lat": current_lat,
                "lng": current_lng
            }

            ws.send(json.dumps(payload))
            print(f"📍 Step {i}/{steps}: Sent Lat {current_lat:.4f}, Lng {current_lng:.4f}")
            time.sleep(1.5)  # Move every 1.5 seconds

        ws.close()
        print("🏁 Simulation finished!")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    simulate_movement()