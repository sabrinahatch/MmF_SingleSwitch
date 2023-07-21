# Sabrina Hatch
# CMU REUSE SNAP Lab
# Summer 2023

# how would I do this for SRPT and try to optimize so that it's an easier transition

import numpy as np

# create flow class
class Flow:
    def __init__(self, arrivalTime, size, src, dest, rate, rpt):
        self.arrivalTime = arrivalTime
        self.size = size
        self.src = src
        self.dest = dest
        self.rate = rate
        self.rpt = rpt
        self.pdt = None
        self.completionTime = None

class Link:
    def __init__(self, cap, name, fol, type):
        self.cap = cap
        self.name = name
        self.fol = fol
        self.type = type

class Path:
    def __init__(self, name, matching, serviceList):
        self.name = name
        self.matching = matching
        self.serviceList = serviceList
        self.nextPathArrival = None
        self.nextPathDeparture = None




# fcn to generate job sizes
def generateJobSize():
    return np.random.exponential(1)

# fcn that generates an interarrival time
def generateInterarrivalTime():
    return np.random.exponential(10 / 8)


# fcn to generate all the link objects in the system
def initializeLinks(k):
    if k % 2 != 0:
        raise ValueError("k must be an even number.")

    links = []
    half_k = k // 2

    # split the ports into source and destination categories
    for port in range(1, half_k + 1):
        src_name = "src" + str(port)
        dest_name = "dest" + str(port)
        src_link = Link(name=src_name, cap=1, fol=[], type="src")
        dest_link = Link(name=dest_name, cap=1, fol=[], type="dest")
        links.extend([src_link, dest_link])
    return links


def makeMatchings(links):
    src_links = [link for link in links if link.type == "src"]
    dest_links = [link for link in links if link.type == "dest"]

    if len(src_links) != len(dest_links):
        raise ValueError("Number of source links must be equal to the number of destination links.")

    matchings = []
    for src_link in src_links:
        for dest_link in dest_links:
            matching = (src_link, dest_link)
            matchings.append(matching)

    return matchings
# function that runs the MmF algorithm on the list of unsatLinks (links that are currently being serviced)
# function updates link and flow attributes to accurately represent the state of the system in any given point of time
def maxMinFair(listOfLinks):
    global unsatLinks, unsatFlows, min_inc, temp, temp2
    # find the min inc for all the flows
    for i in unsatLinks:
        for x in i.fol:
            if x in unsatFlows:
                temp.append(x)
        var = (i.cap / len(temp)) if len(temp) > 0 else 0
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
        if (unsatFlows[b].dest in satLinks) or (unsatFlows[b].src in satLinks):
            satFlows.append(unsatFlows[b])
            del unsatFlows[b]
            arrSize2 -= 1
        else:
            b += 1

# fcn to handle an arrival event
def handleArr():
    # declare all global variables
    global unsatFlows, satFlows, path1, path2, path3, path4, link1, link2, link3, link4, departures, lastEvent, departingJob, nextArrTime, nextDepTime

    # create new flow object for new arrival
    size = generateJobSize()
    flow = Flow(arrivalTime=clock, size=size, src=None, dest=None, rate = 0, rpt = size)

    # implement roundrobin system to assign flows to different paths

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

# fcn to handle a departure event
def handleDep():
    global tracker, unsatFlows, satFlows, path1, path2, path3, path4, link1, link2, link3, link4, departures, satLinks, lastEvent, departingJob, nextArrTime, nextDepTime
    # inc the dep counter
    departures += 1
    # set completion time of departing job
    departingJob.completionTime = clock - departingJob.arrivalTime

    print("this is the departing job: " + str(departingJob))
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



# sim logic
seed = 0
maxDepartures = 10
completionTimes = []
runs = 5
# input number of ports that you want
numPorts = 4
count = 0
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
    unsatFlows = []
    allArrivals = []
    allDepartures = []


    # Generate links and matchings
    matchings = makeMatchings(links = initializeLinks(numPorts))

    # Create a path object for each matching
    paths = []
    for index, matching in enumerate(matchings):
        src_link, dest_link = matching
        name = f"Path_{index + 1}"  # You can use any naming convention here
        serviceList = []  # Add flows that belong to this path here
        path = Path(name=name, matching=matching, serviceList=serviceList)
        paths.append(path)


    # start the first job off in the correct order for round robin
    departingJob = None
    rate = None

    # add new arrival times for each path list to create pending jobs
    # add to total list as well to filter out when next job will occur
    for x in paths:
        x.nextPathArrival = generateInterarrivalTime()
        allArrivals.append(x.nextPathArrival)
        print(x.nextPathArrival)
    print("this is the list of all arrivals: " + str(allArrivals))


    # determine the next arrival
    nextArrTime = min(allArrivals)
    print("this is the next arrival event: " + str(nextArrTime))
    # set first departure time to be inf
    nextDepTime = float("inf")
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
