#!/usr/bin/env python3
import threading

# tool to keep track of queued items
class queued():
    padlock = threading.Lock()
    values = []

    # add an item to the queue
    def append(self, n):
        self.padlock.acquire()
        self.values.append(n)
        self.padlock.release()

    # return what's in queue and purge everything
    def get(self):
        self.padlock.acquire()
        values = self.values
        self.padlock.release()
        self.values = []
        return values

