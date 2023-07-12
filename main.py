import numpy as np

class Job:
    def __init__(self, arrivalTime, size, source, dest):
        self.arrivalTime = arrivalTime
        self.size = size
        self.source = source
        self.dest = dest
        self.departureTime = None
        self.completionTime = None


# Function to generate job sizes
def generateJobSize():
    return np.random.exponential(1)

# Function that generates an interarrival time
def generateInterarrivalTime():
    return np.random.exponential(10 / 8)
