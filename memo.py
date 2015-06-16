# !/usr/bin/python
# -*- coding: utf-8 -*-

# import sys
import time
import random

MAX_PROCESS_LIMIT = 999

HARD_DRIVE_IO_TIME_MIN = 200

HARD_DRIVE_IO_TIME_MAX = 300

VIDEO_DRIVE_IO_TIME_MIN = 100

VIDEO_DRIVE_IO_TIME_MAX = 200

PRINTER_DRIVE_IO_TIME_MIN = 50

PRINTER_DRIVE_IO_TIME_MAX = 600

PROCESS_LOOP_MIN = 100

PROCESS_LOOP_MAX = 300

PROCESS_ALLOC_TIME_MAX = 50

IO_DEVICES = {
    0: 'hd',
    1: 'video',
    2: 'printer'
}

PROCESS_STATES = {
    'blocked': 0,
    'created': 1,
    'destroyed': 2,
    'ready': 3,
    'running': 4
}


class Process(object):
    """"
    A process class created to be instanciated and used along the running simulation
    """
    pid = None
    state = None
    time_total = None
    time_remaining = None
    # time_running_loop = None
    # time_current_status = None
    # time_ioing = None
    # running_time = None
    # ready_time = None
    # state_time_ready = None
    # state_time_running = None
    # state_time_blocked = None
    # state_time_destroyed = None

    def set_state(self, state=None):
        self.state = PROCESS_STATES[state]
        return self

    def get_state(self):
        return self.state


# Declarating basic control variables
process_total = 999
delay_time = 2
clock_ping = 1

# Declarating processes array list
processes = []

# Generating PID's to prevent repetition
pid_deck = list(range(0, 1000))
random.shuffle(pid_deck)

# Processing time counter var declaration
processing_time_zero = time.clock()  # Simulate started time
processing_time_result = None  # Simulate result total time


# Timing control
time_ending = None
time_resulting = None


# Starting the timer
time_starting = time.time()


def still_process_to_run():
    for p in processes:
        if p.state != 'destroyed':
            return True

    return False


# Checking the process number typed by user. Needs to be from 5 to 999!
if (process_total >= 5 and process_total <= 999):
    while len(processes) < process_total:
        """"
        While the processes just created are minus than the process number typed by user
        to simulate, do
        """

        # Sorting rate is 20% to decide if a process will be created this time or not
        create_process_sorting = random.randint(1, 5)  # Shorting range to make more time matching

        # If you get lucky we're gonna create the process right now...
        if create_process_sorting <= 1:
            p = Process()
            p.pid = pid_deck.pop()
            p.set_state('created')
            p.time_total = random.randint(100, 300)
            processes.append(p)
            print('CLOCK: a new process was just created with PID: %d & STATE: %s & CLOCK TIME: %d' % (p.pid, p.state, p.time_total))

            # Sorting rate is 1% to process take some I/O resource
            will_ioing = random.randint(1, 100)

            if will_ioing == 1:

                # Setting process state to running and get ready to make I/O access
                p.set_state('running')
                print('I/O ALERT: The process with PID %d is gonna make an I/O access... Now state is: %s' % (p.pid, p.state))

                # Sorting what is gonna be the I/O resource to access
                io_dev = random.randint(0, 2)

                # Getting HD resource
                if io_dev == 0:
                    io_dev_time = random.randint(HARD_DRIVE_IO_TIME_MAX, HARD_DRIVE_IO_TIME_MAX)
                # Getting Vide resource
                elif io_dev == 1:
                    io_dev_time = random.randint(VIDEO_DRIVE_IO_TIME_MIN, VIDEO_DRIVE_IO_TIME_MAX)
                # Getting printer resource
                elif io_dev == 2:
                    io_dev_time = random.randint(PRINTER_DRIVE_IO_TIME_MIN, PRINTER_DRIVE_IO_TIME_MAX)

                p.time_total = p.time_total + io_dev_time
                print('I/O ALERT: The process with PID %d is being access %s I/O resource and it will take %d' % (p.pid, IO_DEVICES[io_dev], io_dev_time))
                time.sleep(p.time_total / 100)
                print('PROCESS ALERT: The process with PID %d has finished to access I/O resource and is being destroyed after %d' % (p.pid, p.time_total))

                # Destroying process before make I/O resource access
                p.set_state = PROCESS_STATES['destroyed']
            else:
                # Setting remaining running loop time to the process
                p.time_remaining = p.time_total - PROCESS_ALLOC_TIME_MAX

                if p.time_remaining <= 0:
                    # Destoying the state because is all done!
                    p.set_state('destroyed')
                    print('PROCESS ALERT: The process with PID %d is all done! Now state is: %s' % (p.pid, p.state))
                else:
                    # Setting ready state to the process
                    p.set_state('ready')
                    print('PROCESS ALERT: The process with PID %d does not make anyone I/O and has more %d to take running. Now state is: %s' % (p.pid, p.time_remaining, p.state))
        else:
            print('CLOCK: None process was created this time...')

        # User friendly delay to enable better view of the screen informations
        time.sleep(delay_time)

        # Calculating process time running
        processing_time_result = processing_time_zero + time.clock()


else:
    print('You need to type processs number between 5 and 999! Try again... ;-)')

# Calcutating real time app running
time_ending = time.time()
time_resulting = time_ending - time_starting

print('Total started process: %d' % len(processes))
print('All process were created and took %f of processing time. They all are ready to work!' % processing_time_result)
print('The real time app running was %f' % time_resulting)
