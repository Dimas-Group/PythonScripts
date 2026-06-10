import sys
import datetime
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import FuncFormatter
import numpy as np
from typing import TYPE_CHECKING

# --- Type Hinting ---
if TYPE_CHECKING:
    from attollo_camera_toolbox import AttolloCamera

# --- Configuration ---
UPDATE_INTERVAL_MS = 1000  # How often to fetch data (in milliseconds)
HISTORY_POINTS = 1000       # How many data points to show on the graph

# --- Global Data Storage ---
# 'times' will now store seconds elapsed (floats), not datetime objects
times = []
temp_data = [[], [], [], []] 
part_labels = ["DETECTOR", "FPGA_JUNCTION", "DETECTOR_BOARD", "PROCESSOR_BOARD"]

# We need a variable to track when the connection started
start_time = None 

# --- Plot Setup ---
fig, ax = plt.subplots(figsize=(12, 7))
lines = []
for i, label in enumerate(part_labels):
    line, = ax.plot([], [], label=label, marker='o', markersize=3)
    lines.append(line)

ax.legend(loc='best')
ax.set_title("Attollo Camera - Temperature")
ax.set_xlabel("Time Elapsed (HH:MM:SS)")
ax.set_ylabel("Temperature (°C)")

# This function converts x-axis values (seconds) into "HH:MM:SS" strings
def format_time_elapsed(x, pos):
    return time.strftime('%H:%M:%S', time.gmtime(x))

ax.xaxis.set_major_formatter(FuncFormatter(format_time_elapsed))

ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=10))

plt.tight_layout()

# --- Animation Update Function ---
def update_plot(frame, cam_instance):
    global times, temp_data, start_time
    
    try:
        # 1. Fetch new data
        new_temps = cam_instance.return_temp() 

        if new_temps is None or len(new_temps) != 4:
            print("Warning: Received invalid data from return_temp()")
            return lines

        # 2. Calculate Time Elapsed
        # If this is the very first data point, set the start timer
        if start_time is None:
            start_time = datetime.datetime.now()
            
        current_time_abs = datetime.datetime.now()
        # Calculate difference in seconds
        time_diff = (current_time_abs - start_time).total_seconds()
        
        times.append(time_diff)

        # 3. Append new data to our history lists
        for i, temp in enumerate(new_temps):
            temp_data[i].append(temp)
        
        # 4. Prune old data
        times = times[-HISTORY_POINTS:]
        for i in range(4):
            temp_data[i] = temp_data[i][-HISTORY_POINTS:]
        
        # 5. Update the plot lines with new data
        for i, line in enumerate(lines):
            line.set_data(times, temp_data[i])

        # 6. Rescale the axes
        ax.relim()
        ax.autoscale_view()
        
        # We don't need autofmt_xdate anymore because we aren't using Date objects
        # But we can rotate labels if they get crowded
        plt.setp(ax.get_xticklabels(), rotation=0)

        return lines

    except (AttributeError, RuntimeError, TypeError) as e:
        if "object" in str(e).lower() or "port" in str(e).lower() or "NoneType" in str(e):
             print("Camera error (port closed or object deleted). Stopping plot.")
             plt.close(fig)
        else:
            print(f"Error during plot update: {e}")
        
        plt.close(fig) 
        return []

# --- Main Launch Function ---
def start_temperature_plot(cam_instance: 'AttolloCamera'):
    """
    Initializes and displays the non-blocking temperature plot.
    """
    global start_time, times, temp_data
    
    print("Initializing animation...")
    
    # Reset data on new start so the graph starts at 00:00:00
    start_time = None
    times = []
    temp_data = [[], [], [], []]
    
    # 2. Create Animation
    ani = animation.FuncAnimation(
        fig,
        update_plot,
        fargs=(cam_instance,),
        interval=UPDATE_INTERVAL_MS,
        # IMPORTANT: blit=False is required if the Axis limits are changing!
        # If blit=True, the axis labels will NOT update/scroll.
        blit=False, 
        cache_frame_data=False
    )

    plt.show()
    return ani