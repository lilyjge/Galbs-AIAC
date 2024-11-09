"""
Module for interfacing with stepper motors.
"""

import time

import gpiozero


CW = 1
CCW = -1

STEP_SEQUENCE_LEFT = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
STEP_SEQUENCE_RIGHT = [[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]

DEFAULT_ROTATIONS_PER_MINUTE = 620
MIN_ROTATIONS_PER_MINUTE = 240
MAX_ROTATIONS_PER_MINUTE = 620

DEFAULT_MIN_ANGLE = 0
DEFAULT_MAX_ANGLE = 130  # Change this when the actual robot is built.

ROTOR_STEPS_PER_REVOLUTION = 32
REDUCTION_RATIO = 64


class StepperMotor:
    """
    Stepper motor class.
    """

    def __init__(
        self,
        motor_pins: "tuple[int, int, int, int]",
        left: bool,
        min_angle: int = DEFAULT_MIN_ANGLE,
        max_angle: int = DEFAULT_MAX_ANGLE,
    ) -> None:
        """
        Initializes the stepper motor with the specified configuration.

        motor_pins: GPIO pin numbers for stepper motor.
        left: Stepper motor is on left side of robot.
        min_angle: The lower limit for the range of motion.
        max_angle: The upper limit for the range of motion.
        """
        self.__motor_pins = [gpiozero.OutputDevice(pin) for pin in motor_pins]

        self.__step_sequence = STEP_SEQUENCE_LEFT if left else STEP_SEQUENCE_RIGHT
        self.__step_delay = 60 / ROTOR_STEPS_PER_REVOLUTION / DEFAULT_ROTATIONS_PER_MINUTE

        self.__min_angle = min_angle
        self.__max_angle = max_angle
        self.__current_angle = 110

    def __set_step_delay(self, rotations_per_minute: int) -> bool:
        """
        Sets the delay between steps.

        rotations_per_minute: Desired speed in rotations per minute.

        Returns: Success.
        """
        if (
            rotations_per_minute < MIN_ROTATIONS_PER_MINUTE
            or rotations_per_minute > MAX_ROTATIONS_PER_MINUTE
        ):
            print(f"ERROR: Rotations per minute out of bounds: {rotations_per_minute}")
            return False

        try:
            self.__step_delay = 60 / ROTOR_STEPS_PER_REVOLUTION / rotations_per_minute

        # Catching all exceptions for library call
        # pylint: disable-next=broad-exception-caught
        except Exception as exception:
            print(
                f"ERROR: Failed to calculate step delay for speed: {rotations_per_minute}, exception: {exception}"
            )
            return False

        return True

    def __move_steps(self, number_of_steps: int, direction: int) -> bool:
        """
        Moves the motor a specified number of steps in a given direction.

        number_of_steps: Number of steps to move.
        direction: Direction of movement (CW or CCW).

        Returns: Success.
        """
        if number_of_steps <= 0:
            print(f"ERROR: Invalid number of steps: {number_of_steps}")
            return False

        if direction not in [-1, 1]:
            print(f"ERROR: Invalid direction: {direction}")
            return False

        step_number = 0
        try:
            for _ in range(number_of_steps):
                step_number = (step_number + direction) % ROTOR_STEPS_PER_REVOLUTION
                sequence = self.__step_sequence[step_number % len(self.__step_sequence)]
                for pin, state in zip(self.__motor_pins, sequence):
                    if state:
                        pin.on()
                    else:
                        pin.off()
                time.sleep(self.__step_delay)

        # Catching all exceptions for library call
        # pylint: disable-next=broad-exception-caught
        except Exception as exception:
            print(f"ERROR: Failed to move steps: {number_of_steps}, exception: {exception}")
            return False

        return True

    def set_position(
        self, angle: int, rotations_per_minute: int = DEFAULT_ROTATIONS_PER_MINUTE
    ) -> bool:
        """
        Moves the motor to a specified angle at a given speed.

        angle: Desired angle to rotate motor to.
        rotations_per_minute: Speed at which to rotate motor.

        Returns: Success.
        """
        result = self.__set_step_delay(rotations_per_minute)
        if not result:
            print(f"ERROR: Failed to set rotations per minute: {rotations_per_minute}")
            return False

        if angle < self.__min_angle or angle > self.__max_angle:
            print(f"ERROR: Angle not in valid range: {angle}")
            return False

        angle_differerence = angle - self.__current_angle
        if angle_differerence == 0:
            return True

        direction = CW if angle_differerence > 0 else CCW

        try:
            steps_to_move = abs(
                int((angle_differerence * ROTOR_STEPS_PER_REVOLUTION * REDUCTION_RATIO) / 360)
            )
        # Catching all exceptions for library call
        # pylint: disable-next=broad-exception-caught
        except Exception as exception:
            print(
                f"ERROR: Failed to calculate number of steps to rotate to angle {angle}, exception: {exception}"
            )
            return False

        result = self.__move_steps(steps_to_move, direction)
        if not result:
            print(f"ERROR: Failed to perform steps {steps_to_move}")
            return False

        self.__current_angle = angle

        return True