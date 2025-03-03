from datetime import datetime
from time import sleep
from typing import Callable, List, Union

import board
from digitalio import DigitalInOut
import adafruit_character_lcd.character_lcd as characterlcd
import adafruit_ahtx0
from gpiozero import Button, LED


class ManageDisplay:
    """Class to manage the character LCD display."""
    MessageType = Union[str, tuple[str, str],
                        Callable[[], Union[str, tuple[str, str]]]]

    def __init__(self):
        """Initialize the LCD with the correct GPIO pins."""
        self.lcd_rs = DigitalInOut(board.D17)
        self.lcd_e = DigitalInOut(board.D27)
        self.lcd_d4 = DigitalInOut(board.D5)
        self.lcd_d5 = DigitalInOut(board.D6)
        self.lcd_d6 = DigitalInOut(board.D13)
        self.lcd_d7 = DigitalInOut(board.D26)

        self.lcd = characterlcd.Character_LCD_Mono(
            self.lcd_rs, self.lcd_e,
            self.lcd_d4, self.lcd_d5,
            self.lcd_d6, self.lcd_d7,
            columns=16, lines=2
        )

    def wait(self, paused, seconds=5) -> bool:
        """Wait for a specified duration, breaking early if paused."""
        if paused:
            sleep(seconds)
        for _ in range(seconds * 10):
            if paused:
                break
            sleep(0.1)
        if paused:
            return True
        return False

    def cleanup(self):
        """Clear the display and release GPIO resources."""
        self.lcd.clear()
        for pin in [self.lcd_rs, self.lcd_e, self.lcd_d4,
                    self.lcd_d5, self.lcd_d6, self.lcd_d7]:
            pin.deinit()

    def display_message(self, message: MessageType):
        """Display the message on the LCD."""
        self.lcd.clear()
        msg: Union[str, tuple[str, str]]

        if callable(message):
            msg = message()
        else:
            msg = message

        if isinstance(msg, tuple) and len(msg) == 2:
            self.lcd.message = f"{msg[0]}\n{msg[1]}"
        else:
            self.lcd.message = msg


class ManageLED:
    """Class to control LED states."""

    def __init__(self):
        """Initialize LEDs with their respective GPIO pins."""
        self.red = LED(18)
        self.green = LED(16)
        self.blue = LED(23)

    def __action__(self, action, *args):
        """Perform the specified action on the requested LEDs."""
        redAction = getattr(
            self.red, action,
            lambda: ValueError(f"{action} action not found for Red LED"))
        greenAction = getattr(
            self.green, action,
            lambda: ValueError(f"{action} action not found for Green LED"))
        blueAction = getattr(
            self.blue, action,
            lambda: ValueError(f"{action} action not found for Blue LED"))
        if len(args) == 0:
            redAction()
            greenAction()
            blueAction()
            return
        for color in args:
            match color:
                case 'red':
                    redAction()
                    continue
                case 'green':
                    greenAction()
                    continue
                case 'blue':
                    blueAction()
                    continue

    def on(self, *args):
        """Turn on the specified LEDs."""
        self.__action__('on', *args)

    def off(self, *args):
        """Turn off the specified LEDs."""
        self.__action__('off', *args)


class ManageButton:
    """Class to manage button interactions."""

    def __init__(self):
        """Initialize buttons with their respective GPIO pins."""
        self.red = Button(25)
        self.green = Button(24)
        self.blue = Button(12)


def manageTemp(thSensor, led):
    """Manage LED color based on temperature and return formatted temperature data."""
    c = thSensor.temperature
    f = thSensor.temperature * 9 / 5 + 32

    if c <= 0:
        led.off('red', 'green')
        led.on('blue')
    elif c <= 35:
        led.off('red', 'blue')
        led.on('green')
    elif c > 35:
        led.off('blue', 'green')
        led.on('red')

    return (
        "Temperature:",
        f"{c:0.1f}C / {f:0.1f}F"
    )


if __name__ == "__main__":
    i2c = board.I2C()
    thSensor = adafruit_ahtx0.AHTx0(i2c)

    display = ManageDisplay()

    led = ManageLED()
    manageTemp(thSensor, led)

    button = ManageButton()

    MESSAGES: List[ManageDisplay.MessageType] = [
        lambda: ("Happy", f"{datetime.now().strftime('%A')}!"),
        lambda: ("Current Time:", datetime.now().strftime('%I:%M:%S %p')),
        lambda: manageTemp(thSensor, led),
        lambda: ("Humidity:", f"{thSensor.relative_humidity:0.1f}%")
    ]

    current_message_index = 0
    paused = False

    def show_message():
        """Display the current message."""
        display.display_message(MESSAGES[current_message_index])

    def next_message():
        """Cycle to the next message."""
        global current_message_index
        current_message_index = (current_message_index + 1) % len(MESSAGES)
        show_message()

    def prev_message():
        """Cycle to the previous message."""
        global current_message_index
        current_message_index = (current_message_index - 1) % len(MESSAGES)
        show_message()

    def toggle_pause():
        """Toggle pause state for the message cycle."""
        global paused
        paused = not paused

    button.red.when_pressed = next_message
    button.green.when_pressed = toggle_pause
    button.blue.when_pressed = prev_message

    try:
        while True:
            show_message()
            if not display.wait(paused, 5):
                current_message_index = (
                    current_message_index + 1) % len(MESSAGES)

    except KeyboardInterrupt:
        pass
    finally:
        display.cleanup()
        led.off()
