#!user/bin/env python
# -*- coding: utf-8 -*-
"""Algorhythms"""

import Queue
import urllib2
import os
import random
import csv
import time


def main(file):
    # create list of requests
    if os.path.exists('queuedata.csv'):
        simulateOneServer('queuedata.csv')

    else:
        response = urllib2.urlopen(file)
        html = response.read()
        localfile = open('queuedata.csv', 'wb')
        localfile.write(html)
        localfile.close()


class Server:
    def __init__(self, ppm):
        self.page_rate = ppm
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
    def __init__(self, time):
        self.timestamp = time
        self.pages = random.randrange(1, 21)

    def get_stamp(self):
        return self.timestamp

    def get_pages(self):
        return self.pages

    def wait_time(self, current_time):
        return current_time - self.timestamp

def simulation(num_seconds, requestsList):
    lab_printer = Server(requestsList)
    print_queue = Queue()
    waiting_times = []
    for request in requestsList:
        task = Request(request)
        print_queue.enqueue(task)
        """if simulateOneServer():
            task = Request(current_second)
            print_queue.enqueue(task)"""
        if (not lab_printer.busy()) and (not print_queue.is_empty()):
            next_task = print_queue.dequeue()
            waiting_times.append(next_task.wait_time(current_second))
            lab_printer.startNext(next_task)
        lab_printer.tick()
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


def simulationMultipleServers(numServers):
    activeServers = 0
    waitingTimeDict = dict()

    for currentSecond in range(totalSeconds):
        waitingTimes = []
        waitingTimeDict[activeServers] = waitingTimes

if __name__ == '__main__':
    main('http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv')

"""def new_print_task():
    num = random.randrange(1, 181)
    if num == 180:
        return True
    else:
        return False

    for i in range(10):
        simulation(3600, 5)"""

