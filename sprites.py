import arcade

FIRST_COL_WIDTH = 100

def load_textures_by_state(sprite_sheet_path, sprite_width, sprite_height, columns, rows, states):

    # Iterate through rows and columns
    # Iterate through rows and columns
    textures_by_state = {state: [] for state in states}

    # Validate that the number of states matches the number of rows
    if len(states) != rows:
        raise ValueError("The number of states must match the number of rows in the sprite sheet.")

    # Iterate through rows and columns, assign textures to states
    for row in range(rows):
        state = states[row]  # Each row corresponds to a state
        for col in range(1, columns):  # Start from column 1 to skip the first column
            x = FIRST_COL_WIDTH + (col - 1) * sprite_width  # Account for wider first column
            y = row * sprite_height
            texture = arcade.load_texture(sprite_sheet_path, x, y, sprite_width, sprite_height)
            textures_by_state[state].append(texture)

    return textures_by_state