from matplotlib import pyplot as plt
from scipy.ndimage import binary_fill_holes
import cv2 as cv
import numpy as np


class Picture:
    def __init__(self, filename):
        self.img = cv.imread(filename)
        self.img_gray = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)

    def process_picture(self):
        faces = self.find_faces()
        cv.drawContours(self.img, faces, -1, (255, 0, 0), 3)

        plt.figure(figsize=(6, 6))
        plt.imshow(self.img)
        plt.show()

    def find_faces(self):
        ret, thresh = cv.threshold(self.img_gray, 180, 255, 0)
        edged = cv.Canny(thresh, 100, 200)
        filled = np.array(binary_fill_holes(edged), dtype=np.uint8)
        edged2 = cv.Canny(filled, 0, 1)
        contours, hierarchy = cv.findContours(edged2, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

        return contours

