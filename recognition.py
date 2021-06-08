import pytesseract
import cv2


def recognize(path):
    img = cv2.imread(path)
    predicted_result = pytesseract.image_to_string(
        img,
        lang='eng',
        config='--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABEKMHOPCTYX'
    )
    return predicted_result
