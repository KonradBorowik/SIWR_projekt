from typing import List
from image import Image
from visualizer import get_images
from math import sqrt


def calc_dist(prev: Image, current: Image) -> List:
    prev_mids = prev.get_mid_point()
    current_mids = current.get_mid_point()
    dists = []
    for current_mid in current_mids:
        dist = []
        for prev_mid in prev_mids:
            dist.append(sqrt((abs(prev_mid[0] - current_mid[0]) / prev.img.shape[1] **2) + abs(prev_mid[1] - current_mid[1]) / prev.img.shape[0] **2))
        
        dists.append(dist)

    return dists
