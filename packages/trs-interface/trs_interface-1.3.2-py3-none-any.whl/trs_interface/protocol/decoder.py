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
The bulk of the ``decoder`` module contains functions to decode raw byte strings to dictionaries
containing the message type and data fields. The majority of these are automatically generated,
and consequently not documented.
Fortunately, a user of the ``protocol`` should not need to know anything about these methods,
and instead simply rely on the :class:`StreamDecoder` to split messages out from a continuous
byte stream (such as serial port data), decode them, and serve the decoded dictionaries.

For example:

.. code-block:: python

    from serial import Serial
    from trs_interface.protocol.decoder import StreamDecoder

    # Open a serial port connection
    serial_port = Serial("/dev/ttyACM0", timeout=0.1, write_timeout=0.1)
    # Create the decoder for received messages
    decoder = StreamDecoder(serial_port, on_error="warn")

    # Split out messages waiting on the serial port and return them
    for msg in decoder:
        print(f"Received message: id={msg.id}={msg.msg}, data={msg.data}, payload={msg.payload}")

Note though that an end user of the ``trs_interface`` should not even need to deal with anything
at the ``protocol`` layer, and instead interact with the device purely through the
:class:`TRSInterface <trs_interface.TRSInterface>` class. 
"""

import io
import struct
import functools
import logging
from collections import namedtuple
from typing import Dict, Any, Optional, Sequence

import numpy as np

from . import HEADER_SIZE, LONG_FORM, ID, Polarity

decoder_for_id = {}
"""Dictionary for looking up a function which can decode data corresponding to a given message ID value."""

_log = logging.getLogger(__name__)

def _decoder(msgid):
    """
    Decorator to indicate a function which decodes a message packet.

    :param msgid: Identification code corresponding to the message.
    """
    def decoder_decorator(func):

        @functools.wraps(func)
        def decoder_wrapper(data_raw: bytes) -> Dict[str, Any]:
            """
            Decode a message header, then pass ``data`` on to the wrapped function.
            
            Messages start with the magic string ``"MSG:"``, followed by a two-byte message ID code,
            and then a 4-byte data field.
            """
            # Decode the message header and ensure it looks sensible
            msg_magic, msg_id, msg_data = struct.unpack_from("<4sHi", data_raw)
            if not msg_magic == b"MSG:":
                raise RuntimeError("Decoded message does not start with 'MSG:' prefix.")
            if not msg_id == msgid:
                raise RuntimeError(f"Decoded message id={msg_id} does not match expected value={id} for '{func.__name__}' messages.")
            # Look at any payload data and ensure it seems formatted correctly
            msg_payload = data_raw[HEADER_SIZE:]
            if len(msg_payload) and not (msg_id & LONG_FORM):
                _log.warn(f"Message packet for '{func.__name__}' id={msg_id:#06x} contains {len(msg_payload)} bytes of unexpected payload data, ignoring.")
                msg_payload = b""
            if len(msg_payload):
                # Long form message, check if fixed length or terminated version
                if msg_data <= 0:
                    # Terminated long form message type
                    if not struct.unpack_from("<i", msg_payload[-4:])[0] == msg_data:
                        _log.warn(f"Message payload for '{func.__name__}' id={msg_id} is not terminated by msg_data={msg_data}, appending.")
                        msg_payload += struct.pack("<i", msg_data)
                else:
                    # Fixed-length long form message type
                    if not len(msg_payload) == msg_data:
                        _log.warn(f"Message payload size={len(msg_payload)} for '{func.__name__}' id={msg_id} doesn't match expected msg_data={msg_data:#010x}, correcting.")
                        msg_data = len(msg_payload)
            msg = {"msg": func.__name__, "id": msg_id, "data": msg_data, "payload": msg_payload}
            # Let the wrapped function decode any further info from the byte data
            msg.update(func(data_raw))
            return msg

        # Add the message id and corresponding decode function to the lookup dictionary
        if msgid in decoder_for_id:
            raise ValueError(f"Duplicated message definition '{func.__name__}' for id={msgid:#x}='{decoder_for_id[msgid].__name__}'.")
        decoder_for_id[msgid] = decoder_wrapper
        return decoder_wrapper

    return decoder_decorator


class StreamDecoder:
    """
    Create a StreamDecoder to decode a byte stream into messages to or from the TRSInterface.

    The ``stream`` parameter should be an object which data can be sourced from.
    It should support the ``read()`` method.

    The ``on_error`` parameter selects the action to take if invalid data is detected.
    If set to ``"continue"`` (the default), bytes will be discarded if the byte sequence
    does not appear to be a valid message.
    If set to ``"warn"``, the behaviour is identical, but a warning message will be emitted.
    To instead immediately abort the stream decoding and raise a ``RuntimeError``, set to
    ``"raise"``.

    :param stream: A data stream from which data can be ``read()`` from.
    :param on_error: Action to take if invalid data is detected.
    """
    def __init__(self, stream=None, on_error="warn"):
        if stream is None:
            self._file = io.BytesIO()
        else:
            self._file = stream
        self.buf = b""
        self.on_error = on_error

    def __iter__(self):
        return self

    def _decoding_error(self, message="Error decoding message from buffer."):
        """
        Take appropriate action if parsing of data stream fails.

        :param message: Warning or error message string.
        """
        if self.on_error == "raise":
            raise RuntimeError(message)
        if self.on_error == "warn":
            _log.warn(message)
        # Discard first byte of buffer, it might decode better now...
        self.buf = self.buf[1:]

    def __next__(self):
        # Basic message packet is MSG_HEADER_SIZE bytes, try to fill buffer to at least that size
        if len(self.buf) < HEADER_SIZE:
            self.buf += self._file.read(HEADER_SIZE - len(self.buf))
        # Hopefully enough data in buffer now to try to decode a message
        while len(self.buf) >= HEADER_SIZE:
            # Ensure the data follows the message format
            msg_magic, msg_id, msg_data = struct.unpack_from("<4sHi", self.buf)
            if not msg_magic == b"MSG:":
                self._decoding_error(f"Invalid message prefix='{msg_magic}'")
                continue
            if not msg_id in decoder_for_id:
                self._decoding_error(f"Invalid message with id={msg_id:#x}")
                continue
            # MSB of id indicates message is a long form type
            long_form = bool(msg_id & LONG_FORM)
            # Message header looks OK, break from loop and proceed
            break                    
        # If we got here, either the buffer was/shrank too small,
        # or we have the start of something that looks like a valid message
        if len(self.buf) < HEADER_SIZE:
            # Not enough data to form a message packet
            raise StopIteration
        # Buffer contains enough for a short message, but maybe not a long form one
        length = 0
        if long_form and msg_data > 0:
            # Long form message, and data field encodes fixed payload length
            length = msg_data
            if len(self.buf) < HEADER_SIZE + length:
                # Not enough data in buffer to decode long form message, attempt to read some more data
                self.buf += self._file.read(length - len(self.buf) + HEADER_SIZE)
                if len(self.buf) < HEADER_SIZE + length:
                    # Still didn't receive enough data to decode message
                    raise StopIteration
        elif long_form and msg_data <= 0:
            # Long form message, and data field encodes (4-byte) terminator for variable length payload
            while (len(self.buf) < HEADER_SIZE + 4) or not (struct.unpack_from("<i", self.buf[-4:])[0] == msg_data):
                # Not enough data in buffer or terminator not found yet
                self.buf += self._file.read(1)
                if (len(self.buf) <= HEADER_SIZE + length):
                    # Another byte wasn't available
                    raise StopIteration
                length = len(self.buf) - HEADER_SIZE
        # Have enough data in buffer to decode the full message
        data = self.buf[:length + HEADER_SIZE]
        # Can now remove the message data from the buffer
        self.buf = self.buf[length + HEADER_SIZE:]
        # Decode the message contents
        msg_dict = decoder_for_id[msg_id](data)
        return namedtuple(msg_dict["msg"], msg_dict.keys())(**msg_dict)

    def feed(self, data: bytes):
        """
        Add byte data to the input stream.

        The input stream must support random access (using the ``seek()`` method), and thus
        is not applicable to sources such as serial port input.

        :param data: Byte array containing data to add.
        """
        pos = self._file.tell()
        self._file.seek(0, 2)
        self._file.write(data)
        self._file.seek(pos)


@_decoder(ID.GET_PING)  # id=0x0000
def get_ping(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GOT_PING)  # id=0x0001
def got_ping(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GOT_UNKNOWN_MSG)  # id=0x0011
def got_unknown_msg(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GET_VERSION)  # id=0x0020
def get_version(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GOT_VERSION)  # id=0x0021 | LONG_FORM
def got_version(data_raw: bytes) -> Dict[str, Any]:
    # Long form message, decode payload data
    _, _, msg_data = struct.unpack_from("<4sHi", data_raw)
    # Omit terminator if terminated style message
    msg_payload = data_raw[HEADER_SIZE:(-4 if msg_data <= 0 else None)]
    return {
        "version": msg_payload.decode("ascii"),
    }

@_decoder(ID.STORE_SETTINGS)  # id=0x08002
def store_settings(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GET_LASER_SYNC_POLARITY)  # id=0x1000
def get_laser_sync_polarity(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GOT_LASER_SYNC_POLARITY)  # id=0x1001
def got_laser_sync_polarity(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.SET_LASER_SYNC_POLARITY)  # id=0x1002
def set_laser_sync_polarity(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GET_CHOPPER_SYNCIN_POLARITY)  # id=0x1010
def get_chopper_syncin_polarity(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GOT_CHOPPER_SYNCIN_POLARITY)  # id=0x1011
def got_chopper_syncin_polarity(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.SET_CHOPPER_SYNCIN_POLARITY)  # id=0x1012
def set_chopper_syncin_polarity(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GET_CHOPPER_SYNCOUT_POLARITY)  # id=0x1020
def get_chopper_syncout_polarity(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GOT_CHOPPER_SYNCOUT_POLARITY)  # id=0x1021
def got_chopper_syncout_polarity(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.SET_CHOPPER_SYNCOUT_POLARITY)  # id=0x1022
def set_chopper_syncout_polarity(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GET_DELAY_TRIG_POLARITY)  # id=0x1030
def get_delay_trig_polarity(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GOT_DELAY_TRIG_POLARITY)  # id=0x1031
def got_delay_trig_polarity(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.SET_DELAY_TRIG_POLARITY)  # id=0x1032
def set_delay_trig_polarity(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GET_CAMERA_TRIG_POLARITY)  # id=0x1050
def get_camera_trig_polarity(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GOT_CAMERA_TRIG_POLARITY)  # id=0x1051
def got_camera_trig_polarity(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.SET_CAMERA_TRIG_POLARITY)  # id=0x1052
def set_camera_trig_polarity(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GET_QUADRATURE_POLARITY)  # id=0x1060
def get_quadrature_polarity(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GOT_QUADRATURE_POLARITY)  # id=0x1061
def got_quadrature_polarity(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.SET_QUADRATURE_POLARITY)  # id=0x1062
def set_quadrature_polarity(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GET_QUADRATURE_DIRECTION)  # id=0x1070
def get_quadrature_direction(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GOT_QUADRATURE_DIRECTION)  # id=0x1071
def got_quadrature_direction(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.SET_QUADRATURE_DIRECTION)  # id=0x1072
def set_quadrature_direction(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GET_CHOPPER_SYNC_DELAY)  # id=0x1100
def get_chopper_sync_delay(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GOT_CHOPPER_SYNC_DELAY)  # id=0x1101
def got_chopper_sync_delay(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.SET_CHOPPER_SYNC_DELAY)  # id=0x1102
def set_chopper_sync_delay(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GET_CHOPPER_SYNC_DURATION)  # id=0x1110
def get_chopper_sync_duration(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GOT_CHOPPER_SYNC_DURATION)  # id=0x1111
def got_chopper_sync_duration(data_raw: bytes) -> Dict[str, Any]:
    # Data is unsigned int
    return {
        "data" : struct.unpack_from("I", data_raw, offset=6)[0]
    }

@_decoder(ID.SET_CHOPPER_SYNC_DURATION)  # id=0x1112
def set_chopper_sync_duration(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GET_CAMERA_SYNC_DELAY)  # id=0x1120
def get_camera_sync_delay(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GOT_CAMERA_SYNC_DELAY)  # id=0x1121
def got_camera_sync_delay(data_raw: bytes) -> Dict[str, Any]:
    # Data is unsigned int
    return {
        "data" : struct.unpack_from("I", data_raw, offset=6)[0]
    }

@_decoder(ID.SET_CAMERA_SYNC_DELAY)  # id=0x1122
def set_camera_sync_delay(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GET_CAMERA_SYNC_DURATION)  # id=0x1130
def get_camera_sync_duration(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GOT_CAMERA_SYNC_DURATION)  # id=0x1131
def got_camera_sync_duration(data_raw: bytes) -> Dict[str, Any]:
    # Data is unsigned int
    return {
        "data" : struct.unpack_from("I", data_raw, offset=6)[0]
    }

@_decoder(ID.SET_CAMERA_SYNC_DURATION)  # id=0x1132
def set_camera_sync_duration(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GET_CHOPPER_DIVIDER)  # id=0x1200
def get_chopper_divider(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GOT_CHOPPER_DIVIDER)  # id=0x1201
def got_chopper_divider(data_raw: bytes) -> Dict[str, Any]:
    # Data is unsigned int
    return {
        "data" : struct.unpack_from("I", data_raw, offset=6)[0]
    }

@_decoder(ID.SET_CHOPPER_DIVIDER)  # id=0x1202
def set_chopper_divider(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GET_QUADRATURE_VALUE)  # id=0x1210
def get_quadrature_value(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GOT_QUADRATURE_VALUE)  # id=0x1211
def got_quadrature_value(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.SET_QUADRATURE_VALUE)  # id=0x1212
def set_quadrature_value(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.ARM)  # id=0x2008
def arm(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.START)  # id=0x2018
def start(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.STOP)  # id=0x2019
def stop(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GOT_DATA)  # id=0x4001
def got_data(data_raw: bytes) -> Dict[str, Any]:
    # Long form message, decode payload data
    _, _, msg_data = struct.unpack_from("<4sHi", data_raw)
    # Omit terminator if terminated style message
    msg_payload = np.frombuffer(data_raw[HEADER_SIZE:(-4 if msg_data <= 0 else None)], dtype=np.int32)
    # Quadrature value is top 31 bits (2x), chopper on/off is last bit (even/odd)
    return {
        "quadrature": msg_payload >> 1,
        "chopper": (msg_payload & 0x1).astype(bool)
    }

@_decoder(ID.GET_LASER_SYNC_PERIOD)  # id=0x4100
def get_laser_sync_period(data_raw: bytes) -> Dict[str, Any]:
    return {}

@_decoder(ID.GOT_LASER_SYNC_PERIOD)  # id=0x4101
def got_laser_sync_period(data_raw: bytes) -> Dict[str, Any]:
    # Data is unsigned int
    return {
        "data" : struct.unpack_from("I", data_raw, offset=6)[0]
    }