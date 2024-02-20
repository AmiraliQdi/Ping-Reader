# import Ping360 class
import numpy as np
from brping import Ping360

# Create Ping360 instance
p = Ping360()

# Initialize the Ping360 instance
print("Initialized: %s" % p.initialize())

# Set Ping360 parameters
print(p.set_transmit_frequency(1000))
print(p.set_sample_period(80))
print(p.set_number_of_samples(500))

# Connect to, initialize, and set up Ping360 settings - Missing part in your code

# Open a file for writing responses
with open("ping360_responses.txt", "w") as file:
    # Loop through a full circle, one gradian at a time
    for x in range(400):
        # Transmit ping at the specified angle and get response
        response = p.transmitAngle(x)
        print(response)
        data = np.frombuffer(response.data, dtype=np.uint8)
        print(data.min(), data.max())
        # print all locations that are above threshold
        threshold = 200
        print(np.where(data >= threshold))
        # Write the response data to the file
        file.write(str(response) + "\n")



def getSonarData(sensor, angle):
    """
    Transmits the sonar angle and returns the sonar intensities
    Args:
        sensor (Ping360): Sensor class
        angle (int): Gradian Angle
    Returns:
        list: Intensities from 0 - 255
    """
    sensor.transmitAngle(angle)
    data = bytearray(getattr(sensor, '_data'))
    return [k for k in data]