import os
import logging
from time import time

from radariq.RadarIQ import RadarIQ, MODE_POINT_CLOUD, OUTPUT_LIST
from radariq import port_manager as pm

connected = False  # Connection Status of Device
riq = None

# Logging
FORMAT = '%(asctime)-15s %(message)'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('RadarIQ')
logger.setLevel(logging.INFO)


def calculate_distance(data):
    """
    Processes the points data to find average
    """
    distances = []
    for frame in data:
        max_point = [0, 0, 0, 0]
        for point in frame:
            if point[3] > max_point[3]:  # look for max intensity
                max_point = point
        distances.append(max_point[1])  # Y value
    return sum(distances) / len(distances)


def capture():
    """
    Captures distance data using RadarIQ object based on the parameters gathered from the UI.
    """
    global riq
    try:
        riq.stop()
        riq.set_mode(MODE_POINT_CLOUD)
        riq.set_units('mm', 'mm/s')
        riq.set_frame_rate(20)
        riq.set_distance_filter(100, 10000)
        riq.set_angle_filter(-30, 30)
        riq.set_height_filter(-5000, 5000)
        riq.start(100)  # capture 100 frames then stop

        data = []
        for frame in riq.get_data():
            if frame is not None:
                data.append(frame)

        return data

    except Exception as error:
        print(error)


def connect_riq():
    """
    Connects program to RadarIQ device and returns a RadarIQ object.
    """
    global riq
    try:
        riq = RadarIQ()
        return True

    except Exception as error:
        print(error)
        return False


def display_distance(average):
    print(f"Average Distance: {average}")


def measure():
    global riq
    connect_riq()
    data = capture()
    distance = calculate_distance(data)
    display_distance(distance)
    riq.close()


if __name__ == '__main__':
    print("Please note, this is an approximate distance only. The point cloud mode of radar is not specifically designed for accurate distance measurement.")
    print("Please review the distance products at https://radariq.io for models which are designed for distance measurement.")
    print("Measurement error may be as high as 40mm in this mode.")
    print("")
    print('Taking 100 samples over 5 seconds...')
    print('')
    measure()

