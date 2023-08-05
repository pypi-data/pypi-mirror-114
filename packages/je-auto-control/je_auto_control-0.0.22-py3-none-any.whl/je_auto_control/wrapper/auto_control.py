import sys

from je_auto_control.utils.exception import exception_tag
from je_auto_control.utils.exception.exceptions import AutoControlCantFindKeyException
from je_auto_control.utils.exception.exceptions import AutoControlKeyboardException
from je_auto_control.utils.exception.exceptions import AutoControlMouseException
from je_auto_control.utils.exception.exceptions import AutoControlScreenException
from je_auto_control.wrapper.platform_wrapper import keyboard
from je_auto_control.wrapper.platform_wrapper import keys_table
from je_auto_control.wrapper.platform_wrapper import mouse
from je_auto_control.wrapper.platform_wrapper import mouse_table
from je_auto_control.wrapper.platform_wrapper import screen
from je_auto_control.wrapper.platform_wrapper import special_table

protect_sleep_time = 0.001


def press_key(keycode, is_shift=False):
    try:
        keycode = keys_table.get(keycode)
    except Exception:
        raise AutoControlCantFindKeyException(exception_tag.cant_find_key_error_tag)
    try:
        if sys.platform in ["win32", "cygwin", "msys", "linux", "linux2"]:
            keyboard.press_key(keycode)
        elif sys.platform in ["darwin"]:
            keyboard.press_key(keycode, is_shift=is_shift)
    except Exception:
        raise AutoControlKeyboardException(exception_tag.keyboard_press_key_error_tag)


def release_key(keycode, is_shift=False):
    try:
        keycode = keys_table.get(keycode)
    except Exception:
        raise AutoControlCantFindKeyException(exception_tag.cant_find_key_error_tag)
    try:
        if sys.platform in ["win32", "cygwin", "msys", "linux", "linux2"]:
            keyboard.release_key(keycode)
        elif sys.platform in ["darwin"]:
            keyboard.release_key(keycode, is_shift=is_shift)
    except Exception:
        raise AutoControlKeyboardException(exception_tag.keyboard_release_key_error_tag)


def type(keycode, is_shift=False):
    try:
        press_key(keycode, is_shift)
        release_key(keycode, is_shift)
    except Exception:
        raise AutoControlKeyboardException(exception_tag.keyboard_type_key_error_tag)


def position():
    try:
        return mouse.position()
    except Exception:
        raise AutoControlMouseException(exception_tag.mouse_get_position_error_tag)


def set_position(x, y):
    try:
        mouse.set_position(x=x, y=y)
    except Exception:
        raise AutoControlMouseException(exception_tag.mouse_set_position_error_tag)


def press_mouse(mouse_keycode, x=None, y=None):
    try:
        mouse_keycode = mouse_table.get(mouse_keycode)
    except Exception:
        raise AutoControlCantFindKeyException(exception_tag.cant_find_key_error_tag)
    try:
        now_x, now_y = position()
        if x is None:
            x = now_x
        if y is None:
            y = now_y
        if sys.platform in ["win32", "cygwin", "msys", "linux", "linux2"]:
            mouse.press_mouse(mouse_keycode)
        elif sys.platform in ["darwin"]:
            mouse.press_mouse(x, y, mouse_keycode)
    except Exception:
        raise AutoControlKeyboardException(exception_tag.mouse_press_mouse_error_tag)


def release_mouse(mouse_keycode, x=None, y=None):
    try:
        mouse_keycode = mouse_table.get(mouse_keycode)
    except Exception:
        raise AutoControlCantFindKeyException(exception_tag.cant_find_key_error_tag)
    try:
        now_x, now_y = position()
        if x is None:
            x = now_x
        if y is None:
            y = now_y
    except Exception:
        raise AutoControlKeyboardException(exception_tag.mouse_get_position_error_tag)
    try:
        if sys.platform in ["win32", "cygwin", "msys", "linux", "linux2"]:
            mouse.release_mouse(mouse_keycode)
        elif sys.platform in ["darwin"]:
            mouse.release_mouse(x, y, mouse_keycode)
    except Exception:
        raise AutoControlKeyboardException(exception_tag.mouse_release_mouse_error_tag)


def click_mouse(mouse_keycode, x=None, y=None):
    try:
        mouse_keycode = mouse_table.get(mouse_keycode)
    except Exception:
        raise AutoControlCantFindKeyException(exception_tag.cant_find_key_error_tag)
    try:
        now_x, now_y = position()
        if x is None:
            x = now_x
        if y is None:
            y = now_y
    except Exception:
        raise AutoControlKeyboardException(exception_tag.mouse_get_position_error_tag)
    try:
        if sys.platform in ["win32", "cygwin", "msys", "linux", "linux2"]:
            mouse.click_mouse(mouse_keycode)
        elif sys.platform in ["darwin"]:
            mouse.click_mouse(x, y, mouse_keycode)
    except Exception:
        raise AutoControlKeyboardException(exception_tag.mouse_click_mouse_error_tag)


def scroll(scroll_value, x=None, y=None, scroll_direction="scroll_down"):
    """"
    scroll_direction = 4 : direction up
    scroll_direction = 5 : direction down
    scroll_direction = 6 : direction left
    scroll_direction = 7 : direction right
    """
    try:
        now_cursor_x, now_cursor_y = position()
    except Exception:
        raise AutoControlMouseException(exception_tag.mouse_get_position_error_tag)
    try:
        width, height = size()
        if x is None:
            x = now_cursor_x
        else:
            if x < 0:
                x = 0
            elif x >= width:
                x = width - 1
        if y is None:
            y = now_cursor_y
        else:
            if y < 0:
                y = 0
            elif y >= height:
                y = height - 1
    except Exception:
        raise AutoControlScreenException(exception_tag.screen_get_size_error_tag)
    try:
        if sys.platform in ["win32", "cygwin", "msys"]:
            mouse.scroll(scroll_value, x, y)
        elif sys.platform in ["darwin"]:
            mouse.scroll(scroll_value)
        elif sys.platform in ["linux", "linux2"]:
            scroll_direction = special_table.get(scroll_direction)
            mouse.scroll(scroll_value, scroll_direction)
    except Exception:
        raise AutoControlMouseException(exception_tag.mouse_click_mouse_error_tag)


def size():
    try:
        return screen.size()
    except Exception:
        raise AutoControlScreenException(exception_tag.screen_get_size_error_tag)
