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
The ``trs_interface`` package is responsible for the host (computer) side of communications
and control of the TRSpectrometer interface hardware.

The most important part of the package is the :class:`TRSInterface` class.
This will handle all of a typical user's needs when communicating with the device.

Example usage:

.. code-block:: python

    from trs_interface import TRSInterface
    trsi = TRSInterface()

    # Initialise other associated hardware devices
    # delay = ... motorised delay stage
    # chopper = ... optical chopper wheel
    # camera = ... detector

    # Do any required configuration
    trsi.set_chopper_divider = 4
    trsi.set_chopper_delay = 50          # == 1.2 us (units of 1/42 MHz, ~24 ns)
    trsi.set_camera_sync_delay = 75      # == 1.8 us
    trsi.set_camera_sync_duration = 100  # == 2.4 us

    # Set up a handler for when data is received
    data = (None, None)
    def data_handler(quad_pos, chop_state):
        global data
        print(f"Received {data[0].shape[0]} data points.")
        data = (quad_pos, chop_state)
    trsi.register_data_callback(data_handler)

    # Set up a handler to be notified immediately if the connection fails
    def error_handler(message):
        print(f"Error: {message}")
    trsi.register_error_callback(error_handler)

    # Move delay to starting position
    delay.move_absolute(0)

    # Arm the device so it's waiting for start trigger from delay
    trsi.arm()

    # Start the move
    delay.move_absolute(12345678)
    # ... wait

    # Do something with the data
    print(data)

The status of the device can be queried using the :data:`~TRSInterface.status` property.
This is a dictionary containing the fields:

* ``"connected"``
* ``"laser_sync_polarity"``
* ``"chopper_syncin_polarity"``
* ``"chopper_syncout_polarity"``
* ``"delay_trig_polarity"``
* ``"camera_trig_polarity"``
* ``"quadrature_polarity"``
* ``"quadrature_direction"``
* ``"chopper_sync_delay"``
* ``"chopper_sync_duration"``
* ``"camera_sync_delay"``
* ``"camera_sync_duration"``
* ``"chopper_divider"``
* ``"quadrature_value"``
* ``"laser_sync_period"``

Class properties are also implemented so that the values can be queried or set easily, for example:

.. code-block:: python

    # Print the current quadrature value
    print(trsi.quadrature_value)
    # Set the camera sync pulse duration to 2.952 us (units of 1/42 MHz, ~24 ns)
    trsi.camera_sync_duration = 123;

To configure signal polarities or quadrature directions, some enumerations are defined in the :mod:`~trs_interface.protocol` package:

.. code-block:: python

    from trs_interface.protocol import Polarity, Direction

    # Laser input sync on falling edge of signal
    trsi.laser_sync_polarity = Polarity.FALLING
    # Delay input signal active low
    trsi.delay_trig_polarity = Polarity.LOW
    # Invert quadrature counting direction
    trsi.quadrature_direction = Direction.REVERSE
