######################################################################
#
# File: b2/bounded_queue_executor.py
#
# Copyright 2018 Backblaze Inc. All Rights Reserved.
#
# License https://www.backblaze.com/using_b2_code.html
#
######################################################################

import threading


class BoundedQueueExecutor(object):
    """
    Wraps a futures.Executor and limits the number of requests that
    can be queued at once.  Requests to submit() tasks block until
    there is room in the queue.

    The number of available slots in the queue is tracked with a
    semaphore that is acquired before queueing an action, and
    released when an action finishes.
    """

    def __init__(self, executor, queue_limit):
        self.executor = executor
        self.semaphore = threading.Semaphore(queue_limit)

    def submit(self, fcn, *args, **kwargs):
        # Wait until there is room in the queue.
        self.semaphore.acquire()

        # Wrap the action in a function that will release
        # the semaphore after it runs.
        def run_it():
            try:
                fcn(*args, **kwargs)
            finally:
                self.semaphore.release()

        # Submit the wrapped action.
        return self.executor.submit(run_it)

    def shutdown(self):
        self.executor.shutdown()
