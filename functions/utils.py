
import time


def setInterval(interval, function):
    """
    Args:
        interval (int): The interval in seconds.
        function (function): The function to be executed.
    """
    while True:
        function()
        time.sleep(interval)


