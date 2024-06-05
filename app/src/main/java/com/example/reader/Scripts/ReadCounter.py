from PIL import Image
import sys
import pytesseract
import math
import time
sys.path.append(r'C:\Users\tudor\AndroidStudioProjects\Reader\app\libs\Tesseract-OCR')
import cv2
import sys
if __name__ == '__main__':
    # Press the green button in the gutter to run the script.

    #look around and create the base line for new threshhold
    startTime = time.time()
    #img1 = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
    img1 = sys.argv[1].convert('L')
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(img1)
    x, y = max_loc
    w, h = 600, 600
    x = max(0, x - w / 2)
    y = max(0, y - h / 2)
    w = min(w, img1.shape[1] - x)
    h = min(h, img1.shape[0] - y)
    x = math.floor(x)
    y = math.floor(y)
    h = math.floor(h)
    w = math.floor(w)
    crop = img1[y:y + h, x:x + w]
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(crop)
    # _, thresh1 = cv2.threshold(crop, 150, 220, cv2.THRESH_BINARY_INV)
    # cv2.imshow('thresh', thresh1)
    # cv2.waitKey(0)
    _, thresh1 = cv2.threshold(crop, max_val-30, max_val, cv2.THRESH_TOZERO)  # nice
    _,thresh1 = cv2.threshold(thresh1 , max_val-30 , max_val, cv2.THRESH_BINARY_INV)
    # Creating a structuring element for each of the numbers in our counter
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 3))

    erode = cv2.erode(thresh1, kernel, iterations=3)

    dilate = cv2.dilate(erode, kernel, iterations=1)


    cleaned = cv2.morphologyEx(dilate, cv2.MORPH_TOPHAT, kernel, iterations=3)

    cv2.imshow(cleaned)
    cv2.waitKey(0)
    pytesseract.pytesseract.tesseract_cmd = r'Reader\app\libs\Tesseract-OCR\tesseract'
    text1 = pytesseract.image_to_string(cleaned, lang='lets', config='--psm 6 -c tessedit_char_whitelist="0123456789"')
    text1 = text1[:8]

    print(text1)
    