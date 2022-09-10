from turtle import distance
import cv2
from image import Image
from visualizer import get_images
from histograms import compare_histograms
from distance import calc_dist

if __name__ == '__main__':
    images = get_images()
    hists = []
    distances = []
    for i, image in enumerate(images):
        if i < len(images) -1:
            if image.bbox_count == 0 or images[i+1].bbox_count == 0:
                print("empty")
                continue
            
            hists.append(compare_histograms(image, images[i+1]))
            distances.append(calc_dist(image, images[i+1]))
