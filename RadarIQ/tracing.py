from math import tan, radians
from radariq import RadarIQ, MODE_OBJECT_TRACKING, OUTPUT_LIST
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.widgets import Button
import matplotlib.lines as mlines

"""
Demonstration program tracing a path using RadarIQ's object tracking
"""

FRAME_RATE = 5  # frames per second
MIN_DISTANCE = 10  # Closest distance to look (mm)
MAX_DISTANCE = 10000  # Furthermost distance to look (mm)
MIN_ANGLE = -45  # Minimum angle to look
MAX_ANGLE = 45  # Maximum angle to look


class Visualize:
    """
    Visualize Paths using RadarIQ's object tracking mode.
    """

    def __init__(self):
        self.riq = None
        self.fig = None
        self.anim = None
        self.line = None
        self.data = [[], []]

    def start(self):
        """
        Start the visualization.
        """
        try:
            self.setup_radariq()
            self.start_animation()
            self.riq.start()

        except Exception as err:
            print(err)
        finally:
            self.exit_handler()

    def setup_radariq(self):
        """
        Setup the RadarIQ module.
        """

        try:
            self.riq = RadarIQ(output_format=OUTPUT_LIST)
            self.riq.set_mode(MODE_OBJECT_TRACKING)
            self.riq.set_units('mm', 'mm/s')
            self.riq.set_frame_rate(FRAME_RATE)
            self.riq.set_distance_filter(MIN_DISTANCE, MAX_DISTANCE)
            self.riq.set_angle_filter(MIN_ANGLE, MAX_ANGLE)

        except Exception as error:
            print(error)

    def start_animation(self):
        frame_speed = (1000 / FRAME_RATE) / 2  # run the animation faster than the module
        self.fig, ax = plt.subplots()
        plt.subplots_adjust(bottom=0.2)

        x_min = tan(radians(MIN_ANGLE)) * MAX_DISTANCE
        x_max = tan(radians(MAX_ANGLE)) * MAX_DISTANCE
        ax.axis([x_min, x_max, MIN_DISTANCE, MAX_DISTANCE])

        # Lines
        line1 = mlines.Line2D([0, x_min], [0, MAX_DISTANCE], color="silver", linewidth=1)
        line2 = mlines.Line2D([0, x_max], [0, MAX_DISTANCE], color="silver", linewidth=1)
        ax.add_line(line1)
        ax.add_line(line2)

        ax_clear = plt.axes([0.81, 0.05, 0.1, 0.075])
        b_clear = Button(ax_clear, 'Clear')
        b_clear.on_clicked(self.clear)

        self.line, = ax.plot(self.data[0], self.data[1], "ro-")
        self.riq.start()
        self.anim = animation.FuncAnimation(self.fig, self.update_plot, frames=self.riq.get_data, interval=frame_speed,
                                            init_func=self.init_plot, blit=True)
        plt.show()

    def init_plot(self):
        return self.line,

    def update_plot(self, frame):
        if frame is not None and len(frame)>0:
            self.data[0].append(frame[0]['x_pos'])
            self.data[1].append(frame[0]['y_pos'])
            self.line.set_data(self.data)
        return self.line,

    def clear(self, event):
        self.data = [[], []]

    def exit_handler(self):
        """
        Catch the program exiting (ctrl C).
        """
        try:
            self.riq.close()
        except Exception:
            pass


if __name__ == '__main__':
    vis = Visualize()
    vis.start()
