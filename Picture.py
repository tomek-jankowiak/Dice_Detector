from matplotlib import pyplot as plt
import cv2 as cv
import numpy as np


def angle_cos(p0, p1, p2):
    d1, d2 = (p0 - p1).astype('float'), (p2 - p1).astype('float')
    return abs(np.dot(d1, d2) / np.sqrt(np.dot(d1, d1) * np.dot(d2, d2)))


def distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


class Picture:
    def __init__(self, filename):
        self.img = cv.imread(filename)
        self.img_gray = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)

    def process_picture(self):
        faces = self.find_faces()

        cv.drawContours(self.img, faces, -1, (255, 0, 0), 5)
        plt.figure(figsize=(6, 6))
        plt.imshow(self.img)
        plt.show()

    def find_faces(self):
        tmp = self.img_gray
        tmp = cv.GaussianBlur(tmp, (5, 5), 0, 0)

        squares = []

        for thresh in range(0, 255, 26):
            _retr, binary = cv.threshold(tmp, thresh, 255, cv.THRESH_BINARY)
            contours, _hierarchy = cv.findContours(binary, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv.arcLength(cnt, True)
                cnt = cv.approxPolyDP(cnt, 0.02 * cnt_len, True)
                if len(cnt) == 4 and cv.contourArea(cnt) > 1000 and cv.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos(cnt[i], cnt[(i + 1) % 4], cnt[(i + 2) % 4]) for i in range(4)])
                    if max_cos < 0.1 and cnt[0, 0] > 10 and cnt[0, 1] > 10:
                        squares.append(cnt)

        mass_centers = []
        for square in squares:
            m = cv.moments(square)
            mass_centers.append((m['m10'] / m['m00'], m['m01'] / m['m00']))

        indexes = []
        for i in range(len(mass_centers)):
            add = True
            for j in range(i - 1, -1, -1):
                if distance(mass_centers[i], mass_centers[j]) < 20:
                    add = False
            if add:
                indexes.append(i)

        return [squares[i] for i in indexes]

