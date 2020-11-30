from matplotlib import pyplot as plt, rc
import cv2 as cv
import numpy as np


def angle_cos(p0, p1, p2):
    d1, d2 = (p0 - p1).astype('float'), (p2 - p1).astype('float')
    return abs(np.dot(d1, d2) / np.sqrt(np.dot(d1, d1) * np.dot(d2, d2)))


def distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


class Picture:
    def __init__(self, filename):
        self.filename = filename
        self.img = cv.imread(filename)
        self.img_gray = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)

        height, width, channels = self.img.shape
        self.height = height
        self.width = width

        self.kernel = np.ones((3, 3), np.uint8)

    def process_picture(self):
        squares = self.find_faces()
        faces = []
        for square in squares:
            min_x, min_y = np.min(square[:, 0]), np.min(square[:, 1])
            max_x, max_y = np.max(square[:, 0]), np.max(square[:, 1])
            crop_img = self.img_gray[min_y:max_y, min_x:max_x]
            pips = self.find_pips(crop_img)
            if len(pips) > 0:
                faces.append(square)
                textcoord = (int((max_x+min_x)/2), int(min_y - 10))
                cv.putText(self.img, str(len(pips)), textcoord, cv.FONT_HERSHEY_COMPLEX, 10, (255, 0, 0), 7)

        cv.drawContours(self.img, faces, -1, (0, 0, 255), 10)
        plt.figure(figsize=(6, 6))
        plt.imshow(self.img)
        plt.show()

    def find_faces(self):
        squares = []
        blur = cv.medianBlur(self.img_gray, 5)
        for thresh in range(255, 0, -15):
            _retr, binary = cv.threshold(blur, thresh, 255, cv.THRESH_BINARY)
            contours, _hierarchy = cv.findContours(binary, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                cnt_len = cv.arcLength(cnt, True)
                cnt = cv.approxPolyDP(cnt, 0.02 * cnt_len, True)

                if 4 <= len(cnt) <= 6 and 0.005 * (self.height * self.width) < cv.contourArea(cnt) < 0.1 * \
                        (self.height * self.width) and cv.isContourConvex(cnt):
                    rect = cv.minAreaRect(cnt)
                    (x, y), (width, height), angle = rect
                    aspect_ratio = min(width, height) / max(width, height)
                    if aspect_ratio > 0.88:
                        box = cv.boxPoints(rect)
                        box = np.int0(box)
                        squares.append(box)

        mass_centers = []
        for square in squares:
            m = cv.moments(square)
            mass_centers.append((m['m10'] / m['m00'], m['m01'] / m['m00']))

        indexes = []
        for i in range(len(mass_centers)):
            add = True
            for j in range(i - 1, -1, -1):
                if distance(mass_centers[i], mass_centers[j]) < 100:
                    add = False
            if add:
                indexes.append(i)

        return [squares[i] for i in indexes]

    def find_pips(self, crop_img):
        crop_img = cv.GaussianBlur(crop_img, (5, 5), 0)

        params = cv.SimpleBlobDetector_Params()

        params.minThreshold = 0
        params.maxThreshold = 255

        params.filterByArea = True
        params.minArea = 150
        params.maxArea = 35000

        params.filterByCircularity = True
        params.minCircularity = 0.4

        params.filterByInertia = True
        params.minInertiaRatio = 0.6

        params.filterByConvexity = True
        params.minConvexity = 0.3

        detector = cv.SimpleBlobDetector_create(params)
        keypoints = detector.detect(crop_img)

        '''im_with_keypoints = cv.drawKeypoints(crop_img, keypoints, np.array([]), (0, 0, 255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        plt.figure(figsize=(6, 6))
        plt.imshow(im_with_keypoints)
        plt.show()'''

        return keypoints
