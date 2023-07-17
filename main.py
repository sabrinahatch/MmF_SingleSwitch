import numpy as np


class Flow:
    def __init__(self, arrivalTime, size, source, dest):
        self.arrivalTime = arrivalTime
        self.size = size
        self.source = source
        self.dest = dest
        self.pdt = None
        self.completionTime = None

class Link:
    def __init__(self, capacity, fol):
        self.capacity = capacity
        self.fol = fol


# Function to generate job sizes
def generateJobSize():
    return np.random.exponential(1)

# Function that generates an interarrival time
def generateInterarrivalTime():
    return np.random.exponential(10 / 8)

def calcMinInc(unsat_links):
    counter = 0
    for i in unsat_links:
        for x in i.fol:
            if x in unsatFlows:
                counter += 1
        temp.append(i.cap/counter)
    min_inc = min(temp)

    for x in unsatFlows:
        # update each flow's rate and new departure time
        x.rate = x.rate + min_inc
        x.pdt = clock + (x.rpt / x.rate)




def handleArr():
    size = generateJobSize()
    # how do we decide what the src and dest are? Are we generating the pairs randomly?
    global tracker, unsatFlows, satFlows, path1, path2, path3, path4, link1, link2, link3, link4, departures
    flow = Flow(arrivalTime = clock, size = size, source = None, dest = None)

    if tracker == 5:
        tracker = 1
    if tracker == 1:
        path1.append(flow)
        flow.src = link1
        flow.dest = link3
        link1.fol.append(flow)
        link3.fol.append(flow)
    elif tracker == 2:
        path2.append(flow)
        flow.src = link2
        flow.dest = link4
        link2.fol.append(flow)
        link4.fol.append(flow)
    elif tracker == 3:
        path3.append(flow)
        flow.src = link1
        flow.dest = link4
        link1.fol.append(flow)
        link4.fol.append(flow)
    elif tracker == 4:
        path4.append(flow)
        flow.src = link2
        flow.dest = link3
        link2.fol.append(flow)
        link3.fol.append(flow)
    tracker += 1
    unsatFlows.append(flow)
    calcMinInc(unsatFlows)
    lastEvent = clock
    departingJob = min(unsatFlows, key=lambda x: x.pdt)

    # set the next departure and arrival
    nextArrTime =  clock + generateInterarrivalTime()
    nextDepTime = departingJob.pdt





def handleDep():
    global tracker, unsatFlows, satFlows, path1, path2, path3, path4, link1, link2, link3, link4, departures

    departures += 1

seed = 0
maxDepartures = 200000
completionTimes = []
count = 0
runs = 5000
for i in range(runs):
    count += 1
    np.random.seed(seed)
    nextDepTime = float('inf')
    nextArrTime = generateInterarrivalTime()
    jobSizes = []
    temp = []
    satFlows = []
    # will hold all the current jobs being served
    unsatFlows = []
    # declare all of the different path lists
    path1 = []
    path2 = []
    path3 = []
    path4 = []
    departingJob = None
    rate = None
    departures = 0
    clock = 0.0
    lastEvent = clock
    print("********************* This is run: " + str(count) + " *****************************" + "\n")

    while departures <= maxDepartures:
        if nextArrTime <= nextDepTime:
            clock = nextArrTime
            handleArr()
        else:
            clock = nextDepTime
            handleDep()

    seed += 1