import cv2
import numpy as np

def display(image):
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

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
    
    if dim == 3:
        # go by x, y, then color
        for color in range(image.shape[2]):
            for x in range(image.shape[1]):
                for y in range(image.shape[0]):
                    pixel = image[y, x, color] & mask
                    rtn[y, x, color] = pixel + bits[b_i]
                    b_i += 1
                    if b_i >= len(bits):
                        return rtn
    else:
        for x in range(image.shape[1]):
            for y in range(image.shape[0]):
                pixel = image[y, x] & mask
                rtn[y, x] = pixel + bits[b_i]
                b_i += 1
                if b_i >= len(bits):
                    return rtn

def decrypt(image, msg_len):
    bits = bit_extract(image, msg_len)

    b_list = []

    for i in range(0, len(bits), 8):
        res = int(''.join(map(str, bits[i:i+8])), 2)
        b_list.append(res)

    return bytes(b_list)

def bit_extract(image, msg_len):
    dim = len(image.shape)

    bits = []
    mask = 0b00000001

    b_count = 0
    
    if dim == 3:
        # go by x, y, then color
        for color in range(image.shape[2]):
            for x in range(image.shape[1]):
                for y in range(image.shape[0]):
                    bits.append(image[y, x, color] & mask)
                    b_count += 1
                    if b_count >= msg_len*8:
                        return bits
    # grayscale
    else:
        for x in range(image.shape[1]):
            for y in range(image.shape[0]):
                bits.append(image[y, x])
                b_count += 1
                if b_count >= msg_len*8:
                    return bits

def user_file_hide(image):
        while True:
            test_msg = input('Hello! Please enter file path you would like to store in the image.\n')

            filetype = test_msg.split(".")[-1]
            f = open(test_msg, "rb")
            file = f.read()
            try:
                return hide(image, file)
            except ValueError:
                print("\nSorry, please use a bigger image or store a smaller message.\n\n")
                continue
        
def user_file_decrypt(secret, file):
    b_msg = decrypt(secret, len(file))
    # msg = read_bytes(b_msg)
    
    # https://www.geeksforgeeks.org/create-a-new-text-file-in-python/
    file_path = "./parsed{}".format(filetype)
    
    # format_msg = '{}\n'.format(msg)
    
    with open(file_path, 'wb') as file:
        file.write(b_msg)

def user_both(image):
    while True:
        test_msg = input('Please enter file path you would like to store in the image.\n')

        filetype = test_msg.split(".")[-1]
        f = open(test_msg, "rb")
        file = f.read()

        try:
            secret = hide(image, file)

            display(image)
            display(secret)
        
            b_msg = bytes(decrypt(secret, len(file)))
            # msg = read_bytes(b_msg)
            
            # https://www.geeksforgeeks.org/create-a-new-text-file-in-python/
            file_path = "./parsed{}".format(filetype)

            # format_msg = '{}\n'.format(msg)
            
            with open(file_path, 'wb') as file:
                file.write(b_msg)
                
            # print('\n{}'.format(msg))
            break
        except ValueError:
            print("\nSorry, please use a bigger image or store a smaller message.\n\n")
            continue
        
def main():
    # code pictures here
    # image = cv2.imread('img.png', cv2.IMREAD_GRAYSCALE)

    while True:
        opt = input('''Welcome! Please select what you want to do:
        (1) Hide file in image
        (2) Fetch file from image
        (3) Hide and fetch file
        (4) Quit
        ''')

        image = None
        secret = None
        
        match opt:
            case '1':
                i_path = input("Please specify the source image's path: ")
                image = cv2.imread(i_path)
                
                secret = user_file_hide(image)
                print('File hidden in image. New image saved in current directory!')
                name = input('Please enter the file name: ')
                name = '{}.png'.format(name)
                cv2.imwrite(name, secret)
            case '2':
                secret = input('Please enter the file path to the image to fetch from: ')
                user_file_decrypt(secret)
                print('File saved to current directory!')
            case '3':
                user_both(image)
                y = input('Would you like to compare ? (y/n)\n')
        
                if y == 'y':
                    display(image)
                    display(secret)
            case '4':
                return
            case _:
                continue
        
if __name__ == "__main__":
    main()
