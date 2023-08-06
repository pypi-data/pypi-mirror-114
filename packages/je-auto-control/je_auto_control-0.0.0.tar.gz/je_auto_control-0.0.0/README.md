# je_auto_control

## install

```
pip install je_auto_control
```

## Info

* Dev env
    * windows 11
    * osx 11 big sur
    * ubuntu 20.0.4

<br>

* Test on
    * windows 11
    * osx 11 big sur
    * ubuntu 20.0.4

<br>

* Notice! change image detect test default path to your image path

## TODO

* more feature

## example

* All test and example in test dir

## how to use

#### keyboard

```python
import time

from je_auto_control import type
from je_auto_control import keys_table

"""
check keys
"""
print(keys_table.keys())

"""
Linux in every type and press then release need stop 0.01 time in my computer,i'm not sure it's right?

example:
    type("T")
    time.sleep(0.01)
    type("E")
    time.sleep(0.01)
    type("S")
    time.sleep(0.01)
    type("T")
    time.sleep(0.01)

or:
    press_key("T")
    release_key("T")
    time.sleep(0.01)
"""

type("T")
type("E")
type("S")
type("T")
```

#### mouse

```python
import time

from je_auto_control import position
from je_auto_control import set_position
from je_auto_control import press_mouse
from je_auto_control import release_mouse
from je_auto_control import click_mouse
from je_auto_control import mouse_table

time.sleep(1)

print(position())
set_position(809, 388)

print(mouse_table.keys())

press_mouse("mouse_right")
release_mouse("mouse_right")
press_mouse("mouse_left")
release_mouse("mouse_left")
click_mouse("mouse_left")

```

#### scroll

```python
from je_auto_control import scroll

scroll(100)

```

#### screen

```python
from je_auto_control import size

print(size())
```

#### locate image

```python
import time

from je_auto_control import locate_image_center

time.sleep(2)
# detect_threshold 0~1 , 1 is absolute equal
image_data = locate_image_center("../../../test_template.png", detect_threshold=0.9, draw_image=False)
print(image_data)
```

#### locate all image

```python
import time

from je_auto_control import locate_all_image

time.sleep(2)
# detect_threshold 0~1 , 1 is absolute equal
image_data = locate_all_image("../../../test_template.png", detect_threshold=0.9, draw_image=False)
print(image_data)
```

#### locate and click image in center

```python
import time

from je_auto_control import locate_and_click

time.sleep(2)
# detect_threshold 0~1 , 1 is absolute equal
image_data = locate_and_click("../../../test_template.png", "mouse_left", detect_threshold=0.9,
                              draw_image=False)
print(image_data)

```
