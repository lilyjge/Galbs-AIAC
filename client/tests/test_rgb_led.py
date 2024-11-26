"""
Testing script for all GPIO components.
"""

import time

from modules.rgb_led import rgb_led
from modules.rgb_led import color


def main() -> int:
    """
    Main, will switch to pytest soon.
    """
    # The old LED is common anode
    led1 = rgb_led.RgbLed(17, 27, 22, False)
    # The new LED is common cathode
    led2 = rgb_led.RgbLed(5, 6, 13, True)

    led1.set_color(color.Color.create(255, 0, 0)[1])
    led2.set_color(color.Color.create(255, 0, 0)[1])

    time.sleep(1)

    led1.fade_color(color.Color.create(0, 255, 0)[1], 300)
    led2.fade_color(color.Color.create(0, 255, 0)[1], 300)

    time.sleep(100)

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main != 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