"""

__version__ = "1.3.2"

import logging
import asyncio
from threading import Thread
import atexit
import re

import serial
from serial.tools import list_ports, list_ports_common

from .protocol import encoder, ID
from .protocol.decoder import StreamDecoder

class TRSInterface():
    """
    Initialise and open serial device for the TRSInterface device.

    If the ``serial_port`` parameter is ``None`` (default), then an attempt to detect the device
    will be performed.
    The first device found will be returned.
    If multiple devices are attached to the system, the ``location`` parameter may be used to select the correct device.
    Location refers to the USB bus and port identifier the device is plugged in to, for example "1-14:1.0".
    This is a regular expression match, for example ``location="14"`` would match devices with "14" anywhere in the location string,
    while ``location=".*14$"`` would match locations ending in 14.

    :param serial_port: Serial port device the device is connected to.
    :param location: Regular expression matching the serial number of device to search for.
    """
 
    def __init__(self, serial_port=None, location=""):
        
        # If serial_port not specified, search for a device
        if serial_port is None:
            serial_port = find_device(location=location)

        # Accept a serial.tools.list_ports.ListPortInfo object (which we may have just found)
        if isinstance(serial_port, list_ports_common.ListPortInfo):
            serial_port = serial_port.device
        
        if serial_port is None:
            if location:
                msg = f"No TRSInterface devices detected with location matching '{location}'."
            else:
                msg = "No TRSInterface devices detected."
            raise RuntimeError(msg)

        self._log = logging.getLogger(__name__)
        self._log.debug(f"Initialising serial port ({serial_port}).")
        # Open and configure serial port settings
        self._port = serial.Serial(serial_port, timeout=0.1, write_timeout=0.1)
        self._log.debug("Opened serial port OK.")

        self.status = {
            "connected" : True,
            "ping" : None,
            "version" : None,
            "laser_sync_polarity" : None,
            "chopper_syncin_polarity" : None,
            "chopper_syncout_polarity" : None,
            "delay_trig_polarity" : None,
            "camera_trig_polarity" : None,
            "quadrature_polarity" : None,
            "quadrature_direction" : None,
            "chopper_sync_delay" : None,
            "chopper_sync_duration" : None,
            "camera_sync_delay" : None,
            "camera_sync_duration" : None,
            "chopper_divider" : None,
            "quadrature_value" : None,
            "laser_sync_period" : None,
        }
        """Dictionary of status properties for the device."""

        # Decoder for received messages
        self._decoder = StreamDecoder(self._port, on_error="warn")

        # List of functions to call when data is received
        self._data_callbacks = set()

        # List of functions to call if a connection error occurs
        self._error_callbacks = set()

        # Create a new event loop for ourselves to queue and send commands
        self._loop = asyncio.new_event_loop()

        # Schedule the first check for incoming data on the serial port
        self._loop.call_soon(self._schedule_reads)
        self.read_interval = 0.01
        """Time to wait between read attempts on the serial port, in seconds."""

        # Schedule the first check for updated quadrature value
        self._update_handle = self._loop.call_soon(self._schedule_updates)
        self.update_interval = 0.1
        """Time to wait between read queries of the device status, such as current quadrature decoder value."""

        # Get values for status properties
        for name in self.status:
            if not name == "connected":
                self._loop.call_soon(self._write, encoder.pack(ID[f"GET_{name.upper()}"]))

        # Create a new thread to run the event loop in
        self._thread = Thread(target=self._run_eventloop)
        # Set as daemon thread so it can be killed automatically at program exit
        self._thread.daemon = True
        self._thread.start()

        # Close the serial port at exit in case close() wasn't called
        atexit.register(self._atexit)

    def _run_eventloop(self):
        """
        Entry point for the event loop thread.
        """
        self._log.debug("Starting event loop.")
        asyncio.set_event_loop(self._loop)
        try:
            self._loop.run_forever()
        finally:
            self._loop.close()
            self._loop = None
        self._log.debug("Event loop stopped.")
        self._close_port()

    def _close_port(self):
        """
        Close the serial port connection to the device.
        """
        if self._port is not None:
            self._log.debug("Closing serial connection.")
            self._port.close()
            self._port = None

    def _atexit(self):
        """
        Catch exit signal and attempt to close everything gracefully.
        """
        # Request the event loop to stop
        self.close()
        # Wait for event loop thread to finish
        self._thread.join()

    def _write(self, message_bytes):
        """
        Write a message out the the serial port.

        :param message_bytes: Message to send to the device as raw byte array.
        """
        #self._log.debug(f"Writing command bytes: {message_bytes}")
        try:
            self._port.write(message_bytes)
            self._port.flush()
        except serial.serialutil.SerialException:
            msg = "Unable to write to serial port (device disconnected?)"
            self._log.error(msg)
            self.status["connected"] = False
            self.close()
            # Notify listeners of error
            for cb in self._error_callbacks:
                cb(msg)

    def _schedule_reads(self):
        """
        Check for any incoming messages and process them at regular intervals.
        """
        #self._log.debug(f"Checking for data on serial port.")
        try:
            for msg in self._decoder:
                #self._log.debug(f"Received message: {msg}")
                self._process_message(msg)
            # Schedule next check
            self._loop.call_later(self.read_interval, self._schedule_reads)
        except serial.serialutil.SerialException:
            msg = "Unable to read from serial port (device disconnected?)"
            self._log.error(msg)
            self.status["connected"] = False
            self.close()
            # Notify listeners of error
            for cb in self._error_callbacks:
                cb(msg)

    def _schedule_updates(self):
        """
        Request updated device status at regular intervals.
        """
        if self.status["connected"]:
            self._loop.call_soon_threadsafe(self._write, encoder.get_quadrature_value())
            self._loop.call_soon_threadsafe(self._write, encoder.get_laser_sync_period())
            # Schedule next check
            self._update_handle = self._loop.call_later(self.update_interval, self._schedule_updates)

    def _process_message(self, m):
        """
        Process a single message from the device.

        :param m: The decoded message from the controller.
        """
        action, _, name = m.msg.partition("_")
        if m.msg == "got_data":
            # Pass data to registered receivers
            for cb in self._data_callbacks:
                cb(m.quadrature, m.chopper)
            # Restart status update requests
            self._update_handle.cancel()
            self._update_handle = self._loop.call_soon_threadsafe(self._schedule_updates)
        elif m.msg == "got_version":
            # Use version string in payload of long-form message
            self.status["version"] = m.version
        elif action == "got" and name in self.status:
            # Update value in status dictionary
            self.status[name] = m.data
        else:
            self._log.warn(f"Unhandled message: {m.msg}")

    def register_data_callback(self, callback_function):
        """
        Register a function to be called when data is received from the device.

        The function passed in should have the signature ``callback_function(quadrature, chopper)``,
        where ``quadrature`` is the value for the quadrature encoder as a numpy array of signed integers (np.uint32)
        and ``chopper`` is the state of the chopper ("on" or "off") as a numpy array of boolean values.

        :param callback_function: Function to call when data is received.
        """
        if callable(callback_function):
            self._data_callbacks.add(callback_function)
        else:
            self._log.warn("Attempted to register a non-callable object as a callback function.")

    def unregister_data_callback(self, callback_function):
        """
        Unregister a previously registered callback function.

        The function passed in should have been previously registered using :meth:`register_data_callback`.

        :param callback_function: Function to unregister.
        """
        if callback_function not in self._data_callbacks:
            self._log.warn("Attemped to unregister an unknown function.")
        else:
            self._data_callbacks.remove(callback_function)

    def register_error_callback(self, callback_function):
        """
        Register a function to be called if there is an error communicating with the device.

        The function passed in should have the signature ``callback_function(message)``,
        where ``message`` is a string describing the error.

        :param callback_function: Function to call when a connection error occurs.
        """
        if callable(callback_function):
            self._error_callbacks.add(callback_function)
        else:
            self._log.warn("Attempted to register a non-callable object as a callback function.")

    def unregister_error_callback(self, callback_function):
        """
        Unregister a previously registered error callback function.

        The function passed in should have been previously registered using :meth:`register_error_callback`.

        :param callback_function: Function to unregister.
        """
        if callback_function not in self._error_callbacks:
            self._log.warn("Attemped to unregister an unknown function.")
        else:
            self._error_callbacks.remove(callback_function)

    def close(self):
        """
        Close the serial connection to the device.
        """
        if self._loop is not None:
            self._log.debug("Stopping event loop.")
            self._loop.call_soon_threadsafe(self._loop.stop)
        # Note, this returns before event loop has actually stopped and serial port closed

    def __getattr__(self, name):
        """
        Intercept ``__getattr__`` calls for class properties which match valid device :data:`status` parameters.

        Allows the use of parameter names as class properties, for example ``q = device.quadrature_value``
        instead of ``q = device.status["quadrature_value"]``.
        """
        if "status" in self.__dict__ and name in self.status:
            if (self._loop is None or not self.status["connected"]) and not name == "connected":
                raise ConnectionError("Connection to serial device failed.") 
            return self.status[name]
        else:
            raise AttributeError(f"Attempt to get invalid status property '{name}'.")

    def __setattr__(self, name, value):
        """
        Intercept __setattr__ calls for class properties which match valid device :data:`status` parameters.

        Allows the use of feature names as class properties, for example ``device.quadrature_value = 0``.
        """
        if "status" in self.__dict__ and name in self.status:
            if self._loop is None or not self.status["connected"]:
                raise ConnectionError("Connection to serial device failed.")
            if name == "ping":
                # Ping is a special case, no "set" message, but repeats data value sent in "get" message
                self._loop.call_soon_threadsafe(self._write, encoder.get_ping(value))
            else:
                try:
                    # Normal parameter, set value, then query to update real value from device
                    self._loop.call_soon_threadsafe(self._write, encoder.pack(ID[f"SET_{name.upper()}"], value))
                    self._loop.call_soon_threadsafe(self._write, encoder.pack(ID[f"GET_{name.upper()}"]))
                except KeyError:
                    # Likely a read-only value such as laser sync period
                    self._log.warn(f"Couldn't set value for read-only property: {name}")
        else:
            super().__setattr__(name, value)
  
    def arm(self):
        """
        Arm the device to start collecing data on hardware trigger signal from the delay stage.
        """
        if self._loop is None or not self.status["connected"]:
            raise ConnectionError("Connection to serial device failed.")
        # Stop requesting status updates, as they'll cancel the arm status
        self._update_handle.cancel()
        self._loop.call_soon_threadsafe(self._write, encoder.arm(True))

    def start(self, frame_count=0):
        """
        Instruct the device to start collecting data immediately.
        """
        if self._loop is None or not self.status["connected"]:
            raise ConnectionError("Connection to serial device failed.")
        # Stop requesting status updates
        self._update_handle.cancel()
        self._loop.call_soon_threadsafe(self._write, encoder.start(frame_count))

    def stop(self):
        """
        Instruct the device to stop collecting data, or exit the :meth:`arm` mode.
        """
        if self._loop is None or not self.status["connected"]:
            raise ConnectionError("Connection to serial device failed.")
        self._loop.call_soon_threadsafe(self._write, encoder.stop())
        # Restart requests for status updates
        self._update_handle.cancel()
        self._update_handle = self._loop.call_soon_threadsafe(self._schedule_updates)
    
    def store_settings(self):
        """
        Instruct the device to store its current settings to flash memory.
        
        The settings will be used as defaults when powered on in the future.
        """
        if self._loop is None or not self.status["connected"]:
            raise ConnectionError("Connection to serial device failed.")
        self._loop.call_soon_threadsafe(self._write, encoder.store_settings())


def find_device(location=""):
    """
    Search attached serial ports for a TRSInterface device.

    The first device found will be returned.
    If multiple devices are attached to the system, the ``location`` parameter may be used to select the correct device.
    Location refers to the USB bus and port identifier the device is plugged in to, for example "1-14:1.0".
    This is a regular expression match, for example ``location="14"`` would match devices with "14" anywhere in the location string,
    while ``location=".*14$"`` would match locations ending in 14.

    :param location: Regular expression to match a device USB location.
    """
    for p in serial.tools.list_ports.comports():
        # If manufacturer and product fields exist, try to use them
        # If a location is provided, require a match
        if ((p.vid == 0x2341) and (p.pid == 0x003e)
            and (re.match(location, p.location) if p.location else True)):
            return p
