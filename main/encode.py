import cv2
import numpy as np

def display(image):
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def encrypt_message(message):
    return
    
def hide(image, enc_message):
    return
    
def decrypt(mes_img, key_img):
    return
    
def main():
    # code pictures here
    image = cv2.imread('img.jpg', cv2.IMREAD_GRAYSCALE)

if __name__ == "__main__":
    main()
