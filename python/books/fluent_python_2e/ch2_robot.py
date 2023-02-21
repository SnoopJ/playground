"""
This code sample is adapted from an example in the book "Fluent Python" (2nd edition)

https://github.com/fluentpython/example-code-2e/blob/28d6d033156831a77b700064997c05a40a83805f/02-array-seq/array-seq.ipynb?short_path=afdbf6b#L993-L1020

This defines the no-longer-imaginary Robot class to show off how the pattern
matching functions
"""


class InvalidCommand(Exception):
    pass


class LED:
    def set_brightness(self, ident, intensity):
        print(f"[LED {ident!r}]: Set intensity to {intensity}")

    def set_color(self, ident, red, green, blue):
        print(f"[LED {ident!r}]: Set color to ({red}, {green}, {blue})")


class Robot:
    def __init__(self, leds):
        self.leds = leds

    def beep(self, times, frequency):
        print(f"Beeping {times=} times at {frequency=}")
        for _ in range(int(times)):
            print("Beep!")

    def rotate_neck(self, angle):
        print(f"Rotate neck by {angle=}")

    def handle_command(self, message):
        match str(message).split():
            case ['BEEPER', frequency, times]:
                self.beep(times, frequency)
            case ['NECK', angle]:
                self.rotate_neck(angle)
            case ['LED', ident, intensity]:
                self.leds[ident].set_brightness(ident, intensity)
            case ['LED', ident, red, green, blue]:
                self.leds[ident].set_color(ident, red, green, blue)
            case _:
                raise InvalidCommand(message)


if __name__ == "__main__":
    rob = Robot(leds={
        '0': LED(),
        '1': LED(),
        '2': LED(),
        '3': LED(),
    })

    rob.handle_command("BEEPER 42 10")
    rob.handle_command("NECK 42")
    rob.handle_command("LED 0 0")
    rob.handle_command("LED 0 100")
    rob.handle_command("LED 0 0 0 0")
    rob.handle_command("LED 1 255 255 0")

    rob.handle_command("FAKECOMMAND THIS WILL FAIL")
