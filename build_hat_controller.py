from buildhat import Motor

steering_motor = None
last_position = None  # Changed to None to detect first run
MIN_CHANGE_THRESHOLD = 15
initial_position = None  # Store the very first position
last_significant_position = None  # Track the last position that caused movement
last_check_time = None
ROTATION_TIMEOUT = 0.1  # 100ms timeout for rotation

def setup():
    global steering_motor, last_position, initial_position, last_significant_position
    if steering_motor is None:
        steering_motor = Motor('A')
        # Initialize positions only if they haven't been set
        if last_position is None:
            initial_position = steering_motor.get_position()
            last_position = initial_position
            last_significant_position = initial_position

def lego_build_hat_input():
    import time
    setup()
    global last_position, initial_position, last_significant_position, last_check_time
    
    current_time = time.time()
    # Get the current rotation of the steering wheel
    current_position = steering_motor.get_position()
    
    # Calculate if there's active rotation
    position_change = abs(current_position - last_position)
    is_rotating = position_change >= MIN_CHANGE_THRESHOLD
    
    # Update last_position always to track continuous small changes
    last_position = current_position
    
    # Update last check time if rotating
    if is_rotating:
        last_check_time = current_time
    
    # Calculate position relative to initial position
    relative_position = current_position - initial_position
    
    # Normalize the rotation to a value between -1 and 1
    # Assuming max rotation is 100 degrees in each direction
    normalized_steering = max(min(relative_position / 100.0, 1.0), -1.0)
    
    # Add a small deadzone around zero to prevent unwanted movement
    if abs(normalized_steering) < 0.1:
        normalized_steering = 0.0
    
    # Only return movement if actively rotating
    if not is_rotating:
        normalized_steering = 0.0
    
    return {
        "steering": normalized_steering,
        "left": normalized_steering < -0.1,
        "right": normalized_steering > 0.1
    }