from typing import List
from image import Image
from visualizer import get_images
from math import sqrt


def calc_dist(prev: Image, next: Image) -> List:
    prev_mids = prev.get_mid_point()
    next_mids = next.get_mid_point()
    dists = []
    for prev_mid in prev_mids:
        dist = []
        for next_mid in next_mids:
            dist.append(sqrt(abs(prev_mid[0] - next_mid[0])**2 + abs(prev_mid[1] - next_mid[1])**2))
        
        dists.append(dist)

    return dists
