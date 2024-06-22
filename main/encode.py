import cv2
import numpy as np

def display(image):
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def encrypt_message(message):
    return

def read_bytes(b_msg):
    rtn = ''
    for byte in b_msg:
        rtn += chr(byte)

    return rtn

def hide(image, b_message):
    dim = len(image.shape)

    store_space = image.shape[0]
    for i in range(1, dim):
        store_space *= image.shape[i]

    if store_space < len(b_message) * 8:
        raise ValueError("Image must have enough pixels to store message")

    bits = []

    for byte in b_message:
        # https://blog.finxter.com/5-best-ways-to-convert-python-bytes-to-bits/
        temp = list(map(int, bin(byte)[2:].zfill(8)))
        bits += temp
                
    return bit_insert(image, bits, dim)

def bit_insert(image, bits, dim):
    mask = 0b11111110
    b_i = 0

    rtn = np.copy(image)
    
    # Note: our implementation here will impact how we get our message out of the image
    if dim == 3:
        # go by x, y, then color
        for color in range(image.shape[2]):
            for x in range(image.shape[0]):
                for y in range(image.shape[1]):
                    pixel = image[y, x, color] & mask
                    rtn[y, x, color] = pixel + bits[b_i]
                    b_i += 1
                    if b_i >= len(bits):
                        return rtn
    else:
        for x in range(image.shape[0]):
            for y in range(image.shape[1]):
                pixel = image[y, x] & mask
                rtn[y, x] = pixel + bits[b_i]
                b_i += 1
                if b_i >= len(bits):
                    return rtn

def decrypt(image):
    dim = len(image.shape)

    bits = []
    mask = 0b00000001
    
    if dim == 3:
        # go by x, y, then color
        for color in range(image.shape[2]):
            for x in range(image.shape[0]):
                for y in range(image.shape[1]):
                    bits.append(image[y, x, color] & mask)
    else:
        for x in range(image.shape[0]):
            for y in range(image.shape[1]):
                bits.append(image[y, x, color])

    b_list = []
                
    for i in range(0, len(bits), 8):
        # TODO: dont take bytes past message length
        res = int(''.join(map(str, bits[i:i+8])), 2)
        b_list.append(res)
        
    return b_list
    
def main():
    # code pictures here
    # image = cv2.imread('img.png', cv2.IMREAD_GRAYSCALE)
    image = cv2.imread('img.png')
    display(image)

    test_mess = b'hello'
    
    secret = hide(image, test_mess)

    display(secret)

    b_msg = decrypt(secret)

    print(read_bytes(b_msg))
    
if __name__ == "__main__":
    main()
