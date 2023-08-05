"""GPIOInputButton to receive signals."""
from ..helper.gpio import setup_input, read_input, edge_detect
import subprocess
from functools import partial
from typing import Callable, Any
from datetime import datetime
import logging
import asyncio
from ..const import (
    CONFIG_PIN,
    GPIO,
    SINGLE,
    DOUBLE,
    LONG,
    ClickTypes,
    DEBOUNCE_DURATION,
    LONG_PRESS_DURATION,
    DELAY_DURATION,
    SECOND_DELAY_DURATION,
)

_LOGGER = logging.getLogger(__name__)


def configure_pin(pin: str) -> None:
    pin = f"{pin[0:3]}0{pin[3]}" if len(pin) == 4 else pin
    _LOGGER.debug(f"Configuring pin for GPIO {pin}")
    subprocess.run(
        [CONFIG_PIN, pin, GPIO],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )


class GpioInputButton:
    """Represent Gpio input switch."""

    def __init__(
        self, pin: str, press_callback: Callable[[ClickTypes, str], None], rest_pin: Any
    ) -> None:
        """Setup GPIO Input Button"""
        self._pin = pin
        configure_pin(pin)
        self._loop = asyncio.get_running_loop()
        self._press_callback = press_callback
        setup_input(self._pin)
        edge_detect(self._pin, callback=self._handle_press, bounce=25)
        self._first_press_timestamp = None
        self._is_long_press = False
        self._second_press_timestamp = None
        self._second_check = False
        _LOGGER.debug("Configured listening for input pin %s", self._pin)

    def _handle_press(self, pin) -> None:
        """Handle the button press callback"""
        # Ignore if we are in a long press
        if self._is_long_press:
            return
        now = datetime.now()

        # Debounce button
        if (
            self._first_press_timestamp is not None
            and now - self._first_press_timestamp < DEBOUNCE_DURATION
        ):
            return

        # Second click debounce. Just in case.
        if (
            self._second_press_timestamp is not None
            and now - self._second_press_timestamp < DEBOUNCE_DURATION
        ):
            return

        if not self._first_press_timestamp:
            self._first_press_timestamp = now
        elif not self._second_press_timestamp:
            self._second_press_timestamp = now

        self._loop.call_soon_threadsafe(
            self._loop.call_later,
            DELAY_DURATION,
            self.check_press_length,
        )

    @property
    def is_pressed(self):
        """Is button pressed."""
        return read_input(self._pin)

    def check_press_length(self) -> None:
        """Check if it's a single, double or long press"""
        # Check if button is still pressed
        if self.is_pressed:
            # Schedule a new check
            self._loop.call_soon_threadsafe(
                self._loop.call_later,
                DELAY_DURATION,
                self.check_press_length,
            )

            # Handle edge case due to multiple clicks
            if self._first_press_timestamp is None:
                return

            # Check if we reached a long press
            diff = datetime.now() - self._first_press_timestamp
            if not self._is_long_press and diff > LONG_PRESS_DURATION:
                self._is_long_press = True
                _LOGGER.debug("Long button press, call callback")
                self._loop.call_soon_threadsafe(
                    partial(self._press_callback, LONG, self._pin)
                )
            return

        # Handle short press
        if not self._is_long_press:
            if not self._second_press_timestamp and not self._second_check:
                # let's try to check if second click will atempt
                self._second_check = True
                self._loop.call_soon_threadsafe(
                    self._loop.call_later,
                    SECOND_DELAY_DURATION,
                    self.check_press_length,
                )
                return
            if self._second_check:
                if self._second_press_timestamp:
                    _LOGGER.debug(
                        "Double click event, roznica %s",
                        self._second_press_timestamp - self._first_press_timestamp,
                    )
                    self._loop.call_soon_threadsafe(
                        partial(self._press_callback, DOUBLE, self._pin)
                    )

                elif self._first_press_timestamp:
                    _LOGGER.debug("One click event, call callback")
                    self._loop.call_soon_threadsafe(
                        partial(self._press_callback, SINGLE, self._pin)
                    )

        # Clean state on button released
        self._first_press_timestamp = None
        self._second_press_timestamp = None
        self._second_check = False
        self._is_long_press = False
