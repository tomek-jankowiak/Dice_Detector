import cv2 as cv


def result(picture):
    output_filename = picture.filename.replace('images', 'output')
    cv.imwrite(output_filename, picture.img)

