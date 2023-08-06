# Copyright 2021 Patrick C. Tapping
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

"""
The bulk of the ``encoder`` module contains functions to encode data to raw byte strings.
The majority of these are automatically generated, and consequently not documented.
Fortunately, they should be fairly straightforward to use.

For example:

.. code-block:: python

    from trs_interface.protocol import encoder

    # Times are integers measured in units of 1/42 MHz (~24 ns)
    msg = encoder.set_camera_sync_delay(50)  # == 2.083 µs

    msg = encoder.set_quadrature_value(0)

    msg = encoder.arm()
   
"""

import warnings
import struct
from typing import Optional

import numpy as np
from numpy.typing import ArrayLike

from . import LONG_FORM, ID

def pack(msg_id: int, data: int=0, payload: Optional[bytes]=None):
    """
    Pack a message into a byte array.

    :param msg_id: ID code of message type.
    :param data: Data to put into the 32-bit data field.
    :param payload: Byte array containing additional payload data appended to the message.
    :returns: Byte array representing the message and data.
    """
    long_form = bool(msg_id & LONG_FORM)
    if not long_form and payload:
        raise ValueError(f"Can't pack a header only message type id={msg_id} with payload data.")
    if long_form and payload is None:
        # We can pack a message with a zero length payload I suppose...
        warnings.warn(f"Packing a message id={msg_id} with zero length payload (data field ignored).")
        data = 0
        payload = b""
    if payload is not None and data > 0:
        # Fixed size message, data field should be payload size
        data = len(payload)
    elif payload is not None and data <= 0:
        # Variable sized (terminated) message, data should be terminator bytes
        if not struct.unpack_from("<i", payload[:-4]) == data:
            # Payload doesn't end with terminator bytes, add them
            warnings.warn(f"Payload does not end with terminator bytes given by data={data:#06x}, appending terminator.")
            payload += struct.pack("<i", data)
    else:
        # Header-only message, no payload
        payload = b""
    return struct.pack("<4sHi", b"MSG:", msg_id, data) + payload


def get_ping(ping:int=0) -> bytes:
    return pack(ID.GET_PING, data=ping)

def got_ping(ping:int=0) -> bytes:
    return pack(ID.GOT_PING, data=ping)

def got_unknown_msg(msg:int=0) -> bytes:
    return pack(ID.GOT_UNKNOWN_MSG, data=msg)

def get_version(version:int=0) -> bytes:
    return pack(ID.GET_VERSION, data=version)

def got_version(version:str="0.0.0") -> bytes:
    v = version.encode("ascii")
    return pack(ID.GOT_VERSION, data=len(v), payload=v)

def store_settings(settings:int=0) -> bytes:
    return pack(ID.STORE_SETTINGS, data=settings)

def get_laser_sync_polarity(polarity:int=0) -> bytes:
    return pack(ID.GET_LASER_SYNC_POLARITY, data=polarity)

def got_laser_sync_polarity(polarity:int=0) -> bytes:
    return pack(ID.GOT_LASER_SYNC_POLARITY, data=polarity)

def set_laser_sync_polarity(polarity:int=0) -> bytes:
    return pack(ID.SET_LASER_SYNC_POLARITY, data=polarity)

def get_chopper_syncin_polarity(polarity:int=0) -> bytes:
    return pack(ID.GET_CHOPPER_SYNCIN_POLARITY, data=polarity)

def got_chopper_syncin_polarity(polarity:int=0) -> bytes:
    return pack(ID.GOT_CHOPPER_SYNCIN_POLARITY, data=polarity)

def set_chopper_syncin_polarity(polarity:int=0) -> bytes:
    return pack(ID.SET_CHOPPER_SYNCIN_POLARITY, data=polarity)

def get_chopper_syncout_polarity(polarity:int=0) -> bytes:
    return pack(ID.GET_CHOPPER_SYNCOUT_POLARITY, data=polarity)

def got_chopper_syncout_polarity(polarity:int=0) -> bytes:
    return pack(ID.GOT_CHOPPER_SYNCOUT_POLARITY, data=polarity)

def set_chopper_syncout_polarity(polarity:int=0) -> bytes:
    return pack(ID.SET_CHOPPER_SYNCOUT_POLARITY, data=polarity)

def get_delay_trig_polarity(polarity:int=0) -> bytes:
    return pack(ID.GET_DELAY_TRIG_POLARITY, data=polarity)

def got_delay_trig_polarity(polarity:int=0) -> bytes:
    return pack(ID.GOT_DELAY_TRIG_POLARITY, data=polarity)

def set_delay_trig_polarity(polarity:int=0) -> bytes:
    return pack(ID.SET_DELAY_TRIG_POLARITY, data=polarity)

def get_camera_trig_polarity(polarity:int=0) -> bytes:
    return pack(ID.GET_CAMERA_TRIG_POLARITY, data=polarity)

