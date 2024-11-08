"""
Color object module.
"""

RGB_MIN = 0
RGB_MAX = 255


class Color:
    """
    RGB color object.
    """

    __create_key = object()

    @classmethod
    def create(cls, red: int, green: int, blue: int) -> "tuple[bool, Color | None]":
        """
        Public factory method for Color objects.

        red: Red RGB value.
        green: Green RGB value.
        blue: Blue RGB value.

        Returns: Success, color object.
        """
        if not cls._is_valid_rgb_value(red):
            print("Error: Invalid red value, must be between 0 and 255.")
            return False, None

        if not cls._is_valid_rgb_value(green):
            print("Error: Invalid green value, must be between 0 and 255.")
            return False, None

        if not cls._is_valid_rgb_value(blue):
            print("Error: Invalid blue value, must be between 0 and 255.")
            return False, None

        return True, Color(cls.__create_key, red, green, blue)

    @staticmethod
    def _is_valid_rgb_value(value: int) -> bool:
        """
        Checks if a given color component is within the RGB range.

        value: RGB value.

        Returns: Validity.
        """
        return RGB_MIN <= value <= RGB_MAX

    def __init__(self, class_private_create_key: object, red: int, green: int, blue: int) -> None:
        """
        Private constructor, use create() method.
        """
        assert class_private_create_key is Color.__create_key, "Use create() method"

        self.__red = red
        self.__green = green
        self.__blue = blue

    @property
    def rgb_values(self) -> "tuple[int, int, int]":
        """
        Gets the RGB values of the color as a tuple.

        Returns: red RGB value, green RGB value, blue RGB value.
        """
        return self.__red, self.__green, self.__blue
