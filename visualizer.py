import cv2
import numpy as np
import os

class Image:
    def __init__(self, img_path, bboxes):
        self.img = cv2.imread(img_path)
        self.bboxes = self.get_xyxy(bboxes)

    def show_image(self):

        for bbox in self.bboxes:
            x_min, y_min, x_max, y_max = bbox
            cv2.rectangle(self.img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 5)
        cv2.imshow('window', self.img)
        cv2.waitKey()

    def get_xyxy(self, xywh):
        xyxy = []
        if xywh != []:
            for bbox in xywh:
                x_min = bbox[0]
                y_min = bbox[1]
                x_max = bbox[0] + bbox[2]
                y_max = bbox[1] + bbox[3]

                xyxy.append([x_min, y_min, x_max, y_max])
        return xyxy


def get_bboxes():
    with open('c6s1/bboxes.txt', 'r') as txt_file:
        bboxes_count = -1
        image_read = False
        bboxes = []
        images = []
        for line in txt_file.readlines():
            if line.rstrip().endswith('.jpg'):
                img_path = os.path.join('c6s1/frames', line.rstrip())
                bboxes_count = -1
                image_read = True
            elif len(line.strip()) == 1:
                bboxes_count = int(line)
                counter = bboxes_count
            else:
                bboxes_count -= 1
                bbox = []
                for coord in line.split():
                    bbox.append(int(float(coord)))

                bboxes.append(bbox)

            if bboxes_count == 0 and image_read == True:
                images.append(Image(img_path, bboxes))
                # print(f'{img_path}; {counter}; {bboxes}')
                bboxes = []

    return images
                



if __name__ == '__main__':
    images = get_bboxes()
    
    for image in images:
        image.show_image()
