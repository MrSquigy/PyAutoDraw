import pyautodraw.pyautodraw as pad
import pyautogui
import random

caches = {}

# ----=== Helper Functions ===---- #


def calc_fib_cache(n):
    if "fibonacci" not in caches:
        caches["fibonacci"] = [0, 1]
    fib_nums = caches["fibonacci"]
    fib_cache_length = len(fib_nums)

    while fib_cache_length <= n:
        fib_nums.append(fib_nums[fib_cache_length - 2] + fib_nums[fib_cache_length - 1])
        fib_cache_length += 1


def fibonacci(n):
    if "fibonacci" not in caches or len(caches["fibonacci"]) < n:
        calc_fib_cache(n)

    return caches["fibonacci"][n]


# ----=== Drawings ===---- #


def cool_squares(init_length):
    length = init_length
    while round(length) > 0:
        pad.draw_square(length)
        pad.change_colour()
        length -= init_length / 10

    length = init_length
    pyautogui.moveRel(init_length / 10, init_length / 10)

    while length > 0:
        pad.draw_square(length)

        inc = init_length / 10
        pyautogui.moveRel(inc, inc)
        length -= inc

        pad.change_colour()


def fib_squares(num):
    for i in range(num, 0, -1):
        pad.draw_square(fibonacci(i))


# Random positions of random square sizes
def random_squares(num):
    canvas_x, canvas_y = pad.get_canvas_size()

    for _ in range(num):
        pad.change_colour()
        r_len = random.randint(1, canvas_y)
        r_pos = (
            random.randint(0, canvas_x - r_len),
            random.randint(0, canvas_y - r_len),
        )
        pad.draw_square(r_len, r_pos)


if __name__ == "__main__":
    pad.init()
    random_squares(11)
