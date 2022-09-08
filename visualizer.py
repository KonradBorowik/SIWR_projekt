import os
from typing import List
from image import Image


def get_images() -> List[Image]:
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
            else:
                bboxes_count -= 1
                bbox = []
                for coord in line.split():
                    bbox.append(int(float(coord)))

                bboxes.append(bbox)

            if bboxes_count == 0 and image_read == True:
                images.append(Image(img_path, bboxes))
                bboxes = []

    return images
