import sys
import traceback
from arduino_iot_cloud import ArduinoCloudClient
import datetime
import pandas as pd
import seaborn as sns
import asyncio

DEVICE_ID = "808282cb-d11a-456f-9ce3-e1601ea260a1"
SECRET_KEY = "d?16c!4EYQJt1Mv77DEh4y8fk"

# Default lists to store data
data_list = []
save_list = []

def add_to_list(value, timestamp, axis):
    global data_list
    global save_list

    # Append the new data point to the list
    data_list.append([timestamp, value, axis])

    # Check if the list has more than 20 data points
    if len(data_list) > 20:
        save_list = data_list.copy()
        data_list.clear()
        save_to_csv(save_list)  # Save the data to a CSV file
        list_to_graph()
        save_list.clear()

def save_to_csv(data):
    # Save the data to a CSV file
    df = pd.DataFrame(data, columns=['timestamp', 'value', 'axis'])
    timestamp_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    csv_file = f'data_{timestamp_str}.csv'
    df.to_csv(csv_file, index=False)
    print(f"Data saved to {csv_file}")
    calculate_stats(csv_file)

def list_to_graph():
    global save_list

    # Create a DataFrame from the saved list
    df = pd.DataFrame(save_list, columns=['timestamp', 'value', 'axis'])
    df = df.sort_values('timestamp').reset_index(drop=True)
    
    # Create and save the graph using seaborn
    fig = sns.lineplot(data=df, x='timestamp', y='value', hue='axis').get_figure()
    timestamp_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    fig.savefig(f'figure_{timestamp_str}.png')
    print(f"New graph saved as figure_{timestamp_str}.png")

def calculate_stats(csv_file):
    # Read the saved CSV file to calculate statistical measures
    df = pd.read_csv(csv_file)
    
    # Separate data for each axis
    df_x = df[df['axis'] == 'x']['value']
    df_y = df[df['axis'] == 'y']['value']
    df_z = df[df['axis'] == 'z']['value']
    
    # Calculate and print statistical measures
    print(f"Mean of X-axis: {df_x.mean()}")
    print(f"Mean of Y-axis: {df_y.mean()}")
    print(f"Mean of Z-axis: {df_z.mean()}")
    
    print(f"Standard Deviation of X-axis: {df_x.std()}")
    print(f"Standard Deviation of Y-axis: {df_y.std()}")
    print(f"Standard Deviation of Z-axis: {df_z.std()}")
    
    # Create a correlation matrix
    df_pivot = df.pivot(index='timestamp', columns='axis', values='value')
    correlation_matrix = df_pivot.corr()
    print("Correlation Matrix:")
    print(correlation_matrix)

def on_py_x_change(client, value):
    timestamp = datetime.datetime.now().strftime('%H%M%S')
    print(f"X-axis: {timestamp}, {value}")
    add_to_list(value, timestamp, 'x')

def on_py_y_change(client, value):
    timestamp = datetime.datetime.now().strftime('%H%M%S')
    print(f"Y-axis: {timestamp}, {value}")
    add_to_list(value, timestamp, 'y')

def on_py_z_change(client, value):
    timestamp = datetime.datetime.now().strftime('%H%M%S')
    print(f"Z-axis: {timestamp}, {value}")
    add_to_list(value, timestamp, 'z')

async def run_client():
    try:
        # Instantiate Arduino cloud client
        client = ArduinoCloudClient(
            device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY
        )

        # Register callbacks for the x, y, z value changes
        client.register("py_x", value=None, on_write=on_py_x_change)
        client.register("py_y", value=None, on_write=on_py_y_change)
        client.register("py_z", value=None, on_write=on_py_z_change)

        # Start the Arduino IoT Cloud client
        await client.run(interval=10, backoff=2)
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

def main():
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            print("Async event loop already running. Adding coroutine to the existing loop.")
            asyncio.ensure_future(run_client())
        else:
            print("Starting a new event loop.")
            loop.run_until_complete(run_client())
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
