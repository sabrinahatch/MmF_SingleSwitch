# Sabrina Hatch
# CMU REUSE SNAP Lab
# Summer 2023

import numpy as np

# create flow class
class Flow:
    def __init__(self, arrivalTime, size, src, dest, rate, rpt):
        self.arrivalTime = arrivalTime
        self.size = size
        self.src = src
        self.dest = dest
        self.pdt = None
        self.completionTime = None
        self.rate = rate
        self.rpt = rpt


# create link class to keep track of link capacity
class Link:
    def __init__(self, cap, fol):
        self.cap = cap
        self.fol = fol


# Function to generate job sizes
def generateJobSize():
    return np.random.exponential(1)


# Function that generates an interarrival time
def generateInterarrivalTime():
    return np.random.exponential(10 / 8)


def maxMinFair(listOfLinks):
    global unsatLinks, unsatFlows, min_inc, temp, temp2
    # find the min inc for all the flows
    for i in unsatLinks:
        for x in i.fol:
            if x in unsatFlows:
                temp.append(x)
        var = (i.cap / len(temp))
        temp2.append(var)
    min_inc = min(temp2)
    print("this is the min inc " +  str(min_inc))
    # now update each flows' rate & pdt
    for x in unsatFlows:
        # update each flow's rate and new departure time
        x.rate = x.rate + min_inc
        x.pdt = clock + (x.rpt / x.rate)
    # calculates the capacity of the links and updates their attributes
    for x in unsatLinks:
        x.cap = 1 - sum([i.rate for i in x.fol])

    # iterate over lists of sat links/flows and unsat links/flows and update them accordingly based on the new water
    # filling algo application

    arrSize1 = len(unsatLinks)
    a = 0
    while a < arrSize1:
        if unsatLinks[a].cap == 0:
            satLinks.append(unsatLinks[a])
            del unsatLinks[a]
            arrSize1 -= 1
        else:
            a += 1

    arrSize2 = len(unsatFlows)
    b = 0
    while b < arrSize2:
        if (unsatFlows[b].dest in satLinks) or (unsatLinks[a].src in satLinks):
            satFlows.append(unsatFlows[b])
            del unsatFlows[b]
            arrSize2 -= 1
        else:
            b += 1




def handleArr():
    # declare all global variables
    global tracker, unsatFlows, satFlows, path1, path2, path3, path4, link1, link2, link3, link4, departures, lastEvent, departingJob, nextArrTime, nextDepTime

    # create new flow object for new arrival
    size = generateJobSize()
    flow = Flow(arrivalTime=clock, size=size, src=None, dest=None, rate = 0, rpt = size)

    # implement roundrobin system to assign flows to different paths
    # if we reach 5, we need to restart the counter
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
    # incremement the track to keep roundrobin
    tracker += 1
    # append the new flow to the list of unsat flows
    unsatFlows.append(flow)
    # calculate the new minInc for the updated list of flows
    maxMinFair(unsatLinks)
    # update new lastEvent
    lastEvent = clock
    # assign the next departing job based on the pdt
    departingJob = min(unsatFlows, key=lambda x: x.pdt)

    # set the next departure and arrival
    nextArrTime = clock + generateInterarrivalTime()
    nextDepTime = departingJob.pdt


def handleDep():
    global tracker, unsatFlows, satFlows, path1, path2, path3, path4, link1, link2, link3, link4, departures, satLinks, lastEvent, departingJob, nextArrTime, nextDepTime
    # inc the dep counter
    departures += 1
    # set completion time of departing job
    departingJob.completionTime = clock - departingJob.arrivalTime
    # if we are on the last job of the run, append to corr list
    if departures == maxDepartures:
        completionTimes.append(departingJob.completionTime)
    # remove the job from the list of unsatFlows (flows being serviced)
    unsatFlows.remove(departingJob)
    # if there are still link that are unsaturated, we need to update their jobs' rpts now that
    # a flow has just left the system
    if len(unsatLinks) != 0:
        for x in unsatFlows:
            x.rpt = x.rpt - (x.pdt - clock) * x.rate
        maxMinFair(unsatLinks)

        lastEvent = clock
        departingJob = min(unsatFlows, key=lambda x: x.pdt)
    else:
        departingJob = None
        nextDepTime = float("inf")
        lastEvent = clock


seed = 0
maxDepartures = 10
completionTimes = []
count = 0
runs = 5
for i in range(runs):
    count += 1
    np.random.seed(seed)
    nextDepTime = float('inf')
    nextArrTime = generateInterarrivalTime()
    jobSizes = []
    temp = []
    temp2 = []
    satFlows = []
    satLinks = []
    # will hold all the current jobs being served
    unsatFlows = []
    # declare all of the different path lists
    path1 = []
    path2 = []
    path3 = []
    path4 = []

    link1 = Link(1, [])
    link2 = Link(1, [])
    link3 = Link(1, [])
    link4 = Link(1, [])
    unsatLinks = [link1, link2, link3, link4]
    # start the first job off in the correct order for round robin

    tracker = 1
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
