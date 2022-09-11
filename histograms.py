import cv2
from typing import List

from image import Image
from visualizer import get_images


def compare_histograms(prev: Image, current: Image) -> List:
    prev_hists = prev.get_upper_histograms()
    current_hists = current.get_upper_histograms()

    hists_similarity = []
    for current_hist in current_hists:
        hist_similarity = []
        for prev_hist in prev_hists:
            hist_similarity.append(cv2.compareHist(current_hist, prev_hist, cv2.HISTCMP_CORREL))
        hists_similarity.append(hist_similarity)
    
    return hists_similarity
