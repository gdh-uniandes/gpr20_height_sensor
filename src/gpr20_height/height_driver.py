
"""Height sensor driver class for GPR-20 robot."""

# Tries to import mcp3008 library
try:
    import mcp3008

# If library not available import mock library
except ImportError:
    import gpr20_height.mcp3008_mock as mcp3008

from time import sleep
from numpy import std, mean


class HeightDriver(object):
    """Height sensor driver class for GPR-20 robot.

    This class handles the SPI communication with a MCP3008 analog-digital
    converter that is connected to a SHARP GP2Y0A21YK0F distance measurement
    sensor. Retrieved data from the distance measurement sensor is then
    converted to a distance value.

    Attributes:
        adc (mcp3008.MCP3008): analog/digital converter interface. It is not a
            custom developed module but an open-source library.
    """

    def __init__(self):
        """Initialize the height sensor driver."""
        # Instantiates the ADC interface
        self._adc = mcp3008.MCP3008()

    def __take_sample(self):
        """Take a distance measurement from the height sensor.

        This methods suppose that a GP2Y0A21YK0F distance sensor is being
        used for the measurements. Thus this methods reads a voltage value
        from the ADC and then converts the voltage into distance based on the
        sensor's datasheet.

        Returns:
            float: measured distance in meters from the height sensor.
        """
        # Reads ADC data normalized with 5.3V
        adc_data = self._adc.read([mcp3008.CH0], 5.3)[0] + 0.001

        # Converts measured voltage to distance based on datasheet
        distance = 0.29998 * adc_data ** -1.173

        # Returns calculated distance
        return distance

    def take_measurement(self):
        """Method to return a valid measurment value when requested.

        In order to prevent erroneus data to be returned, a statistical
        analysis is performed. The statistical analysis consists of removing
        outliers in data samples. This is done by calculating the standard
        deviation and the mean of the samples. If the std. deviation is higher
        than a fixed value, the furthest measurment is removed from the
        samples. This is done until the std. deviation is less than the
        defined threshold.

        Returns:
            float: mean of the valid measurements from the height sensor.
        """
        # Define a list to store measurements
        measurements_list = []

        # Iterate to acquire thirty (30) measurements
        for indx in range(30):

            # Acquire the measurement
            distance = self.__take_sample()

            # Store data in list
            measurements_list.append(distance)

            # Waits for five (5) milliseconds
            sleep(0.005)

        # Defines a flag to process data until reaching consensus
        proc_finished = False

        # Iterate until data is processed
        while not proc_finished:

            # Calculate the standard deviation
            data_std_dev = std(measurements_list)

            # Calculate the mean
            data_mean = mean(measurements_list)

            # Check if standard deviation meets requirement (<0.005)
            if data_std_dev < 0.005:

                # Sets the process to finished
                proc_finished = True

            # Eliminate data id std. dev. does not meet requirement
            else:

                # Furthest data element index and delta
                far_indx, far_delta = 0, 0

                # Iterate over measurements
                for indx in range(len(measurements_list)):

                    # Calculate delta
                    delta = abs(measurements_list[indx] - data_mean)

                    # Check if delta is higher than highest delta
                    if delta > far_delta:

                        # Store element indx and value if meets condition
                        far_indx, far_delta = indx, delta

                # Removes outlier from data
                measurements_list.pop(far_indx)

        # Return the mean of the valid samples
        return data_mean

    def __del__(self):
        """Delete method implementation to close ADC connection."""
        self._adc.close()
