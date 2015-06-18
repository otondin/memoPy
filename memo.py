# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import random

SCHEDULING_ALGORITHMS = (
    ('first-fit', 'First-fit'),
    ('circular-fit', 'Circular-fit'),
    ('bert-fit', 'Best-fit'),
    ('worst-fit', 'Worst-fit'),
)

PROCESS_SIZE_MIN = 100  # in bytes
PROCESS_SIZE_MAX = 1000  # in bytes
PROCESS_EXEC_TIME_MIN = 1  # in seconds
PROCESS_EXEC_TIME_MAX = 300  # in seconds
MEMORY_SIZE = 5000  # in bytes


class Process(object):
    """"
    A process class created to be instanciated and used along the running simulation
    """
    pid = None
    size = None
    execution_time = None

    def get_pid(self):
        return self.pid

    def get_size(self):
        return self.size


# Declarating basic control variables
scheduling = sys.argv[1]
number_processes = sys.argv[2]

delay_time = 0
if len(sys.argv) == 4:
    delay_time = float(sys.argv[3])


# Declarating processes array list
processes = []


# Generating PID's to prevent repetition
pid_deck = list(range(0, 1000))
random.shuffle(pid_deck)


# Processing time counter var declaration
processing_time_zero = time.clock()  # Simulate started time
processing_time_result = 0  # Simulate result total time


# Timing control
time_ending = None
time_resulting = None


# Starting the timer
time_starting = time.time()


# Systema Memory Control
system_memory = MEMORY_SIZE
system_memory_used = 0
system_memory_unused = MEMORY_SIZE
memory_used_measure = None
memory_unused_measure = None


# Clock Control
clock = 0


def manager_output(cicle, processes, memory_free):
    sys.stdout.write('Clicle %d - Processes managed: %d - Memory Free %d \n' % (cicle, processes, system_memory))
    sys.stdout.flush()


# Memory Manager
while len(processes) < int(number_processes):
    clock = clock + 1
    manager_output(clock, len(processes), system_memory)

    # Creating rate is 20% to decide if a process will be created this time or not
    create_process_rating = random.randint(1, 5)

    # If you get lucky we're gonna create the process right now...
    if create_process_rating == 1:
        p = Process()
        p.pid = pid_deck.pop()
        p.size = random.randint(PROCESS_SIZE_MIN, PROCESS_SIZE_MAX)
        p.execution_time = random.randint(PROCESS_EXEC_TIME_MIN, PROCESS_EXEC_TIME_MAX)

        if p.size > system_memory:
            print("The system is out of memory right now to execute your process.")
        else:
            processes.append(p)
            system_memory = system_memory - p.size
            system_memory_used = system_memory_used + p.size
            system_memory_unused = system_memory_unused + (system_memory - p.size)
        print("The process with PID %d was created with size %d e and will take %d seconds to be executed." % (p.pid, p.size, p.execution_time))

        time.sleep(p.execution_time / 1000)
        # system_memory = system_memory + p.size

    # User friendly delay to enable better view of the screen informations
    time.sleep(delay_time)

    # Calculating process time running
    processing_time_result = processing_time_zero + time.clock()


# Measuring memory usage
memory_used_measure = system_memory_used / len(processes)
memory_unused_measure = system_memory_unused / len(processes)

# Endind the simulator and outputing some last informations to user
print("Total processes managed: %d" % len(processes))
print("Total clicles: %d" % clock)
print("Measuse used memory each cicle: %.d" % memory_used_measure)
print("Measuse unused memory each cicle: %.d" % memory_unused_measure)
