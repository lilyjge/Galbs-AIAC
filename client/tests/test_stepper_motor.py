"""
Testing script for stepper motors.
"""

from modules.stepper_motor import stepper_motor


def main() -> int:
    """
    Main, will switch to pytest soon.
    """
    angle = 130

    stepper_motor1 = stepper_motor.StepperMotor((18, 23, 24, 25), True)
    stepper_motor2 = stepper_motor.StepperMotor((12, 16, 20, 21), False)

    stepper_motor1.set_position(angle, 620)
    stepper_motor2.set_position(angle, 620)

    stepper_motor1.set_position(0, 310)
    stepper_motor2.set_position(0, 310)

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main != 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
