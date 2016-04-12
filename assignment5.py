#!user/bin/env python
# -*- coding: utf-8 -*-
"""Algorhythms"""


import urllib2
import os
import csv


class Queue: # I defined the class becuase it the methods didn't seem to exist with 'import Queue'
    def __init__(self):
        self.items = []
    def is_empty(self):
        return self.items == []
    def enqueue(self, item):
        self.items.insert(0,item)
    def dequeue(self):
        return self.items.pop()
    def size(self):
        return len(self.items)

def main(file, servers):
    # create list of requests
    if os.path.exists('queuedata.csv'):
        if servers is None:
            simulateOneServer('queuedata.csv')
        else:
            simulateManyServers('queuedata.csv', servers)

    else:
        response = urllib2.urlopen(file)
        html = response.read()
        localfile = open('queuedata.csv', 'wb')
        localfile.write(html)
        localfile.close()


class Server:
    def __init__(self, secsPross):
        self.page_rate = secsPross
        self.current_task = None
        self.time_remaining = 0

    def tick(self):
        if self.current_task != None:
            self.time_remaining = self.time_remaining - 1
            if self.time_remaining <= 0:
                self.current_task = None

    def busy(self):
        if self.current_task != None:
            return True
        else:
            return False

    def start_next(self, new_task):
        self.current_task = new_task
        self.time_remaining = new_task.get_pages() * 60/self.page_rate


class Request:

    def __init__(self, time, processTime):
        self.timestamp = time
        self.processTime = processTime

    def get_stamp(self):
        return self.timestamp

    def get_pages(self):
        return self.processTime

    def wait_time(self, current_time):
        return current_time - self.timestamp

def simulation(num_seconds, requestsList):
    print_queue = Queue()
    waiting_times = []
    current_second = 0
    for request in requestsList:
        lab_printer = Server(int(request[2]))
        task = Request(int(request[0]), int(request[2]))
        print_queue.enqueue(task)
        print print_queue # confirming a Queue object is created
        while current_second < num_seconds:
            current_second += int(request[2]) # to keep track of the amount of seconds elapsed
                                              # and end the task once the total amount possible has elapsed (num_seconds)

            if (not lab_printer.busy()) and (not print_queue.is_empty()):
                next_task = print_queue.dequeue() #Can't seem to get this to be anything other than [0]
                waiting_times.append(next_task.wait_time(int(request[0])))
                lab_printer.start_next(next_task)

            average_wait = sum(waiting_times) / len(waiting_times)
            print("Average Wait %6.2f secs %3d tasks remaining."
                    %(average_wait, print_queue.size()))


def simulateOneServer(file):
    # call simulation
    # simulation(totalSeconds, requestsList)
    f = open(file, 'rb')
    reader = csv.reader(f)

    requestsList = []
    for row in reader:
        requestsList.append(row)

    totalSeconds = requestsList[-1][0] # access total time
    simulation(totalSeconds, requestsList)


def simulateManyServers(requestList, numServers): # This function is incomplete. You helped me with it
                                                  # a bit during office hours, but I was unable to
                                                  # complete it as I could not get past the single server function
    f = open(file, 'rb')
    reader = csv.reader(f)
    requestsList = []

    for row in reader:
        requestsList.append(row)

    totalSeconds = requestsList[-1][0] # access total time
    activeServers = 0
    waitingTimeDict = dict()

    for currentSecond in range(totalSeconds):
        waitingTimes = []
        waitingTimeDict[activeServers] = waitingTimes

if __name__ == '__main__':
    main('http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv', None)



