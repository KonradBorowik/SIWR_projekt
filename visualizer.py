import cv2
import numpy as np
import os

class Image:
    def __init__(self, img_path, bboxes):
        self.img = cv2.imread(img_path)

    def show_image(self):
        cv2.imshow('window', self.img)
        cv2.waitKey()

        x_min = int(float(x_min))
        x_max = int(float(x_max))
        y_min = int(float(x_min))
        y_max = int(float(y_max))
        cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 5)


def get_bboxes():
    with open('c6s1/bboxes.txt', 'r') as txt_file:
        bboxes_count = 0
        image_read = False
        bboxes = []
        images = []
        for line in txt_file.readlines():
            if bboxes_count == 0 and line.rstrip().endswith('.jpg'):
                img_path = os.path.join('c6s1/frames', line.rstrip())
                image_read = True
            elif len(line.rstrip()) == 1:
                bboxes_count = int(line)
            else:
                bboxes_count -= 1
                bboxes.append(line.split())

            if bboxes_count == 0 and image_read == True:
                images.append(Image(img_path, bboxes))


if __name__ == '__main__':
    get_bboxes()
