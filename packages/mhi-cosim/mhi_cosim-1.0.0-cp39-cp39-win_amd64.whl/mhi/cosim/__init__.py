import os, sys
from contextlib import contextmanager
from typing import Tuple

"""
MHI Python Co-simulation Module
===============================

Example::

    import mhi.cosim

    with mhi.cosim.cosimulation("config.cfg") as cosim:
       channel = cosim.find_channel(1)

       time = 0
       time_step = 0.001
       run_time = 1.0

       x = ...
       y = ...
       z = ...
       
       while time <= run_time:

           a = ...
           b = ...
           c = ...
           d = ...

           time += time_step
           channel.set_values(a, b, c, d)
           channel.send(time)

           if time <= run_time:
               x, y, z = channel.get_values(time)
"""


class Error(Exception):
    """
    Cosim Exceptions
    """

class Channel:
    def __init__(self, channel_id: int):
        """
        Create a channel object on the given `channel_id`
        """

    def get_value(self, time: float, index: int) -> float:
        """
        Retrieve the value on the given index of the channel for
        the time indicated.

        This call will block until the sender publishes the channel
        values for the requested time.

        0 <= `index` < `Channel.recv_size`
        """

    def get_values(self, time: float) -> Tuple[float, ...]:
        """
        Retrieve all values of the channel for the time indicated.

        This call will block until the sender publishes the channel
        values for the requested time.

        Returns `Channel.recv_size` values.
        """

    def set_value(self, value: float, index: int) -> None:
        """
        Store a value in the given index for sending to the remote end.

        0 <= `index` < `Channel.send_size`
        """

    def set_values(self, *values: float) -> None:
        """
        Set all values of the channel.

        Raise an error if the number of values given is not `Channel.send_size`.
        """

    def send(self, time: float) -> None:
        """
        Send the stored values to the remote end, indicating these
        values become valid when the remote end reaches the given time.
        """

    @property
    def id(self) -> int:
        """
        Return the channel id for this channel. (read-only)
        """

    @property
    def send_size(self) -> int:
        """
        Number of channel values that send to the remove end. (read-only)
        """

    @property
    def recv_size(self) -> int:
        """
        Number of channel values are received from the remove end. (read-only)
        """


def initialize_cfg(cfg_path: str) -> None:
    """
    Call this function to start the Co-Simulation Process. Only call this        */
    function once per process.  This function accepts the accepts the host
    and port specified in a configuration file.
    """

def finalize() -> None:
    """
    Call this function to end the Co-Simulation process.
    """
    
class Cosimulation:
    """
    A shim class to support a `with` statement that returns an
    object that manages intialization and finalization of the cosimulation
    library.
    """
    
    def find_channel(self, channel_id: int) -> Channel:
        """
        Find and return a channel object identified by `channel_id`
        """
        return Channel(channel_id)


@contextmanager
def cosimulation(cfg_path: str) -> Cosimulation:
    """
    This function returns an context managed object suitable for use in
    a `with` statement.
    """

    initialize_cfg(cfg_path)
    try:
        yield Cosimulation()
    finally:
        finalize()


# Import the C extension module
try:
    from ._cosim import *
except ImportError:
    pass
else:
    pass
