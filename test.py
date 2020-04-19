import uiautomator2 as u2
import cv2, numpy as np
from cv import *


# a = {'asd':44}
# if a:
#     print(a(0))


#
d = u2.connect()
dWidth, dHeight = d.window_size()
print(dWidth, dHeight)
screen_before = d.screenshot(format="opencv")

# screen_before = UIMatcher.RotateClockWise90(screen_before)
cv2.imwrite('test.jpg', UIMatcher.RotateClockWise90(screen_before))
dic,vals = UIMatcher.findpic(screen_before,template_paths=['img/tongyi.jpg'])
print(dic,vals)
max_index_x ,max_index_y = dic[vals.index(max(vals))]
max_index_x = int(max_index_x*dWidth)
max_index_y = int(max_index_y* dHeight)
# d.click(max_index_x *dWidth, max_index_y * dHeight)
cv2.rectangle(screen_before, (0,0), (10,10),(0,0,255),2)
# d.click(max_index_x,max_index_y)
plt.show()
# cv2.imshow('res.png',screen_before)
# cv2.waitKey(0)

# a = {'1': 1,'2': 2,'3': 3,'4': 4,}
#
#
# print(a[:2])