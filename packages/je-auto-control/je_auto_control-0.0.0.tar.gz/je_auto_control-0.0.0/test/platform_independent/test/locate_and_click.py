import time

from je_auto_control import locate_and_click

time.sleep(2)
# detect_threshold 0~1 , 1 is absolute equal
image_data = locate_and_click("../../../test_template.png", "mouse_left", detect_threshold=0.9,
                              draw_image=False)
print(image_data)
