import time

from blitzer import Blitzer

with Blitzer():
    time.sleep(1)

with Blitzer():
    for i in range(100000):
        i = i ** 2
