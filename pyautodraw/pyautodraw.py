import math
import pyautogui
import random
import sys

# Globals

# List of positions of different colours
_colour_positions = []


# Tuple for canvas size
_canvas_size = pyautogui.size()
_canvas_size = (_canvas_size[0] - 15, _canvas_size[1] - 218)


# Starting position of the canvas on the screen
_canvas_pos = (5, 144)


def init(clear=True, resize=True, pause=0.05):
    pyautogui.PAUSE = pause

    _get_colour_positions()
    focus_paint_window()

    if resize:
        resize_canvas(_canvas_size)

    if clear:
        clear_canvas()

    select_brush()
    move_to_canvas()


def _get_colour_positions():
    inc = 20
    init_x = 754
    x, y = init_x, 52

    for i in range(30):
        _colour_positions.append((x, y))

        # Check if next row
        if (i + 1) % 10 == 0:
            y += inc
            x = 754

        x += inc


# ----=== Brush Functions ===---- #


# Changes the currently selected colour.
# Leave parameter empty for random colour.
def change_colour(new_colour=None):
    curr_mouse = pyautogui.position()  # save spot in drawing

    if new_colour not in _colour_positions and new_colour is not None:
        print("Don't know the position of {}".format(new_colour))
    else:
        if new_colour is None:
            new_colour = random.choice(_colour_positions)

        pyautogui.moveTo(new_colour)
        pyautogui.click()
        pyautogui.moveTo(curr_mouse)


def select_brush():
    pyautogui.click((335, 70))


# ----=== Canvas Functions ===---- #


def clear_canvas():
    pyautogui.hotkey("ctrl", "a")
    pyautogui.keyDown("delete")


def get_canvas_size():
    return _canvas_size


def is_on_canvas(position):
    actual_position = get_actual_draw_position(position)

    if actual_position[0] < _canvas_pos[0]:
        return False
    if actual_position[1] < _canvas_pos[1]:
        return False
    if position[0] > _canvas_size[0]:
        return False
    if position[1] > _canvas_size[1]:
        return False


def move_to_canvas():
    pyautogui.moveTo(_canvas_pos)


def resize_canvas(new_size):
    pyautogui.hotkey("ctrl", "w")  # Resize menu
    pyautogui.press("right")  # Select pixels

    # Remove aspect ratio
    for _ in range(3):
        pyautogui.press("tab")

    pyautogui.press("space")

    # Enter new size
    pyautogui.hotkey("shift", "tab")
    pyautogui.typewrite(str(new_size[1]))
    pyautogui.hotkey("shift", "tab")
    pyautogui.typewrite(str(new_size[0]))

    pyautogui.press("enter")  # Confirm changes


# ----=== Drawing Functions ===---- #

# Draws a circle at the specified position,
# with the specified radius
def draw_circle(radius, position="relative"):
    draw_start = get_actual_draw_position(position)
    draw_start[0] += radius  # Make position circle origin

    pyautogui.moveTo(draw_start)
    pyautogui.mouseDown()

    # Move in a curve
    # old_pause = pyautogui.PAUSE
    # pyautogui.PAUSE = 0
    origin = [draw_start[0] - radius, draw_start[1]]

    for i in range(360):
        rad = math.radians(i)
        new_p = [origin[0] + radius * math.sin(rad), origin[1] + radius * math.cos(rad)]
        if not is_on_canvas(new_p):
            continue

        pyautogui.moveTo(new_p)

    # pyautogui.PAUSE = old_pause
    pyautogui.mouseUp()


# Draws a line from the specified position to the end position
def draw_line(end_position, position="relative"):
    draw_start = get_actual_draw_position(position)
    pyautogui.moveTo(draw_start)

    # Draw line
    pyautogui.dragRel(end_position)


# Draws a rectangle at the specified position
def draw_rect(width, height, position="relative"):
    draw_start = get_actual_draw_position(position)
    pyautogui.moveTo(draw_start)

    direction = 1
    for _ in range(2):
        pyautogui.dragRel(direction * width, 0)
        pyautogui.dragRel(0, direction * height)
        direction *= -1


# Draws a square at the specifid position
def draw_square(width, position="relative"):
    draw_rect(width, width, position)


# ----=== Helper Functions ===---- #

# Puts the paint window in focus
def focus_paint_window():
    curr_mouse = pyautogui.position()

    pyautogui.click(pyautogui.size()[0] / 2, 5)
    pyautogui.moveTo(curr_mouse)


def get_actual_draw_position(position):
    actual_position = list(_canvas_pos)

    if type(position) == str:
        if position == "relative":
            actual_position = list(pyautogui.position())
    else:
        actual_position[0] += position[0]
        actual_position[1] += position[1]

    return actual_position


if __name__ == "__main__":
    print("This is a library, not a runnable script")
    sys.exit()
