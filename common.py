import threading

#last_tracked_angles = None
thread_lock = threading.Condition()

windowLength = 1360
windowHeight = 768