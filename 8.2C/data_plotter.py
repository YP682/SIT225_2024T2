import pandas as pd
import numpy as np
from dash import Dash, dcc, html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import os

# File from which to read accelerometer data
csv_file = "new_accelerometer_data.csv"  # Updated CSV file name

# Initialize Dash App
app = Dash(__name__)

# Dash Layout
app.layout = html.Div([
    dcc.Graph(id='live-graph'),
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0)  # Update every second
])

def smooth_data(data, window_size=5):
    """Applies a simple moving average to smooth data."""
    if len(data) < window_size:
        print(f"Not enough data to smooth. Showing raw data (data size = {len(data)}).")
        return data  # Return raw data if not enough for smoothing
    return np.convolve(data, np.ones(window_size) / window_size, mode='valid')

def get_data_from_csv():
    """Reads data from the CSV file and returns X, Y, Z data."""
    if not os.path.isfile(csv_file):
        print("CSV file not found.")
        return [], [], [], []

    try:
        df = pd.read_csv(csv_file)
        if df.empty:
            print("CSV file is empty.")
            return [], [], [], []

        # Check if the required columns are present in the CSV
        if 'x' not in df.columns or 'y' not in df.columns or 'z' not in df.columns:
            print(f"Required columns 'x', 'y', or 'z' not found in the CSV file.")
            return [], [], [], []

        # Smooth data or return raw data if not enough points
        smoothed_x = smooth_data(df['x'].values, window_size=5)
        smoothed_y = smooth_data(df['y'].values, window_size=5)
        smoothed_z = smooth_data(df['z'].values, window_size=5)

        # Get the timestamps corresponding to the smoothed data
        timestamps = df['timestamp'][-len(smoothed_x):].values

        return timestamps, smoothed_x, smoothed_y, smoothed_z
    except Exception as e:
        print(f"Error reading or processing CSV data: {e}")
        return [], [], [], []

@app.callback(Output('live-graph', 'figure'), Input('interval-component', 'n_intervals'))
def update_graph(n):
    """Updates the live graph with new data every second."""
    print(f"Graph update triggered, interval count: {n}")
    
    fig = go.Figure()

    # Fetch data from the CSV
    timestamps, smoothed_x, smoothed_y, smoothed_z = get_data_from_csv()

    # Plot data only if we have timestamps
    if len(timestamps) > 0:
        fig.add_trace(go.Scatter(x=timestamps, y=smoothed_x, mode='lines', name='X-axis'))
        fig.add_trace(go.Scatter(x=timestamps, y=smoothed_y, mode='lines', name='Y-axis'))
        fig.add_trace(go.Scatter(x=timestamps, y=smoothed_z, mode='lines', name='Z-axis'))
    else:
        print("No data to plot.")

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
