from math import tan, radians
from radariq import RadarIQ, MODE_OBJECT_TRACKING, OUTPUT_LIST



FRAME_RATE = 10  # frames per second
MIN_DISTANCE = 1000  # Closest distance to look (mm)
MAX_DISTANCE = 10000  # Furthermost distance to look (mm)
MIN_ANGLE = -30  # Minimum angle to look
MAX_ANGLE = 30  # Maximum angle to look


class CountRodent:
    """
    Count rodent
    """

    def __init__(self):
        self.riq = None
        self.people = {}  # In the form {<object id> : 'left|right'}
        self.counter = 0

    def start(self):
        """
        Start the visualization.
        """
        try:
            self.setup_radariq()
            self.riq.start()
            self.run_counter()

        except Exception as err:
            print(err)
        finally:
            self.exit_handler()

    def setup_radariq(self):
        """
        Set up the RadarIQ module.
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

    def run_counter(self):
        for frames in self.riq.get_data():  # loop goes round once per frame
            if frames is not None and len(frames) > 0:
                for frame in frames:
                    if frame['tracking_id'] in self.people.keys():  # has the person previously been detected
                        # person start on the left and is now at the right of the sensors field of view
                        if self.people[frame['tracking_id']] == 'left' and self.is_at_right_boundary(frame['x_pos'], frame['y_pos']):
                            self.people[frame['tracking_id']] = 'right'
                            self.count()
                        # person start on the right and is now at the left of the sensors field of view
                        elif self.people[frame['tracking_id']] == 'right' and self.is_at_left_boundary(frame['x_pos'], frame['y_pos']):
                            self.people[frame['tracking_id']] = 'left'
                            self.count()

                    else:  # New person
                        # If they are at the left boundary, begin counting them
                        if self.is_at_left_boundary(frame['x_pos'], frame['y_pos']):
                            self.people[frame['tracking_id']] = 'left'
                        # If they are at the right boundary, begin counting them
                        elif self.is_at_right_boundary(frame['x_pos'], frame['y_pos']):
                            self.people[frame['tracking_id']] = 'right'
                        # don't count at all until the object touches a boundary.
                        else:
                            pass

    def count(self):
        self.counter += 1
        print("Number of rodents {self.counter}")

    def is_at_left_boundary(self, x, y):
        """
        See if the object is on the left boundary.

        :param x: X coordinate of the object
        :param y: Y coordinate of the object
        :return:
        """
        x_boundary = tan(radians(MIN_ANGLE)) * y  # find where the x boundary would be for the objects y position
        x_boundary_1 = x_boundary * 0.8
        x_boundary_2 = x_boundary * 1.2

        # if the object is within the tolerance of the boundary
        result = x_boundary_1 > x > x_boundary_2
        if result:
            print("Rodent detected at LEFT boundary")
        return result

    def is_at_right_boundary(self, x, y):
        """
        See if the object is on the right boundary.

        :param x: X coordinate of the object
        :param y: Y coordinate of the object
        :return:
        """
        x_boundary = tan(radians(MAX_ANGLE)) * y  # find where the x boundary would be for the objects y position
        x_boundary_1 = x_boundary * 0.8
        x_boundary_2 = x_boundary * 1.2

        # if the object is within the tolerance of the boundary
        result = x_boundary_1 < x < x_boundary_2
        if result:
            print("Rodent detected at RIGHT boundary")
        return result

    def exit_handler(self):
        """
        Catch the program exiting (ctrl C).
        """
        try:
            self.riq.close()  # this will stop the sensor which will stop the run_counter loop
        except Exception:
            pass


if __name__ == '__main__':
    rodent_counter = CountRodent()
    rodent_counter.start()
