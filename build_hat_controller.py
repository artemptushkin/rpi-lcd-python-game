from buildhat import Motor

steering_motor = None
last_position = 0

def setup():
    global steering_motor
    global last_position
    if steering_motor is None:
        steering_motor = Motor('A')
        last_position = 0


def lego_build_hat_input():
    setup()
    # Get the current rotation of the steering wheel
    rotation = steering_motor.get_position()

    # If the rotation is negative, the wheel was turned left, otherwise right
    if rotation < -10:  # Adjust threshold for "left turn"
        return {
            "left": True,
            "right": False
        }
    elif rotation > 10:  # Adjust threshold for "right turn"
        return {
            "left": False,
            "right": True
        }
    else:
        return {
            "left": False,
            "right": False
        }