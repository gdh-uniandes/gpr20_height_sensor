"""Mock implementation of mcp3008 library."""

# imports the random library to generate values
import random

# Defines operation modes        
CH0 = 8     # single-ended CH0
CH1 = 9     # single-ended CH1
CH2 = 10    # single-ended CH2
CH3 = 11    # single-ended CH3
CH4 = 12    # single-ended CH4
CH5 = 13    # single-ended CH5
CH6 = 14    # single-ended CH6
CH7 = 15    # single-ended CH7
DF0 = 0     # differential CH0 = IN+ CH1 = IN-
DF1 = 1     # differential CH0 = IN- CH1 = IN+
DF2 = 2     # differential CH2 = IN+ CH3 = IN-
DF3 = 3     # differential CH2 = IN- CH3 = IN+
DF4 = 4     # differential CH4 = IN+ CH5 = IN-
DF5 = 5     # differential CH4 = IN- CH5 = IN+
DF6 = 6     # differential CH6 = IN+ CH7 = IN-
DF7 = 7     # differential CH6 = IN- CH7 = IN+

class MCP3008(object):

    def __init__(self):
        pass

    def read(self, modes, norm=False):

        # Creates the return list
        reading = []
        
        # Iterates over every read mode
        for mode in modes:

            # Generates a random value
            rand_val = random.randint(0, 1024)

            # Normalizes value to 5V for debug
            norm_val = (rand_val / 1024.0) * 5.0 + 0.001

            # Converts analog value into distance for debug purposes
            distance = 0.29998 * norm_val ** -1.173

            # Prints the analog value
            print("Analog value: %d. Equivalent to: %f (5.0V)" % (rand_val, distance))

            # Normalizes value if required
            if norm != False:
                rand_val = (rand_val / 1024.0) * norm

            # Appends random value into list
            reading.append(rand_val)

        # Returns list
        return reading

    def close(self):
        print("Connection is closed!")