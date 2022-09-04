import cv2
import numpy as np

images = []

import os

dir = os.path.dirname(os.path.abspath(__file__))

for file in os.listdir(dir + '/tiles/'):
    images.append(cv2.imread(dir + '/tiles/' + file))

def vconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    w_min = min(im.shape[1] for im in im_list)
    im_list_resize = [cv2.resize(im, (w_min, int(im.shape[0] * w_min / im.shape[1])), interpolation=interpolation)
                      for im in im_list]
    return cv2.vconcat(im_list_resize)


# im_v_resize = vconcat_resize_min(images)
# cv2.imwrite(dir + '/opencv_vconcat_resize.jpg', im_v_resize)

# # True

def hconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    h_min = min(im.shape[0] for im in im_list)
    im_list_resize = [cv2.resize(im, (int(im.shape[1] * h_min / im.shape[0]), h_min), interpolation=interpolation)
                      for im in im_list]
    return cv2.hconcat(im_list_resize)


def concat_tile(im_list_2d):
    return cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in im_list_2d])


def concat_tile_resize(im_list_2d, interpolation=cv2.INTER_CUBIC):
    im_list_v = [hconcat_resize_min(im_list_h, interpolation=interpolation) for im_list_h in im_list_2d]
    return vconcat_resize_min(im_list_v, interpolation=interpolation)

new_images = [cv2.imread(x) for x in [dir + '/all_game_images1.jpg',dir + '/all_game_images2.jpg',dir + '/all_game_images3.jpg']]

im_h_resize = hconcat_resize_min(new_images)
cv2.imwrite(dir + '/3_times_all_games.webp', im_h_resize, [int(cv2.IMWRITE_WEBP_QUALITY), 20])


exit()




im_tile_resize = concat_tile_resize([images[:4],images[4:8],images[8:12], images[12:]])
cv2.imwrite(dir + '/all_game_images1.jpg', im_tile_resize)
import random
random.shuffle(images)

im_tile_resize = concat_tile_resize([images[:4],images[4:8],images[8:12], images[12:]])
cv2.imwrite(dir + '/all_game_images2.jpg', im_tile_resize)
import random
random.shuffle(images)
im_tile_resize = concat_tile_resize([images[:4],images[4:8],images[8:12], images[12:]])
cv2.imwrite(dir + '/all_game_images3.jpg', im_tile_resize)