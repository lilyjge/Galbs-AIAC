"""
Simultanous stepper motor control.
"""

from . import stepper_motor
import time


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



def set_position(
        angle: int, stepper_motor_left: stepper_motor.StepperMotor, stepper_motor_right: stepper_motor.StepperMotor, rotations_per_minute: int = DEFAULT_ROTATIONS_PER_MINUTE
    ) -> bool:
        """
        Moves the motor to a specified angle at a given speed.

        angle: Desired angle to rotate motor to.
        rotations_per_minute: Speed at which to rotate motor.

        Returns: Success.
        """
        if stepper_motor_left.current_angle != stepper_motor_right.current_angle:
            print(f"ERROR: Motors not in sync")
            return False

        result = stepper_motor_left.set_step_delay(rotations_per_minute)
        if not result:
            print(f"ERROR: Failed to set rotations per minute: {rotations_per_minute}")
            return False
        result = stepper_motor_right.set_step_delay(rotations_per_minute)
        if not result:
            print(f"ERROR: Failed to set rotations per minute: {rotations_per_minute}")
            return False

        if angle < stepper_motor_left.angle_limits[0] or angle > stepper_motor_left.angle_limits[1]:
            print(f"ERROR: Angle not in valid range: {angle}")
            return False
        if angle < stepper_motor_right.angle_limits[0] or angle > stepper_motor_right.angle_limits[1]:
            print(f"ERROR: Angle not in valid range: {angle}")
            return False

        angle_differerence = angle - stepper_motor_left.current_angle
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

        #result = self.__move_steps(steps_to_move, direction)

        left_step_number = 0
        right_step_number = 0
        try:
            for _ in range(steps_to_move):
                left_step_number = stepper_motor_left.move_step(left_step_number, direction)
                right_step_number = stepper_motor_right.move_step(right_step_number, direction)
                time.sleep(stepper_motor_left.step_delay)

        # Catching all exceptions for library call
        # pylint: disable-next=broad-exception-caught
        except Exception as exception:
            print(f"ERROR: Failed to move steps: {steps_to_move}, exception: {exception}")
            return False

        if not result:
            print(f"ERROR: Failed to perform steps {steps_to_move}")
            return False

        stepper_motor_left.set_current_angle(angle)
        stepper_motor_right.set_current_angle(angle)

        return True