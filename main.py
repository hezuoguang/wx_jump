#coding:utf-8
#Created by weimi on 18/1/4.

from PIL import Image

import wda
import numpy as np
import cv2 as cv
import matplotlib.animation as animation
import matplotlib.pyplot as plt

# 6s
time_coe = 0.00194
# 6s plus
# time_coe = 0.00116

chessman_offset_x = 25
chessman_offset_y = 120
#
# chessman_offset_x = 67
# chessman_offset_y = 228

# 棋子模板
chessman_template = cv.imread('chessman_6s.png', 0)
# chessman_template = cv.imread('chessman_6s_plus.png', 0)

wda_client = wda.Client('http://192.168.31.171:8100')
wda_session = wda_client.session()

# 棋盘/游戏界面
chessman_map_name = 'wx_jump.png'

# 截屏
def wda_screenshot(image_name):
    global wda_client
    wda_client.screenshot(image_name)

# 获取截屏图片
def np_image_with_screenshot():
    import time
    time.sleep(1)
    global chessman_map_name
    image_name = chessman_map_name
    # image_name = 'WechatIMG35.jpeg'
    wda_screenshot(image_name=image_name)
    print('----')
    return np.array(Image.open(image_name))

def update_image(frame, *fargs):

    im, fig = fargs[0], fargs[1]
    if fig.can_update == True:
        setattr(fig, 'can_update', False)
        im.set_array(np_image_with_screenshot())
    return im,

# 获取棋子坐标
def chessman_point():
    global chessman_template
    global chessman_map_name
    image_name = chessman_map_name
    # image_name = 'WechatIMG35.jpeg'
    img = cv.imread(image_name, 0)
    result = cv.matchTemplate(img, chessman_template, cv.TM_CCOEFF_NORMED)
    min_val1, max_val1, min_loc1, max_loc1 = cv.minMaxLoc(result)
    return max_loc1[0] + chessman_offset_x, max_loc1[1] + chessman_offset_y

# 跳跃
def jump(start_x, start_y, end_x, end_y):
    distance = (start_y - end_y) ** 2 + (start_x - end_x) ** 2
    press_time = distance ** 0.5 * time_coe
    global wda_session
    import random
    touch_x = random.randint(140, 150)
    touch_y = random.randint(140, 150)
    print('jump', touch_x, touch_y, press_time)
    wda_session.tap_hold(touch_x, touch_y, press_time)

def on_press(event):
    if event.inaxes == None:
        print("none")
        return

    fig = event.inaxes.figure
    # 防止误击
    if fig.can_update == True:
        return
    start_x, start_y = chessman_point()

    end_x = event.xdata
    end_y = event.ydata
    print('start', start_x, start_y)
    print('end', end_x, end_y)
    setattr(fig, 'can_update', True)
    jump(start_x=start_x, start_y=start_y, end_x=end_x, end_y=end_y)


def main():
    fig = plt.figure()
    np_img = np_image_with_screenshot()
    im = plt.imshow(np_img, animated=True)
    setattr(fig, 'can_update', False)
    fig.canvas.mpl_connect('button_press_event', on_press)
    ani = animation.FuncAnimation(fig, update_image, fargs=(im, fig), interval=100, blit=True)
    plt.show()


if __name__ == '__main__':
    main()