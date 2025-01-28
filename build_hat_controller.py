from buildhat import Motor

steering_motor = None
last_position = None  # Changed to None to detect first run
MIN_CHANGE_THRESHOLD = 5  # Reduced threshold for more responsive control
initial_position = None  # Store the very first position
last_steering_value = 0  # Track the last steering value

def setup():
    global steering_motor
    global last_position
    global initial_position
    if steering_motor is None:
        steering_motor = Motor('A')
        # Initialize positions only if they haven't been set
        if last_position is None:
            initial_position = steering_motor.get_position()
            last_position = initial_position

def lego_build_hat_input():
    setup()
    global last_position, initial_position, last_steering_value
    
    # Get the current rotation of the steering wheel
    current_position = steering_motor.get_position()
    
    # Calculate position relative to initial position
    relative_position = current_position - initial_position
    
    # Only update if change is significant enough
    if abs(current_position - last_position) >= MIN_CHANGE_THRESHOLD:
        last_position = current_position
        rotation = relative_position
        has_new_input = True
    else:
        rotation = last_position - initial_position  # Use the last significant position relative to initial
        has_new_input = False

    # Normalize the rotation to a value between -1 and 1
    # Assuming max rotation is 100 degrees in each direction
    normalized_steering = max(min(rotation / 100.0, 1.0), -1.0)
    
    # Add a small deadzone around zero to prevent unwanted movement
    if abs(normalized_steering) < 0.1:
        normalized_steering = 0.0
        has_new_input = True  # Allow movement to stop when returning to center
    
    # Only consider it a new direction if the steering value changed significantly
    has_new_direction = abs(normalized_steering - last_steering_value) >= 0.05  # Reduced threshold
    last_steering_value = normalized_steering
    
    # Make sure left/right matches the steering direction
    is_left = normalized_steering < -0.1
    is_right = normalized_steering > 0.1
    
    return {
        "steering": normalized_steering,
        "has_new_input": has_new_input or has_new_direction,  # Allow movement on either condition
        "left": is_left,
        "right": is_right,
        "direction": "left" if is_left else "right" if is_right else None
    }