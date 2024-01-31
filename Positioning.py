import time
from BMI160_i2c import Driver
import numpy as np
import quaternion
import matplotlib
matplotlib.use('Agg')  # Set the Agg backend
import matplotlib.pyplot as plt

initial_position = np.array([0.0, 0.0, 0.0])  # Initial position (x, y, z)
velocity = np.array([0.0, 0.0, 0.0])  # Initial velocity (x, y, z)
orientation = quaternion.quaternion(1.0, 0.0, 0.0, 0.0)
# Constants for sensor fusion
accelerometer_weight = 0.98  # Weight for accelerometer data
gyroscope_weight = 0.02  # Weight for gyroscope data
x_positions = []
y_positions = []
z_positions = []
# Sample time (time interval between sensor readings)
dt = 0.01
print('Trying to initialize the sensor...')
sensor = Driver(0x68) # change address if needed
print('Initialization done')
# Loop to simulate sensor data (replace with actual data acquisition)
for _ in range(1000):
    # Simulated accelerometer data (acceleration in m/s^2)
    data = sensor.getMotion6()
    accelerometer_data = np.array([data[0], data[1], data[2]])  # Example accelerometer data (including gravity)

    # Simulated gyroscope data (angular rate in radians per second)
    gyroscope_data = quaternion.quaternion(0.1, data[3], data[4], data[5])  # Example gyroscope data

    # Calculate orientation change from gyroscope data
    orientation_change = 0.5 * orientation * gyroscope_data * dt

    # Update the orientation using quaternion integration
    orientation += orientation_change

    # Rotate the accelerometer data to the global frame using the current orientation
    rotated_accelerometer_data = (orientation * quaternion.quaternion(0, *accelerometer_data) * orientation.conjugate()).vec

    # Integrate acceleration to update velocity
    velocity += rotated_accelerometer_data * dt

    # Integrate velocity to update position
    initial_position += velocity * dt

    # Append position data to lists for plotting
    x_positions.append(initial_position[0])
    y_positions.append(initial_position[1])
    z_positions.append(initial_position[2])
    time.sleep(dt)
time_values = np.arange(0, 1000 * dt, dt)

# Plot position data

plt.figure(figsize=(8, 6))
plt.plot(x_positions, y_positions, label='XY Trajectory')
plt.xlabel('X Position (meters)')
plt.ylabel('Y Position (meters)')
plt.title('XY Trajectory')
plt.grid(True)
plt.legend()
plt.show()
# Save the plot as an image (e.g., PNG)
plt.savefig('position_plot.png')
