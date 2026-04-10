# task2.py

# ---------------- RGB PATTERNS ----------------
patterns = {
    "1": [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0)],  #RED, GREEN, BLUE
    "2": [(255, 255, 0), (255, 0, 0), (0, 90, 255), (0, 0, 0)], #YELLOW, RED, PEACOCK BLUE
    "3": [(0, 63, 52), (255, 255, 0),(255, 255, 255), (0, 0, 0)] #LIGHT BLUE, BRIGHT YELLOW, WHITE
}

# ---------------- INPUT PATTERNS ----------------
input_patterns = {
    "1": ["PRESS", "PRESS", "HOLD"],
    "2": ["HOLD", "PRESS", "HOLD"],
    "3": ["HOLD", "HOLD", "HOLD"],
}

# ---------------- STATE ----------------
current_profile = None
pattern_expected = []
input_buffer = []
game_active = False
after_id = None
root_ref = None
ser_ref = None

# ---------------- DELAYS ----------------
color_delay = 500   # 500ms between each color
cycle_pause = 500   # extra pause between cycles

# ---------------- SEND COLOR ----------------
def send_color(ser, r, g, b):
    if ser:
        ser.write(f"{r},{g},{b}\n".encode())

# ---------------- START GAME ----------------
def start_rgb_game(root, ser, profile):
    """
    Starts the RGB loop for the selected profile.
    Each color has a 500ms delay, with a small pause between cycles.
    """
    global current_profile, pattern_expected, input_buffer
    global game_active, after_id, root_ref, ser_ref

    if profile not in patterns:
        profile = "1"

    current_profile = profile
    pattern_expected = input_patterns[profile]
    input_buffer = []
    game_active = True
    root_ref = root
    ser_ref = ser

    pattern = patterns[profile]
    pattern_len = len(pattern)

    def loop(index=0):
        global game_active, after_id

        if not game_active:
            send_color(ser_ref, 0, 0, 0)
            return

        # send current color
        color = pattern[index % pattern_len]
        send_color(ser_ref, *color)

        # schedule next step
        next_index = index + 1
        delay = color_delay

        # if finished a full cycle, add extra pause
        if next_index % pattern_len == 0:
            delay += cycle_pause

        after_id = root_ref.after(delay, loop, next_index)

    loop()

# ---------------- HANDLE INPUT ----------------
def handle_input_rgb(event):
    """
    event: "PRESS" or "HOLD"
    returns:
        1 = correct sequence
        0 = wrong sequence
        None = still in progress
    """
    global input_buffer, pattern_expected, game_active

    if not game_active or event not in ["PRESS", "HOLD"]:
        return None

    input_buffer.append(event)

    # keep buffer size within expected pattern
    if len(input_buffer) > len(pattern_expected):
        input_buffer.pop(0)

    #Correct
    if input_buffer == pattern_expected:
        stop_game()
        return 1

    #Wrong (early mismatch)
    if input_buffer != pattern_expected[:len(input_buffer)]:
        input_buffer.clear()
        stop_game()
        return 0

    # still waiting for more input
    return None

# ---------------- STOP GAME ----------------
def stop_game():
    global game_active, after_id, root_ref, ser_ref
    game_active = False

    if after_id and root_ref:
        try:
            root_ref.after_cancel(after_id)
        except:
            pass
        after_id = None

    # turn off LEDs
    send_color(ser_ref, 0, 0, 0)