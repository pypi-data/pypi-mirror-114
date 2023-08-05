import sys

from je_auto_control.utils.exception import exception_tag
from je_auto_control.utils.exception.exceptions import AutoControlCantFindKeyException
from je_auto_control.utils.exception.exceptions import AutoControlKeyboardException
from je_auto_control.wrapper.platform_wrapper import keyboard
from je_auto_control.wrapper.platform_wrapper import keys_table


def press_key(keycode, is_shift=False):
    try:
        keycode = keys_table.get(keycode)
    except Exception:
        raise AutoControlCantFindKeyException(exception_tag.cant_find_key)
    try:
        if sys.platform in ["win32", "cygwin", "msys", "linux", "linux2"]:
            keyboard.press_key(keycode)
        elif sys.platform in ["darwin"]:
            keyboard.press_key(keycode, is_shift=is_shift)
    except Exception:
        raise AutoControlKeyboardException(exception_tag.keyboard_press_key)


def release_key(keycode, is_shift=False):
    try:
        keycode = keys_table.get(keycode)
    except Exception:
        raise AutoControlCantFindKeyException(exception_tag.cant_find_key)
    try:
        if sys.platform in ["win32", "cygwin", "msys", "linux", "linux2"]:
            keyboard.release_key(keycode)
        elif sys.platform in ["darwin"]:
            keyboard.release_key(keycode, is_shift=is_shift)
    except Exception:
        raise AutoControlKeyboardException(exception_tag.keyboard_release_key)


def type(keycode, is_shift=False):
    try:
        press_key(keycode, is_shift)
        release_key(keycode, is_shift)
    except Exception:
        raise AutoControlKeyboardException(exception_tag.keyboard_type_key)
