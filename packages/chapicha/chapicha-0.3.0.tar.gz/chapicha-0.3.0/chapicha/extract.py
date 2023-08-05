import itertools
from operator import itemgetter
from math import ceil, log
import sys


import cv2
import numpy as np
import pytesseract


from chapicha.util import TextShade, TextFlow, GroupDict, MergeStrategy
from chapicha.transform import scale


MAX_AREA = 1000000


# FIXME: FInd a bettern way to detect text in image
def findTextRegions(img: np.ndarray, text_color: TextShade = TextShade.DARK):
    if text_color == TextShade.LIGHT:
        thresh = cv2.THRESH_BINARY
    else:
        thresh = cv2.THRESH_BINARY_INV

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 180, 255, thresh)

    kernel = np.ones((7, 7), np.uint8)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def showTextRegions(img, contours):
    disp = img.copy()
    for rect in contours:
        #  rect = cv2.boundingRect(c)
        x, y, w, h = rect
        cv2.rectangle(disp, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("Frame", disp)
    while "q" != chr(cv2.waitKey() & 255):
        pass
    cv2.destroyAllWindows()


def showGrouped(img, grouped):
    disp = img.copy()
    colors = itertools.cycle([(255, 0, 0), (0, 255, 0), (0, 0, 255)])
    for k, group in grouped.items():
        c = next(colors)
        for rect in group:
            #  rect = cv2.boundingRect(c)
            x, y, w, h = rect
            cv2.rectangle(disp, (x, y), (x + w, y + h), c, 2)
    cv2.imshow("Frame", disp)
    while "q" != chr(cv2.waitKey() & 255):
        pass
    cv2.destroyAllWindows()


def filterDivergent(iterable, factor=0.9):
    """Filter out bounding boxes that are unlikely to contain text."""
    avg = sum([x[2] * x[3] for x in iterable]) / len(iterable)

    def filterfunc(val):
        val_avg = val[2] * val[3]
        return avg * (1 + factor) >= val_avg >= avg * (1 - factor)

    return filter(filterfunc, iterable)


def mergeBoundingBoxes(img, contours, flow=TextFlow.HORIZONTAL):
    """Reduce the number of bounding boxes by merging adjacent ones."""
    CLOSENESS = 20
    boundingBoxes = [cv2.boundingRect(c) for c in contours]
    grouped = GroupDict(filterDivergent(boundingBoxes), CLOSENESS)
    merged = []
    #  print(f"{grouped=}")
    for k, v in grouped.items():
        new_x, _, _, _ = min(v, key=itemgetter(0))
        _, new_y, _, _ = min(v, key=itemgetter(1))
        max_x = max(map(lambda x: x[0] + x[2], v))
        max_y = max(map(lambda x: x[1] + x[3], v))
        merged.append((new_x, new_y, max_x - new_x, max_y - new_y))

    #  print(f"{merged=}")
    return merged


def extract_text(
    img, text_color=TextShade.LIGHT, text_flow=TextFlow.HORIZONTAL
):
    contours = findTextRegions(img, TextShade.DARK)
    merged = mergeBoundingBoxes(img, contours)
    config = "-l eng --oem 3 --psm 7"
    text = []
    for rect in merged:
        (x, y, w, h) = rect
        x1, y1 = x + w, y + h
        roi = img[y:y1, x:x1, :]
        maybe_text = pytesseract.image_to_string(roi, config=config)
        if maybe_text:
            text.append(maybe_text)
    return list(reversed(text))


def sort_split(arr):
    """Auxiliary function for median_cut that sorts and splits buckets."""
    _, _, cols = arr.shape
    max_channel = 0
    max_diff = -1
    for c in range(cols):
        diff = np.ptp(arr[:, :, c])
        if diff > max_diff:
            max_diff = diff
            max_channel = c
    # sort 3D array with 'key' being max_channel
    sorted_arr = np.einsum(
        "iijk->ijk", arr[:, arr[:, :, max_channel].argsort()]
    )
    return np.array_split(sorted_arr, 2, axis=1)


# https://stackoverflow.com/a/4398799
def closest(x):
    return 2 ** int(ceil(log(x) / log(2)))


def make_n(colors, n, strategy=MergeStrategy.INTELLIGENT, difference=0.10):
    """Merge multiple colors together until into n colors"""
    if len(colors) < n:
        raise ValueError("Length of colors should be larger than n")
    colors = sorted(colors, key=lambda x: x[0])
    if strategy == MergeStrategy.NAIVE:
        # return first n
        try:
            return (colors[:n], n)
        except IndexError:
            return (colors, len(colors))
    else:
        # return first n but check they are different upto some given threshold
        last = colors.pop()
        merged = [last]
        while colors and len(merged) < n:
            current = colors.pop()
            print(current)
            if np.allclose(current, last, rtol=difference):
                pass
            else:
                merged.append(current)
            last = current
        return (merged, len(merged))


# FIXME
def median_cut(img, n):
    """MedianCut algorithm uses average for bucket aggregation."""
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    w, h, _ = img.shape
    if (area := w * h) >= MAX_AREA:  # arbitrary value to trigger image resize
        factor = area // MAX_AREA
        img = scale(img, factor=factor)
    buckets = [img]
    while len(buckets) < n:
        new_buckets = []
        for b in buckets:
            new_buckets.extend(sort_split(b))
        buckets = new_buckets
    result = []
    for b in buckets:
        w, h, cols = b.shape
        color = np.reshape(b, (w * h, 1, cols))
        elem = np.argmax(color)
        agg = np.rint(color[elem])
        result.append(np.reshape(agg, (3, 1)))
    return result


def extract_colors(img, n=4):
    colors = median_cut(img, closest(n))
    if len(colors) != n:
        try:
            print(f"Reducing {len(colors)} to {n} colors")
            print(colors)
            colors, x = make_n(colors, n)
            print(f"Found {x} colors")
        except ValueError:
            print("Image does not contain that many colors")
    return colors


def split_panels(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 7), 0)
    edges = cv2.Canny(blurred, 20, 30)
    edges_tight = cv2.Canny(blurred, 240, 250)
    images = np.hstack((gray, edges, edges_tight))

    cv2.imshow('Frame', images)
    while "q" != chr(cv2.waitKey() & 255):
        pass



if __name__ == '__main__':
    filename = sys.argv[1]
    img = cv2.imread(filename)
    split_panels(img)


