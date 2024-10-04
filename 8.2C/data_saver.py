import sys
import traceback
from arduino_iot_cloud import ArduinoCloudClient
import datetime
import pandas as pd
import asyncio
import os

# File to save the accelerometer data
csv_file = "new_accelerometer_data.csv"  # Updated CSV file name

# Device credentials
DEVICE_ID = "808282cb-d11a-456f-9ce3-e1601ea260a1"
SECRET_KEY = "d?16c!4EYQJt1Mv77DEh4y8fk"

# Buffer to store the latest X, Y, Z values
buffer = {'x': None, 'y': None, 'z': None}

# Add delay between updates (in seconds)
update_delay = 5  # Delay of 5 seconds between each update

def save_to_csv(x, y, z):
    """Save the incoming X, Y, Z data to a CSV file."""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_data = pd.DataFrame([[timestamp, x, y, z]], columns=['timestamp', 'x', 'y', 'z'])

    try:
        if not os.path.isfile(csv_file):
            new_data.to_csv(csv_file, mode='a', header=True, index=False)
        else:
            new_data.to_csv(csv_file, mode='a', header=False, index=False)
        print(f"Saved data to CSV: X={x}, Y={y}, Z={z} at {timestamp}")
    except PermissionError as e:
        print(f"Permission Error: {e}. Retrying in a moment...")

def check_and_save():
    """Check if all X, Y, Z values are present in the buffer and save them to the CSV file."""
    if buffer['x'] is not None and buffer['y'] is not None and buffer['z'] is not None:
        save_to_csv(buffer['x'], buffer['y'], buffer['z'])
        # Reset the buffer after saving
        buffer['x'], buffer['y'], buffer['z'] = None, None, None

def on_py_x_change(client, value):
    buffer['x'] = value
    check_and_save()

def on_py_y_change(client, value):
    buffer['y'] = value
    check_and_save()

def on_py_z_change(client, value):
    buffer['z'] = value
    check_and_save()

async def run_client():
    """Runs the Arduino IoT Cloud client and handles reconnection logic with delays."""
    retry_count = 0
    max_retries = 5  # Maximum retries before waiting longer

    while True:
        try:
            # Create the client instance
            client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)
            
            # Register the callbacks for each axis
            client.register("py_x", value=None, on_write=on_py_x_change)
            client.register("py_y", value=None, on_write=on_py_y_change)
            client.register("py_z", value=None, on_write=on_py_z_change)

            print("Attempting to connect to Arduino IoT Cloud...")
            await client.run(interval=120, backoff=15)  # Keep the connection active

        except Exception as e:
            print(f"Connection error: {e}")
            retry_count += 1
            if retry_count > max_retries:
                print(f"Max retries reached. Pausing for 5 minutes before trying again...")
                retry_count = 0
                await asyncio.sleep(300)  # Wait for 5 minutes after multiple failed attempts
            else:
                print(f"Retrying connection in 15 seconds...")
                await asyncio.sleep(15)  # Wait 15 seconds between retries to avoid rapid reconnections

        # Add a delay before checking for the next update
        await asyncio.sleep(update_delay)

if __name__ == "__main__":
    asyncio.run(run_client())
