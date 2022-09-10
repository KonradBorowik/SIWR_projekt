from turtle import distance
from typing import List
import cv2
from image import Image
from visualizer import get_images
from histograms import compare_histograms
from distance import calc_dist


def f_b(prev_bbox_count: int, next_bbox_count: int):
    matrix = []
    for ver in range(prev_bbox_count+1):
        row = []
        for hor in range(next_bbox_count+1):
            if ver == hor != 0:
                row.append(0)
            else:
                row.append(1)
        
        matrix.append(row)

    print(matrix)


def calc_factor(hists: List, distances: List):# f_u ?
    prob = []
    for i_ob, object in enumerate(hists):
        print(f'object {i_ob}: {object}')
        mean = []
        for i_bb, hist in enumerate(object):
            print(f'hist {i_bb}: {hist}')
            mean.append((hist * 5 + distances[i_ob][i_bb] * 10) / (5 + 10))
            print(mean)
            
        prob.append(min(mean)) 
    print(prob)


if __name__ == '__main__':
    images = get_images()
    for i, image in enumerate(images):
        hists = []
        distances = []
        if i < len(images) -1:
            print(f'pair {i}')
            if image.bbox_count == 0 or images[i+1].bbox_count == 0:
                print("empty")
                continue

            hists = compare_histograms(image, images[i+1])
            distances = calc_dist(image, images[i+1])

            calc_factor(hists, distances)

            f_b(image.bbox_count, images[i+1].bbox_count)

            if i == 5:
                break
