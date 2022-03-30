"""ROS interface for height sensor."""

import rospy
from gpr20_msgs.srv import GetHeight, GetHeightResponse
from gpr20_height.height_driver import HeightDriver


class HeightNode(object):
    """ROS interface for GPR-20 height sensor."""

    def __init__(self):
        """Initialize the ROS interface for height sensor."""
        # Initializes the ROS node for height sensor
        rospy.init_node("height_sensor", anonymous=False)

        # Instantiates the sensor driver
        self._sensor_driver = HeightDriver()

        # Creates a service to return the measured height on request
        rospy.Service(
            "get_height",
            GetHeight,
            self.height_handler
        )

        # Loops until node is shutdown
        while not rospy.is_shutdown():

            # Spins node to prevent from exiting
            rospy.spin()

    def height_handler(self, srv):
        """Handle a service request to get a height measurement.

        This method handles the get height measurment functionality of the
        GPR-20 software stack. The returned distance is the mean of the
        measurements that provide a standard deviation less than a specific
        value.

        Args:
            srv (gpr20_msgs.GetHeight): request to acquire the distance from
                the height sensor.

        Returns:
            gpr20_msgs.GetHeightResponse: reponse with the most statistically
                significant height measurement.
        """
        # Get the measurement from driver
        distance = self._sensor_driver.take_measurement()

        # Sends service response
        return GetHeightResponse(distance)
