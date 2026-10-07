import matplotlib.pyplot as plt
from pid_template import make_car
from pid_template import update
from pid_template import calculate_desired_acceleration
from pid_template import acceleration_to_throttle_percentage

K_P = 0.5
K_I = 0.1
K_D = 0.1
 
STEPS = 550
 
car = make_car(desired_v=30.0, dt=0.1)

# Set up lists to hold the history of velocity, error, and time for plotting
velocity_history = []
error_history = []
time_history = []

# Run the simulation for a set number of steps
for _ in range(STEPS):

    #calculate the desired acceleration and error
    desired_acceleration, error = calculate_desired_acceleration(
        car, K_P, K_I, K_D
    )

    # convert the desired acceleration to throttle percentage
    throttle_percentage = acceleration_to_throttle_percentage(
        desired_acceleration
    )

    # update velocity, position, and time based on throttle percentage
    update(car, throttle_percentage)
    velocity_history.append(car["v"])
    error_history.append(error)
    time_history.append(car["t"])

# plot the results
plt.figure()
plt.plot(time_history, velocity_history)

plt.title("Velocity vs Time")
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")

# display the velocity graph
plt.show()

# create a second graph showing the velocity error over time
plt.figure()
plt.plot(time_history, error_history)

plt.title("Velocity Error vs Time")
plt.xlabel("Time (s)")
plt.ylabel("Velocity Error (m/s)")

# display the error graph
plt.show()