import cv2
from typing import List

from image import Image
from visualizer import get_images


def compare_histograms(prev: Image, next: Image) -> List:
    prev_hists = prev.get_upper_histograms()
    next_hists = next.get_upper_histograms()

    hists_similarity = []
    for prev_hist in prev_hists:
        hist_similarity = []
        for next_hist in next_hists:
            hist_similarity.append(cv2.compareHist(prev_hist, next_hist, cv2.HISTCMP_CORREL))
        hists_similarity.append(hist_similarity)
    
    return hists_similarity

if __name__ == '__main__':
    images = get_images()
    hists = []
    for i, image in enumerate(images):
        if i < len(images) -1:
            hists.append(compare_histograms(image, images[i+1]))
    print(hists)
