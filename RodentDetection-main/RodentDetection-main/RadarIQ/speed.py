"""
This sample application records the speed in the X direction of the first detected object from the RadarIQ sensor
"""
import time
import tkinter as tk
import tkinter.font as tkFont
import threading
from radariq import RadarIQ, MODE_OBJECT_TRACKING, OUTPUT_LIST, find_com_port

RADAR_BLUE = "#0033A0"
FRAME_RATE = 3  # frames per second
MIN_DISTANCE = 0.5  # Closest distance to look (m)
MAX_DISTANCE = 10  # Furthermost distance to look (m)
MIN_ANGLE = -45  # Minimum angle to look
MAX_ANGLE = 45  # Maximum angle to look
AVERAGING_PERIOD = 10  # number of seconds to run the averaging/max filter
UNITS = "m/s"
MINIMUM_SPEED = 0.5  # Minimum speed


class SpeedMeasurement():
    def __init__(self):
        self.riq = None
        self.window = tk.Tk()
        self.window.title("Speed Measurement")
        self.window.geometry('900x200')
        self.window.configure(bg=RADAR_BLUE)
        large_font = tkFont.Font(family="TkDefaultFont", size=20)

        large_font.configure(size=100)
        small_font = tkFont.nametofont("TkDefaultFont")
        small_font.configure(size=20)
        self.speedLabel = tk.Label(text=f"0 {UNITS}", font=large_font, fg="white", bg=RADAR_BLUE)
        self.maxSpeedLabel = tk.Label(text=f"Max speed: 0 {UNITS}", font=small_font, anchor=tk.NW, fg="white",
                                      bg=RADAR_BLUE)
        self.speedLabel.pack()
        self.maxSpeedLabel.pack()

        self.speedBuffer = CircularList(FRAME_RATE * AVERAGING_PERIOD)
        self.setup_radariq()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.run_thread = False
        self.window.mainloop()

    def on_closing(self):
        self.run_thread = False
        self.riq.close()
        self.window.destroy()

    def setup_radariq(self):
        """
        Setup the RadarIQ module.
        """
        self.run_thread = True
        x = threading.Thread(target=self.run_radar)
        x.start()

    def run_radar(self):
        try:
            port = find_com_port()
            self.riq = RadarIQ(port.device, output_format=OUTPUT_LIST)
            self.riq.set_mode(MODE_OBJECT_TRACKING)
            self.riq.set_units('m', UNITS)
            self.riq.set_frame_rate(FRAME_RATE)
            self.riq.set_distance_filter(MIN_DISTANCE, MAX_DISTANCE)
            self.riq.set_angle_filter(MIN_ANGLE, MAX_ANGLE)
            self.riq.start()

            for frame in self.riq.get_data():
                if frame is not None and len(frame) > 0:
                    speed = frame[0]['x_vel']
                    self.speedBuffer.append(speed)
                    if speed > MINIMUM_SPEED:
                        self.speedLabel.configure(text=f"{speed} {UNITS}")
                    else:
                        self.speedLabel.configure(text=f"- {UNITS}")

                    max_speed = self.speedBuffer.max()
                    if max_speed > MINIMUM_SPEED:
                        self.maxSpeedLabel.configure(text=f"Max speed: {max_speed} {UNITS}")
                    else:
                        self.maxSpeedLabel.configure(text=f"- {UNITS}")
                    time.sleep(0.01)  # release control of the loop to the rest of the program

        except Exception as error:
            print(error)


class CircularList:
    """
    Circular buffer of values
    """

    def __init__(self, size):
        self.index = 0
        self.size = size
        self._data = list()[-size:]

    def append(self, value):
        if len(self._data) == self.size:
            self._data[self.index] = value
        else:
            self._data.append(value)
        self.index = (self.index + 1) % self.size

    def max(self):
        return max(self._data)

    def average(self):
        return sum(self._data) / self.size


if __name__ == '__main__':
    speedy = SpeedMeasurement()
