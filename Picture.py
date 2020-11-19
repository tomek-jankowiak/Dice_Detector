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

        self.kernel = np.ones((3, 3), np.uint8)

    def process_picture(self):
        faces = self.find_faces()
        for face in faces:
            min_x, min_y = np.min(face[:, 0]), np.min(face[:, 1])
            max_x, max_y = np.max(face[:, 0]), np.max(face[:, 1])
            crop_img = self.img_gray[min_y:max_y, min_x:max_x]
            pips = self.find_pips(crop_img)
            textcoord = (int((max_x+min_x)/2), int(min_y - 10))
            cv.putText(self.img, str(len(pips)), textcoord, cv.FONT_HERSHEY_COMPLEX, 5, (0,0,255), 5)

        cv.drawContours(self.img, faces, -1, (255, 0, 0), 5)
        plt.figure(figsize=(6, 6))
        plt.imshow(self.img)
        plt.show()

    def find_faces(self):
        squares = []
        blur = cv.medianBlur(self.img_gray, 5)

        for thresh in range(0, 255, 26):
            _retr, binary = cv.threshold(blur, thresh, 255, cv.THRESH_BINARY)
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

    def find_pips(self, crop_img):
        crop_img = cv.GaussianBlur(crop_img, (5, 5), 0)

        params = cv.SimpleBlobDetector_Params()

        params.filterByArea = True
        params.minArea = 50
        params.maxArea = 20000

        params.filterByCircularity = True
        params.minCircularity = 0.5

        params.filterByInertia = True
        params.minInertiaRatio = 0.75

        detector = cv.SimpleBlobDetector_create(params)
        keypoints = detector.detect(crop_img)

        im_with_keypoints = cv.drawKeypoints(crop_img, keypoints, np.array([]), (0, 0, 255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        plt.figure(figsize=(6, 6))
        plt.imshow(im_with_keypoints)
        plt.show()

        return keypoints


