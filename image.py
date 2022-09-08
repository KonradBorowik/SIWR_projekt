import cv2
import numpy as np

class Image:
    def __init__(self, img_path, bboxes):
        self.img = cv2.imread(img_path)
        self.bboxes = bboxes
        self.bbox_count = len(bboxes)

        self.middle = self.get_mid_point()
        self.bboxes_xyxy = self.get_xyxy()

    def show_image(self):
        for bbox in self.bboxes:
            x_min, y_min, x_max, y_max = bbox
            cv2.rectangle(self.img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 5)
        cv2.imshow('window', self.img)
        cv2.waitKey()

    def get_xyxy(self, xywh):
        xyxy = []
        if self.bboxes != []:
            for bbox in self.bboxes:
                x_min = bbox[0]
                y_min = bbox[1]
                x_max = bbox[0] + bbox[2]
                y_max = bbox[1] + bbox[3]

                xyxy.append([x_min, y_min, x_max, y_max])
        return xyxy

    def get_mid_point(self):
        mid = []
        if self.bboxes != []:
            for bbox in self.bboxes_xyxy:
                x_mid = bbox[0] + bbox[2] // 2
                y_mid = bbox[1] + bbox[3] // 2
                mid.append((x_mid, y_mid))

            return mid

    def get_bgr_histogram(self):
        if self.bboxes != []:
            for bbox in self.bboxes:
                hist_x_min = int(bbox[0] + bbox[2]*0.1)
                hist_x_max = int(bbox[0] + bbox[2]*0.9)
                hist_y_min = bbox[0]
                hist_y_max = bbox[0] + bbox[3]

                hist_bbox = self.img[hist_x_min:hist_x_max][hist_y_min:hist_y_max]
                cv2.imshow('histogram', hist_bbox)
                cv2.waitKey()