def got_camera_trig_polarity(polarity:int=0) -> bytes:
    return pack(ID.GOT_CAMERA_TRIG_POLARITY, data=polarity)

def set_camera_trig_polarity(polarity:int=0) -> bytes:
    return pack(ID.SET_CAMERA_TRIG_POLARITY, data=polarity)

def get_quadrature_polarity(polarity:int=0) -> bytes:
    return pack(ID.GET_QUADRATURE_POLARITY, data=polarity)

def got_quadrature_polarity(polarity:int=0) -> bytes:
    return pack(ID.GOT_QUADRATURE_POLARITY, data=polarity)

def set_quadrature_polarity(polarity:int=0) -> bytes:
    return pack(ID.SET_QUADRATURE_POLARITY, data=polarity)

def get_quadrature_direction(direction:int=0) -> bytes:
    return pack(ID.GET_QUADRATURE_DIRECTION, data=direction)

def got_quadrature_direction(direction:int=0) -> bytes:
    return pack(ID.GOT_QUADRATURE_DIRECTION, data=direction)

def set_quadrature_direction(direction:int=0) -> bytes:
    return pack(ID.SET_QUADRATURE_DIRECTION, data=direction)

def get_chopper_sync_delay(delay:int=0) -> bytes:
    return pack(ID.GET_CHOPPER_SYNC_DELAY, data=delay)

def got_chopper_sync_delay(delay:int=0) -> bytes:
    return pack(ID.GOT_CHOPPER_SYNC_DELAY, data=delay)

def set_chopper_sync_delay(delay:int=0) -> bytes:
    return pack(ID.SET_CHOPPER_SYNC_DELAY, data=delay)

def get_chopper_sync_duration(duration:int=0) -> bytes:
    return pack(ID.GET_CHOPPER_SYNC_DURATION, data=duration)

def got_chopper_sync_duration(duration:int=0) -> bytes:
    return pack(ID.GOT_CHOPPER_SYNC_DURATION, data=duration)

def set_chopper_sync_duration(duration:int=0) -> bytes:
    return pack(ID.SET_CHOPPER_SYNC_DURATION, data=duration)

def get_camera_sync_delay(delay:int=0) -> bytes:
    return pack(ID.GET_CAMERA_SYNC_DELAY, data=delay)

def got_camera_sync_delay(delay:int=0) -> bytes:
    return pack(ID.GOT_CAMERA_SYNC_DELAY, data=delay)

def set_camera_sync_delay(delay:int=0) -> bytes:
    return pack(ID.SET_CAMERA_SYNC_DELAY, data=delay)

def get_camera_sync_duration(duration:int=0) -> bytes:
    return pack(ID.GET_CAMERA_SYNC_DURATION, data=duration)

def got_camera_sync_duration(duration:int=0) -> bytes:
    return pack(ID.GOT_CAMERA_SYNC_DURATION, data=duration)

def set_camera_sync_duration(duration:int=0) -> bytes:
    return pack(ID.SET_CAMERA_SYNC_DURATION, data=duration)

def get_chopper_divider(divider:int=0) -> bytes:
    return pack(ID.GET_CHOPPER_DIVIDER, data=divider)

def got_chopper_divider(divider:int=0) -> bytes:
    return pack(ID.GOT_CHOPPER_DIVIDER, data=divider)

def set_chopper_divider(divider:int=0) -> bytes:
    return pack(ID.SET_CHOPPER_DIVIDER, data=divider)

def get_quadrature_value(value:int=0) -> bytes:
    return pack(ID.GET_QUADRATURE_VALUE, data=value)

def got_quadrature_value(value:int=0) -> bytes:
    return pack(ID.GOT_QUADRATURE_VALUE, data=value)

def set_quadrature_value(value:int=0) -> bytes:
    return pack(ID.SET_QUADRATURE_VALUE, data=value)

def arm(arm:int=1) -> bytes:
    return pack(ID.ARM, data=arm)

def start(frame_count:int=0) -> bytes:
    return pack(ID.START, data=frame_count)

def stop(stop:int=0) -> bytes:
    return pack(ID.STOP, data=stop)

def got_data(quadrature:ArrayLike=[], chopper:ArrayLike=[]) -> bytes:
    """
    Message containing data in its payload.

    The array sizes of ``quadrature`` and ``chopper`` should match, or one parameter may be a single value.

    :param quadrature: Values of the quadrature encoder, as array of signed integers.
    :param chopper: Chopper "on" or "off" values, as array of boolean values.
    """
    # Long form message, encode payload data and set data to payload size
    payload = ((quadrature.astype(np.int32) << 1) + chopper.astype(bool)).tobytes()
    data = len(payload)
    return pack(ID.GOT_DATA, data=data) + payload

def get_laser_sync_period(period:int=0) -> bytes:
    return pack(ID.GET_LASER_SYNC_PERIOD, data=period)

def got_laser_sync_period(period:int=0) -> bytes:
    return pack(ID.GOT_LASER_SYNC_PERIOD, data=period)