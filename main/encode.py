import cv2
import numpy as np

def display(image):
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def encrypt_message(message):
    return

def convert_to_bytes(message):
    return
    
def hide(image, b_message):
    dim = len(image.shape)

    store_space = 0
    for i in range(dim):
        store_space *= image.shape[i]

    b_len = len(b_message)
    b_i = 0
        
    if store_space < len(b_message):
        raise ValueError("Image must have enough pixels to store message")

    # Note: our implementation here will impact how we get our message out of the image
    # TODO: try numpy slicing tricks to speed up implementation
    if dim == 3:
        # go by x, y, then color
        for i in range(image.shape[2]):
            for j in range(image.shape[0]):
                for k in range(image.shape[1]):
                    byte = b_message[b_i]
                    
    else:
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
        
                
    return rtn
    
def decrypt(mes_img, key_img):
    return
    
def main():
    # code pictures here
    image = cv2.imread('img.jpg', cv2.IMREAD_GRAYSCALE)

    test_mess = b'hello'
    
    secret = hide(image, test_mess)
    
if __name__ == "__main__":
    main()
