import cv2

class Image:
    def __init__(self, img_path, bboxes):
        self.img = cv2.imread(img_path)
        self.bboxes = self.get_xyxy(bboxes)
        self.middle = self.get_mid_point()

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

    def get_mid_point(self):
        x_mid = self.bboxes[0] + self.bboxes[2] // 2
        y_mid = self.bboxes[1] + self.bboxes[3] // 2

        return (x_mid, y_mid)
