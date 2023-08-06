"""Class module for the Inmarsat IDP Plug-N-Play Developer Kit Dongle.
"""

from __future__ import absolute_import

from asyncio import AbstractEventLoop, run
from atexit import register as on_exit
from logging import Logger, INFO, DEBUG
from platform import machine
from signal import signal, SIGINT, SIGTERM
from threading import current_thread
from time import sleep
from typing import Callable
from warnings import filterwarnings, warn

from gpiozero import DigitalInputDevice, DigitalOutputDevice, CallbackSetToNone
from gpiozero import Factory as PinFactory
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero.pins.mock import MockFactory

from idpmodem.atcommand_async import IdpModemAsyncioClient
from idpmodem.constants import CONTROL_STATES, BEAMSEARCH_STATES
from idpmodem.constants import FORMAT_B64
from idpmodem.utils import get_wrapping_logger


class PnpDongle:
    """Represents the Plug-N-Play Dongle used in the IDP developer kit.

    A Raspberry Pi Zero W hosts an application and controls UART/RS232 and
    the modem's input and output lines:
    
        * Event notification (output) controlled by modem register ``S88``
        * Modem reset (input)
        * External reset (output) asserts based on certain messages received
          over the satellite
        * 1 Pulse-per-second (output) that can be configured to provide GNSS
          synchronized pulses.

    Attributes:
        modem (IdpModemAsyncioClient): The IsatData Pro modem (``idpmodem``)
        port (str): The serial port the modem is connected to
        mode (str): The mode of communication with the IDP modem (ST2100)
            
            * ``master`` allows the Pi0W to communicate
            * ``transparent`` allows a separate device to communicate
            * ``proxy`` allows the Pi0W to intercept modem output to a client

        modem_event_callback (Callable): Will be called back if notifications
            are enabled.
        external_reset_callback (Callable): Will be called back if an over-
            the-air command asserts the external reset pin.
        pps_pulse_callback (Callable): Will be called back if pulse-per-second
            is enabled and GNSS refresh is every 1 second.
        pin_factory (PinFactory): A gpiozero pin factory mapping GPIO pins
        gpio (dict): Provides access and configuration of the GPIO pins
    """
    
    PIN_EVENT_NOTIFY = 9
    PIN_PPS = 10
    PIN_EXTERNAL_RESET = 11
    PIN_MODEM_RESET = 26
    PIN_RL1A_DIR = 27
    PIN_RL1B_DIR = 22
    PIN_RL2A_DIR = 23
    PIN_RL2B_DIR = 24
    PIN_TRS3221E_ON = 7
    PIN_TRS3221E_OFF = 8
    PIN_TRS3221E_INVALID_NOT = 25
    UART_NAME = '/dev/ttyS0'
    SUPPORTED_ARCHITECTURES = {
        'armv6': 'Raspberry Pi Zero W'
    }

    MODES = ['master', 'proxy', 'transparent']
    GPIO = [
        'RL1A',
        'RL1B',
        'RL2A',
        'RL2B',
        'RS232_ON',
        'RS232_NOT_OFF',
        'RS232_NOT_INVALID',
        'MODEM_EVENT',
        'MODEM_RESET',
        'APP_RESET',
        'PULSE_PER_SEC',
    ]

    def __init__(self,
                 logger: Logger = None,
                 log_level: int = INFO,
                 modem_event_callback: Callable = None,
                 external_reset_callback: Callable = None,
                 pps_pulse_callback: Callable = None,
                 mode: str = 'master',
                 loop: AbstractEventLoop = None,
                 port: str = None,
                 pin_factory: PinFactory = None):
        """Initializes the dongle.
        
        Args:
            logger: Optional logger, one will be created if not supplied.
            log_level: The default logging level.
            modem_event_callback: Optional callback when notification asserts.
            external_reset_callback: Optional callback triggered by remote reset.
            pps_pulse_callback: Optional receiver for GNSS pulse per second.
            mode: `master`, `proxy` or `transparent`.
            loop: (Optional) asyncio event loop
            port: (Optional) override the default on-board UART
            pin_factory: (Optional) override the auto-detected gpiozero factory
            
        """
        on_exit(self._cleanup)
        signal(SIGINT, self._cleanup)
        signal(SIGTERM, self._cleanup)
        filterwarnings('ignore', category=CallbackSetToNone)
        self._log = logger or get_wrapping_logger(log_level=log_level)
        self.port = port
        self._loop = loop
        self.modem = IdpModemAsyncioClient(port=self.port,
                                           logger=self._log,
                                           loop=self._loop)
        self.pin_factory = pin_factory or self._pin_factory_get()
        self.gpio = dict()
        self._gpio_setup(modem_event_callback=modem_event_callback,
                         external_reset_callback=external_reset_callback,
                         pps_pulse_callback=pps_pulse_callback)
        self.mode = mode
    
    @property
    def port(self):
        return self._port
    
    @port.setter
    def port(self, value: str):
        self._port = value if value is not None else self.UART_NAME

    def _reset_relays(self):
        """Resets the dongle relays to ensure expected state."""
        self._log.debug('Resetting relays')
        self.gpio['RL1B'].blink(n=1, background=False)
        self.gpio['RL2B'].blink(n=1, background=False)

    def _pin_factory_get(self):
        """Sets up the GPIOzero PinFactory based on architecture.
        
        Pi Zero W is arm6.
        """
        sys_arch = machine().lower()
        if any(arch in sys_arch for arch in self.SUPPORTED_ARCHITECTURES):
            try:
                return PiGPIOFactory()
            except OSError as e:
                self._log.warning('Using NativeFactory pins'
                    ' since could not load pigpio ({})'.format(e))
                return None
        else:   #: must be running in test mode not Pi Zero W
            if self._port == self.UART_NAME:
                err_msg = 'Serial {} unsupported on {}'.format(
                    self._port, sys_arch)
                self._log.error(err_msg)
                raise ValueError(err_msg)
            self._log.warning('Detected platform {}'.format(machine()) +
                '...using gpiozero MockFactory for development purposes')
            return MockFactory()

    def _gpio_setup(self,
                    modem_event_callback: Callable = None,
                    external_reset_callback: Callable = None,
                    pps_pulse_callback: Callable = None):
        """Initializes the Raspbery Pi GPIO."""
        self.gpio = {
            'RL1A': DigitalOutputDevice(pin=self.PIN_RL1A_DIR,
                                        initial_value=None,
                                        pin_factory=self.pin_factory),
            'RL1B': DigitalOutputDevice(pin=self.PIN_RL1B_DIR,
                                        initial_value=None,
                                        pin_factory=self.pin_factory),
            'RL2A': DigitalOutputDevice(pin=self.PIN_RL2A_DIR,
                                        initial_value=None,
                                        pin_factory=self.pin_factory),
            'RL2B': DigitalOutputDevice(pin=self.PIN_RL2B_DIR,
                                        initial_value=None,
                                        pin_factory=self.pin_factory),
            'RS232_ON': DigitalOutputDevice(pin=self.PIN_TRS3221E_ON,
                                            initial_value=None,
                                            pin_factory=self.pin_factory),
            'RS232_NOT_OFF': DigitalOutputDevice(pin=self.PIN_TRS3221E_OFF,
                                                 initial_value=None,
                                                 pin_factory=self.pin_factory),
            'RS232_NOT_INVALID': DigitalInputDevice(
                                    pin=self.PIN_TRS3221E_INVALID_NOT,
                                    pull_up=False,
                                    pin_factory=self.pin_factory),
            'MODEM_EVENT': DigitalInputDevice(pin=self.PIN_EVENT_NOTIFY,
                                              pull_up=False,
                                              pin_factory=self.pin_factory),
            'MODEM_RESET': DigitalOutputDevice(pin=self.PIN_MODEM_RESET,
                                               initial_value=None,
                                               pin_factory=self.pin_factory),
            'APP_RESET': DigitalInputDevice(pin=self.PIN_EXTERNAL_RESET,
                                            pull_up=False,
                                            pin_factory=self.pin_factory),
            'PULSE_PER_SEC': DigitalInputDevice(pin=self.PIN_PPS,
                                                pull_up=False,
                                                pin_factory=self.pin_factory),
        }
        self.modem_event_callback = modem_event_callback
        if not modem_event_callback:
            self._log.warning('No modem_event_callback defined')
        self.gpio['MODEM_EVENT'].when_activated = (
            modem_event_callback or self._event_activated)
        self._event_data_last = None
        self.gpio['APP_RESET'].when_activated = (
            external_reset_callback)
        if not external_reset_callback:
            self._log.debug('No external_reset_callback defined')
        self.gpio['PULSE_PER_SEC'].when_activated = pps_pulse_callback
        if pps_pulse_callback:
            self.pps_enable()
        else:
            self._log.debug('1PPS output not enabled')
        self._reset_relays()
        pass

    def pin_factory_change(self,
                           pin_factory: PinFactory,
                           gpio_name: str = 'ALL'):
        """Changes the PinFactory of the target GPIO (or all if none specified).
        
        Args:
            pin_factory (PinFactory): The new GPIOzero pin factory
            gpio_name (str): The name of the GPIO or `ALL`

        Raises:
            ValueError if gpio_name is not defined.

        """
        if gpio_name != 'ALL' and gpio_name not in self.gpio:
            raise ValueError('gpio[\'{}\'] not defined'.format(gpio_name))
        if isinstance(pin_factory, MockFactory):
            factory_name = 'MockFactory'
        elif isinstance(pin_factory, PiGPIOFactory):
            factory_name = 'PiGPIOFactory'
        elif pin_factory is None:
            factory_name = 'None'
        else:
            factory_name = 'Unsupported'
        self._log.warning('Attempting to change pin factory to {} for {}'
            .format(factory_name, gpio_name))
        for name in self.gpio:
            if name != gpio_name and gpio_name != 'ALL':
                continue
            gpio = self.gpio[name]
            pin = gpio.pin.number
            if isinstance(gpio, DigitalOutputDevice):
                gpio.close()
                self.gpio[name] = DigitalOutputDevice(
                                      pin=pin,
                                      initial_value=None,
                                      pin_factory=pin_factory)
            else:
                pull_up = gpio.pull_up
                when_activated = gpio.when_activated
                when_deactivated = gpio.when_deactivated
                gpio.close()
                self.gpio[name] = DigitalInputDevice(pin=pin,
                                                     pull_up=pull_up,
                                                     pin_factory=pin_factory)
                self.gpio[name].when_activated = when_activated
                self.gpio[name].when_deactivated = when_deactivated
            if gpio_name != 'ALL':
                return

    def _cleanup(self, *args):
        """Resets the dongle to transparent mode and enables RS232 shutdown."""
        for arg in args:
            self._log.debug('pnpdongle cleanup called with arg = {}'.format(arg))
        if self.mode != 'transparent':
            self._log.debug('Reverting mode to transparent/RS232 auto-shutdown')
            self.mode ='transparent'

    def _rs232valid(self):
        """Detects reception of RS232 data."""
        self._log.debug('RS232 data received')

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if value not in self.MODES:
            raise ValueError('Unsupported mode: {}'.format(value))
        if not self.gpio or None in self.gpio.values():
            self._log.warning('Skipping mode set due to undefined GPIO')
            return
        self._log.debug('Setting Raspberry Pi UART as {}'.format(value))
        self._mode = value
        if value == 'master':
            self._log.debug('Energizing RL1')
            self.gpio['RL1A'].blink(n=1, background=False)
            self._log.debug('Forcing on RS232')
            self.gpio['RS232_ON'].on()
        elif value == 'transparent':
            self._log.debug('Resetting RL1')
            self.gpio['RL1B'].blink(n=1, background=False)
            self._log.debug('Resetting RL2')
            self.gpio['RL2B'].blink(n=1, background=False)
            self._log.debug('Enabling RS232 auto-shutdown')
            self.gpio['RS232_ON'].off()
        else:   #: mode == 'proxy'
            self._log.debug('Resetting RL1')
            self.gpio['RL1B'].blink(n=1, background=False)
            self._log.debug('Energizing RL2')
            self.gpio['RL2A'].blink(n=1, background=False)
            self._log.debug('Forcing on RS232')
            self.gpio['RS232_ON'].on()
        sleep(0.25)

    def _event_activated(self):
        """Queues an event triggered by modem event notification pin.
        
        gpiozero spawns a dummy thread to query which notifications asserted the
        pin and stores in self.event_queue.

        """
        if current_thread().name.startswith('Thread-'):
            current_thread().name = 'GpioThread'
        self._log.debug('Modem event notification asserted')
        notifications = run(self.modem.lowpower_notifications_check())
        for notification in notifications:
            self._process_event(notification)
    
    def _process_event(self, event_type: str):
        """Logs details of relevant event type if no callback was specified.
        
        This is a debug/test facility only. Applications should define a
        modem_event_callback.
        """
        self._log.debug('Processing {} event'.format(event_type))
        if event_type == 'message_mt_received':
            messages = self._process_message_mt_waiting()
            for message in messages:
                self._log.info('Message received: {}'.format(message))
        elif event_type == 'message_mo_complete':
            messages = self._process_message_mo_complete()
            for message in messages:
                if message['state'] > 5:
                    self._log.info('Message completed: {}'.format(message))
        elif event_type == 'event_cached':
            event_data = self._process_event_cached()
            for event in event_data:
                if (not self._event_data_last or
                    event not in self._event_data_last):
                    self._log.info('New event cached: {}'.format(event))
            self._event_data_last = event_data
        else:
            self._log.warning('No processing defined for {}'.format(
                event_type))

    def _process_message_mt_waiting(self) -> list:
        """Retrieves received Mobile-Terminated messages to be logged.
        
        This is a debug/test facility only.

        Returns:
            A list of messages in base64 format.

        """
        self._log.debug('Request to process forward message event')
        messages = None
        messages_waiting = run(self.modem.message_mt_waiting())
        if not isinstance(messages_waiting, list):
            self._log.warning('No MT messages waiting')
        else:
            messages = []
            for meta in messages_waiting:
                message = run(self.modem.message_mt_get(name=meta['name'],
                                                        data_format=FORMAT_B64,
                                                        verbose=True))
                messages.append(message)
        return messages

    def _process_message_mo_complete(self) -> list:
        """Removes a Mobile-Originated message from the transmit queue.
        
        This is a debug/test facility. Applications should be completing
        messages and confirming completion state.
        """
        self._log.debug('Request to process return message event')
        messages_queued = run(self.modem.message_mo_state())
        if not isinstance(messages_queued, list):
            self._log.warning('No MO messages queued or completed')
        return messages_queued

    def _process_event_cached(self, class_subclass: tuple = None) -> list:
        """Processes a cached Trace event for logging if no callback defined.
        
        This is a debug/test facility only. Applications should process
        relevant trace events.
        """
        self._log.debug('Request to process cached modem event')
        event_data = None
        if class_subclass is not None:
            event_data = [run(self.modem.event_get(class_subclass))]
        else:
            event_data = []
            events_available = run(self.modem.event_monitor_get())
            for event in events_available:
                if event.endswith('*'):
                    c, s = event.replace('*', '').split('.')
                    tup = (int(c), int(s))
                    if tup == (3, 1):
                        status = run(self.modem.satellite_status())
                        status['state'] = CONTROL_STATES[status['state']]
                        status['beamsearch'] = (BEAMSEARCH_STATES[
                            status['beamsearch']])
                        event_data.append(status)
                    else:
                        event_data.append(run(self.modem.event_get(event=tup)))
        return event_data

    def modem_reset(self):
        """Resets the IDP modem."""
        self._log.warning('Resetting IDP modem')
        self.gpio['MODEM_RESET'].blink(n=1, background=False)
    
    def pps_enable(self, enable=True):
        """Enables 1 pulse-per-second GNSS time output from the IDP modem.
        
        Sets the GNSS refresh rate to once per second, and enables pulse output.

        Args:
            enable: enables (or disables) pulse-per-second

        """
        self._log.info('{} pulse per second IDP modem output'.format(
            'Enabling' if enable else 'Disabling'))
        response = run(self.modem.command('AT%TRK={}'.format(
            1 if enable else 0)))
        if response[0] == 'OK':
            return True
        self._log.error('Failed to {} 1s GNSS update'.format(
            'enable' if enable else 'disable'))
        return False
