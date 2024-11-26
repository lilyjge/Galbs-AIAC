"""
Testing script for stepper motors.
"""

from modules.stepper_motor import stepper_motor
from modules.stepper_motor import simultaneous


def main() -> int:
    """
    Main, will switch to pytest soon.
    """
    angle = 0

    stepper_motor_left = stepper_motor.StepperMotor((18, 23, 24, 25), True)
    stepper_motor_right = stepper_motor.StepperMotor((12, 16, 20, 21), False)

    simultaneous.set_position(angle, stepper_motor_left, stepper_motor_right)
    
    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main != 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
