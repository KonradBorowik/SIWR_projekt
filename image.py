from tokenize import String
from typing import List
import cv2
import numpy as np

class Image:
    def __init__(self, img_path: String, bboxes: List) -> None:
        self.img = cv2.imread(img_path)
        self.bboxes = bboxes
        self.bbox_count = len(bboxes)
        self.bboxes_xyxy = self.get_xyxy()
        self.middle = self.get_mid_point()
        self.upper_hists = self.get_upper_histograms()

    def show_image(self) -> None:
        for bbox in self.bboxes_xyxy:
            x_min, y_min, x_max, y_max = bbox
            cv2.rectangle(self.img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 5)
        cv2.imshow('window', self.img)
        cv2.waitKey()

    def get_xyxy(self) -> List:
        xyxy = []
        if self.bboxes != []:
            for bbox in self.bboxes:
                x_min = bbox[0]
                y_min = bbox[1]
                x_max = bbox[0] + bbox[2]
                y_max = bbox[1] + bbox[3]

                xyxy.append([x_min, y_min, x_max, y_max])
        return xyxy

    def get_mid_point(self) -> List:
        if self.bboxes != []:
            mid = []
            for bbox in self.bboxes_xyxy:
                x_mid = bbox[0] + bbox[2] // 2
                y_mid = bbox[1] + bbox[3] // 2
                mid.append((x_mid, y_mid))

            return mid

    def get_upper_histograms(self) -> List:
        if self.bboxes != []:
            hists = []
            # background = np.zeros((self.img.shape[0], self.img.shape[1], 3), dtype=np.uint8)
            for bbox in self.bboxes:
                hist_x_min = bbox[0] + int(bbox[2]*0.1)
                hist_x_max = bbox[0] + int(bbox[2]*0.9)
                hist_y_min = bbox[1]
                hist_y_max = bbox[1] + bbox[3] // 2
                # background[hist_y_min:hist_y_max, hist_x_min:hist_x_max] = self.img[hist_y_min:hist_y_max, hist_x_min:hist_x_max]
                hists.append(self.img[hist_y_min:hist_y_max, hist_x_min:hist_x_max])
            
            # cv2.imshow('histogram', background)
            # cv2.waitKey()
            return hists
        else:
            pass
