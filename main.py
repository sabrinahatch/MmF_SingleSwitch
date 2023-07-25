# Sabrina Hatch
# CMU REUSE SNAP Lab
# Summer 2023

import numpy as np
from itertools import groupby

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

# fcn that makes unique matchings of the links to create every possible path in the system
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
def maxMinFair(unsatLinks, unsatFlows, clock):
    # find the min inc for all the flows
    for link in unsatLinks:
        print("these are the flows on link attr: " + str(link) + " , " + str(link.fol))
    # should this be the non zero min? The only time it would be 0 is if the link was saturated or if anothe link was empty
    min_inc = min([link.cap / len(link.fol) for link in unsatLinks if len(link.fol) > 0])
    print("this is the min inc " +  str(min_inc))
    print("\n")



    # now update each flows' rate & pdt
    for x in unsatFlows:
        # update each flow's rate and new departure time
        x.rate += min_inc
        if min_inc == 0:
            x.pdt = clock + x.rpt
        else:
            x.pdt = clock + (x.rpt / x.rate)


    # calculates the capacity of the links and updates their attributes
    for x in unsatLinks:
        x.cap = 1 - sum([flow.rate for flow in x.fol])

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
def handleArr(whichPath):
    # declare all global variables
    global unsatFlows, satFlows, path1, path2, path3, path4, link1, link2, link3, link4, departures, lastEvent, departingJob, nextArrTime, nextDepTime

    # create new flow object for new arrival
    size = generateJobSize()
    # creates the job for the specific path and gives it an initial rate of 0
    flow = Flow(arrivalTime=clock, size=size, src=whichPath.matching[0], dest=whichPath.matching[1], rate = 0, rpt = size)
    # update the flows on link attribute for the links in the path the job is traversing
    whichPath.matching[0].fol.append(flow)
    whichPath.matching[1].fol.append(flow)

    print("this is the new flow " + str(flow) + " on the links: " + str(flow.src) + " , " + str(flow.dest))



    # append the new flow to the list of unsat flows
    unsatFlows.append(flow)
    # calculate the new minInc for the updated list of flows
    print("This is the list of unsatFlows: " + str(unsatFlows))
    print("This is the list of unsatLinks: " + str(unsatLinks))
    maxMinFair(unsatLinks, unsatFlows, clock)
    # update new lastEvent
    lastEvent = clock




    # set the next arrival for the specific path we are on right now
    whichPath.nextPathArrival = clock + generateInterarrivalTime()

    # set the next departure time
    nextDepTime = min(unsatFlows, key=lambda x: x.pdt)

    # determine the next arrival based on total list of path arrivals
    nextArrTime = min(unsatFlows, key=lambda x: x.nextPathArrival)

# fcn to handle a departure event
def handleDep():
    global unsatFlows, satFlows, path1, path2, path3, path4, link1, link2, link3, link4, departures, satLinks, lastEvent, departingJob, nextArrTime, nextDepTime
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
        maxMinFair(unsatLinks, unsatFlows, clock)

        lastEvent = clock
        departingJob = min(unsatFlows, key=lambda x: x.pdt)
    else:
        departingJob = None
        nextDepTime = float("inf")
        lastEvent = clock



# sim logic
seed = 0
maxDepartures = 20
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
    # list that hold all pending arrivals at any given moment
    allArrivals = []
    allDepartures = []


    # Generate links and matchings and then start out by appending all the newly created
    # links to unsatLInks list
    links = initializeLinks(numPorts)
    unsatLinks = links
    matchings = makeMatchings(links)



    # Create a path object for each matching
    paths = []
    for index, matching in enumerate(matchings):
        src_link, dest_link = matching
        name = f"Path_{index + 1}"
        serviceList = []  # Add flows that belong to this path here
        path = Path(name=name, matching=matching, serviceList=serviceList)
        paths.append(path)


    departingJob = None
    rate = None

    # generate pending jobs for each pathList
    for x in paths:
        x.nextPathArrival = generateInterarrivalTime()
        print("This is the path: " + str(x.name) + " with next arrival time: " + str(x.nextPathArrival))
    # determine the first arrival
    whichPath = min(paths, key = lambda path: path.nextPathArrival)
    nextArrTime = whichPath.nextPathArrival
    # set first departure time to be inf
    nextDepTime = float("inf")




    departures = 0
    clock = 0.0
    lastEvent = clock

    # for x in paths:
    #     print(x)
    #     print(x.name)
    #     print(x.matching)
    #     print(x.nextPathArrival)
    #     print("\n")


    print("This is the path with the closest arrival time: " + str(whichPath) + " of " + str(whichPath.nextPathArrival))
    print("\n")



    # at this point, all the links are unsaturated and there are not
    # yet any flows to add to the unsatFlows list. Additionally, there are no flows in the
    # serviceList attr of each of the flows


    print("********************* This is run: " + str(count) + " *****************************" + "\n")

    while departures <= maxDepartures:
        if nextArrTime <= nextDepTime:
            clock = nextArrTime
            handleArr(whichPath)
        else:
            clock = nextDepTime
            handleDep()

    seed += 1
