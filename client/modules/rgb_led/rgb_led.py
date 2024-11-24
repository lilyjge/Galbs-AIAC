"""
Module for interfacing with RGB LEDs.
"""

import time

import gpiozero

from . import color


PWM_REDUCTION = 255
DEFAULT_RGB_COLOR = (0, 0, 0)
FADE_STEPS = 64


class RgbLed:
    """
    RBG LED class.
    """

    def __init__(self, red: int, green: int, blue: int, common_cathode: bool) -> None:
        """
        Initializes the RGB LED with the specified configuration.

        red: Red GPIO pin number.
        green: Green GPIO pin number.
        blue: Blue GPIO pin number.
        common_cathode: RGB LED is common common cathode.
        """
        try:
            self.__rgb_led = gpiozero.RGBLED(
                red=red, green=green, blue=blue, active_high=common_cathode
            )
            result, rgb_color = color.Color.create(*DEFAULT_RGB_COLOR)
            if not result:
                raise ValueError("ERROR: Failed to initialize color")
            self.__rgb_color = rgb_color
            self.set_color(self.__rgb_color)

        # Catching all exceptions for library call
        # pylint: disable-next=broad-exception-caught
        except Exception as exception:
            print(f"ERROR: Failed to initialize RGB LED, exception: {exception}")

    @staticmethod
    def get_pwm_values(rgb_color: color.Color) -> "tuple[bool, tuple[float, float, float] | None]":
        """
        Calculates RGB values to PWM-compatible values (0.0 to 1.0).

        rgb_color: RGB values.

        Returns: Success, PWM values for red, green and blue.
        """
        red_rgb, green_rgb, blue_rgb = rgb_color.rgb_values

        red_pwm = red_rgb / PWM_REDUCTION
        green_pwm = green_rgb / PWM_REDUCTION
        blue_pwm = blue_rgb / PWM_REDUCTION

        return (True, (red_pwm, green_pwm, blue_pwm))

    def set_color(self, rgb_color: color.Color) -> bool:
        """
        Sets LED color.

        rgb_color: RGB values.

        Returns: Success.
        """
        result, (red_pwm, green_pwm, blue_pwm) = self.get_pwm_values(rgb_color)
        if not result:
            print(f"ERROR: Failed to get pwm values for color: {rgb_color.rgb_values}")
            return False

        self.__rgb_led.red = red_pwm
        self.__rgb_led.green = green_pwm
        self.__rgb_led.blue = blue_pwm

        return True

    def fade_color(self, rgb_color: color.Color, duration: float) -> bool:
        """
        Fades LED to specified color.

        rgb_color: Target RGB color.
        duration: Duration of fade animation (ms).

        Returns: Success.
        """
        result, (target_red_pwm, target_green_pwm, target_blue_pwm) = self.get_pwm_values(rgb_color)
        if not result:
            print(f"ERROR: Failed to get pwm values for color: {rgb_color.rgb_values}")
            return False

        current_red_pwm = self.__rgb_led.red
        current_green_pwm = self.__rgb_led.green
        current_blue_pwm = self.__rgb_led.blue

        step_duration = duration / FADE_STEPS

        red_step = (target_red_pwm - current_red_pwm) / FADE_STEPS
        green_step = (target_green_pwm - current_green_pwm) / FADE_STEPS
        blue_step = (target_blue_pwm - current_blue_pwm) / FADE_STEPS

        for i in range(FADE_STEPS):
            self.__rgb_led.red = current_red_pwm + red_step * i
            self.__rgb_led.green = current_green_pwm + green_step * i
            self.__rgb_led.blue = current_blue_pwm + blue_step * i
            time.sleep(step_duration / 1000)

        self.__rgb_led.red = target_red_pwm
        self.__rgb_led.green = target_green_pwm
        self.__rgb_led.blue = target_blue_pwm

        return True

    def turn_off(self) -> None:
        """
        Turns the LED off (i.e., sets the color to 0, 0, 0).
        """
        self.__rgb_led.off()
