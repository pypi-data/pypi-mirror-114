import time

from je_auto_control import locate_image_center

time.sleep(2)
# detect_threshold 0~1 , 1 is absolute equal
image_data = locate_image_center("../../../test_template.png", detect_threshold=0.9, draw_image=False)
print(image_data)
