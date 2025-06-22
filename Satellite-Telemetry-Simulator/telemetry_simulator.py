import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import csv
import os
from datetime import datetime

# Ensure folders exist
os.makedirs("data", exist_ok=True)
os.makedirs("plots", exist_ok=True)

# File for logging
csv_filename = "data/telemetry_log.csv"
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Battery_Level", "Temperature", "Signal_Strength", "Altitude", "Solar_Output"])

# Data storage
time_data = []
battery_data = []
temp_data = []
signal_data = []
altitude_data = []
solar_output_data = []

def generate_telemetry():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    battery = max(0, min(100, 100 - len(time_data) * 0.1 + random.uniform(-1, 1)))
    temp = random.uniform(25, 75)
    signal = random.randint(1, 5)
    altitude = random.uniform(300, 1000)
    solar = random.uniform(100, 900)

    # Alerts
    if battery < 20:
        print(f"[WARNING] Battery low at {battery:.2f}% - {timestamp}")
    if temp > 70:
        print(f"[ALERT] High Temperature: {temp:.2f}°C - {timestamp}")

    # Append
    time_data.append(timestamp)
    battery_data.append(battery)
    temp_data.append(temp)
    signal_data.append(signal)
    altitude_data.append(altitude)
    solar_output_data.append(solar)

    # Log
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, battery, temp, signal, altitude, solar])

# Plot setup
fig, axs = plt.subplots(5, 1, figsize=(10, 14))
plt.subplots_adjust(hspace=0.6)

def animate(i):
    if len(time_data) > 100:
        for arr in [time_data, battery_data, temp_data, signal_data, altitude_data, solar_output_data]:
            arr.pop(0)
    generate_telemetry()

    labels = [
        ("Battery Level (%)", battery_data, 'blue'),
        ("Temperature (°C)", temp_data, 'red'),
        ("Solar Output (W)", solar_output_data, 'green'),
        ("Signal Strength (bars)", signal_data, 'purple'),
        ("Altitude (km)", altitude_data, 'orange')
    ]

    for ax, (title, data, color) in zip(axs, labels):
        ax.cla()
        ax.plot(time_data, data, label=title, color=color)
        ax.set_title(title)
        ax.tick_params(axis='x', rotation=45)
        ax.legend(loc='upper right')
        ax.grid(True)

    # Save snapshot every 30 frames (~30 sec)
    if i % 30 == 0:
        fig.savefig("plots/live_plot.png")

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
