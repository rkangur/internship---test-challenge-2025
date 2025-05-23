import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Parameters
meeting_time = datetime.strptime("09:05:00", "%H:%M:%S")
walk_to_zoo = timedelta(seconds=300)
walk_from_toompark = timedelta(seconds=240)
bus_ride_mean = timedelta(minutes=15)
bus_ride_std = timedelta(minutes=2)

# Simulate a schedule: Bus 8 comes every ~8 minutes from 07:00 to 09:00
def generate_bus_schedule(start="07:00", end="09:00", interval=8):
    times = []
    t = datetime.strptime(start, "%H:%M")
    end_t = datetime.strptime(end, "%H:%M")
    while t <= end_t:
        times.append(t)
        t += timedelta(minutes=interval + np.random.normal(0, 0.5))  # slight jitter
    return times

# Find the next bus after arrival at Zoo
def get_next_bus(zoo_arrival, bus_schedule):
    for bus_time in bus_schedule:
        if bus_time >= zoo_arrival:
            return bus_time
    return None  # No bus available

# Run a single commute simulation
def simulate_commute(leave_time_str, bus_schedule):
    leave_time = datetime.strptime(leave_time_str, "%H:%M")
    zoo_arrival = leave_time + walk_to_zoo
    bus_depart = get_next_bus(zoo_arrival, bus_schedule)
    if bus_depart is None:
        return True  # Missed all buses → late

    # Add stochastic ride time
    ride_time = bus_ride_mean + timedelta(seconds=np.random.normal(0, bus_ride_std.total_seconds()))
    toompark_arrival = bus_depart + ride_time
    meeting_arrival = toompark_arrival + walk_from_toompark

    return meeting_arrival > meeting_time  # True if late

# Simulate lateness probability over a range of home departure times
def simulate_over_range(start="07:30", end="08:45", step_minutes=1, simulations_per_time=100):
    bus_schedule = generate_bus_schedule()
    times = []
    probs = []

    current_time = datetime.strptime(start, "%H:%M")
    end_time = datetime.strptime(end, "%H:%M")

    while current_time <= end_time:
        leave_str = current_time.strftime("%H:%M")
        late_count = sum(simulate_commute(leave_str, bus_schedule) for _ in range(simulations_per_time))
        prob_late = late_count / simulations_per_time
        times.append(leave_str)
        probs.append(prob_late)
        current_time += timedelta(minutes=step_minutes)

    return times, probs

# Plotting
def plot_results(times, probs):
    plt.figure(figsize=(14, 7))
    plt.plot(times, probs, marker='o')
    plt.xticks(rotation=45)
    plt.xlabel("Time Leaving Home")
    plt.ylabel("Probability of Being Late")
    plt.title("Probability of Rita Being Late vs. Home Departure Time")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Main
if __name__ == "__main__":
    times, probs = simulate_over_range()
    plot_results(times, probs)
