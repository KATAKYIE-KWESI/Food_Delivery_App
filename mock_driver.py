import websocket
import json
import time

# UPDATE THIS ID to match the delivery you see in your logs
DELIVERY_ID = "60"
ws_url = f"ws://127.0.0.1:8000/ws/tracking/{DELIVERY_ID}/"


def simulate_movement():
    try:
        print(f"Connecting to: {ws_url}")
        ws = websocket.create_connection(ws_url)
        print(f"✅ Connected! Simulating a LONG trip for Delivery #{DELIVERY_ID}...")

        # START: Near Abrepo Junction (Further away)
        start_lat, start_lng = 6.7000, -1.6300

        # DESTINATION: Near KNUST/Ayigya (Your target)
        dest_lat, dest_lng = 6.6745, -1.5715

        # We increase steps to 30 so the movement is smoother over the long distance
        steps = 30
        for i in range(steps + 1):
            # Calculate the next step's coordinates
            current_lat = start_lat + (dest_lat - start_lat) * (i / steps)
            current_lng = start_lng + (dest_lng - start_lng) * (i / steps)

            payload = {
                "lat": current_lat,
                "lng": current_lng
            }

            ws.send(json.dumps(payload))
            # The distance will start at ~10km and count down
            print(f"📍 Step {i}/{steps}: Sent Lat {current_lat:.4f}, Lng {current_lng:.4f}")
            time.sleep(2)  # Wait 2 seconds per update for a natural feel

        ws.close()
        print("🏁 Simulation finished!")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    simulate_movement()