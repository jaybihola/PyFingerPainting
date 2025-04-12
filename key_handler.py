from pynput import keyboard
import constants
from state import state


def on_press(key):
    if state["current_mode"] == constants.MODE_SWITCHER:
        if key == keyboard.KeyCode.from_char('f'):
            state["current_mode"] = constants.FREE_DRAW_MODE
        if key == keyboard.KeyCode.from_char('s'):
            state["current_mode"] = constants.SHAPE_MODE
        if key == keyboard.KeyCode.from_char('v'):
            state["current_mode"] = constants.VIEW_MODE

    if key == keyboard.Key.space:
        state["current_mode"] = constants.MODE_SWITCHER

    if state["current_mode"] == constants.FREE_DRAW_MODE or state["current_mode"] == constants.SHAPE_MODE:
        if key == keyboard.KeyCode.from_char('c'):
            prev_mode = state["current_mode"]
            state["current_mode"] = constants.COLOR_MODE

    if state["current_mode"] == constants.COLOR_MODE:
        if key == keyboard.KeyCode.from_char('r'):
            print('Color changed to RED')
            state["current_color"] = constants.RED
            if state["prev_mode"]:
                state["current_mode"] = prev_mode
                state["prev_mode"] = None
        if key == keyboard.KeyCode.from_char('b'):
            print('Color changed to BLUE')
            state["current_color"] = constants.BLUE
            if state["prev_mode"]:
                state["current_mode"] = prev_mode
                state["prev_mode"] = None
        if key == keyboard.KeyCode.from_char('g'):
            print('Color changed to GREEN')
            state["current_color"] = constants.GREEN
            if state["prev_mode"]:
                state["current_mode"] = prev_mode
                state["prev_mode"] = None
        if key == keyboard.KeyCode.from_char('y'):
            print('Color changed to YELLOW')
            state["current_color"] = constants.YELLOW
            if state["prev_mode"]:
                state["current_mode"] = prev_mode
                state["prev_mode"] = None
        if key == keyboard.KeyCode.from_char('p'):
            print('Color changed to PURPLE')
            state["current_color"] = constants.PURPLE
            if prev_mode:
                state["current_mode"] = prev_mode
                state["prev_mode"] = None
    if key == keyboard.Key.esc:
        print("Clearing")
        state["points"].clear()


def on_release(key):
    pass


def enable_keyboard():
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()
