import numpy as np


class RingBuffer:
    """
    A 1D ring buffer using numpy arrays
    Based on https://scimusing.wordpress.com/2013/10/25/ring-buffers-in-pythonnumpy/
    """

    def __init__(self, length, dtype=np.uint8):
        self._length = length
        self._dtype = dtype
        self.clear()
        self.index = 0

    def extend(self, x):
        "adds array x to ring buffer"
        x_index = (self.index + np.arange(x.size)) % self.data.size
        self.data[x_index] = x
        self.index = x_index[-1] + 1

    def get(self):
        "Returns the first-in-first-out data in the ring buffer"
        idx = (self.index + np.arange(self.data.size)) % self.data.size
        return self.data[idx]

    def clear(self):
        self.data = np.zeros(self._length, self._dtype)


def ringbuff_numpy_test():
    ringlen = 100000
    ringbuff = RingBuffer(ringlen)
    for i in range(40):
        ringbuff.extend(np.zeros(10000, dtype='f'))  # write
        ringbuff.get()  # read
