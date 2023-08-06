import matplotlib.pyplot as plt
import math
import cv2 as cv 
import numpy as np
# Stop command is by ~

def decode(path):    
    '''
    Input parameter 
    path(str) : Path of the image from which the encoded message is to be decoded

    Output
    text(str) : Decoded message from the image  

    Example
    msg = decode(path)

    Decode function decodes all the characters till it encounters ~(tilda) character.  
    '''

    img = cv.imread(path)

    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    img_str = np.reshape(img, (np.product(img.shape)))

    text = ""

    for i in range(int(len(img_str)/8)):
        bit = img_str[8*i:8*(i+1)]
        #print(bit.shape)
        #print(bit)
        bit = np.remainder(bit, 2)
        #print(bit.shape)
        #print(bit)
        bit = ''.join(map(str, bit))
        #print(bit)

        ascii_character = chr(int(bit, 2))
        #print(ascii_character)
        if ascii_character == '~' :
            break
        else:
            text = text + ascii_character
        i+=8
    return text


def encode(path, text):
    '''
    Input parameter: 
    path(str) : Path of the image to which the message is to be encoded
    text(str) : Message to be encoded

    Output:
    final_image(numpy array) :  New image on which the message is encoded

    Example:
    img = encode(path, text)

    Stop character is ~(tilda). Encode function automatically adds this character at the end of the user input string. No need to specifically add this character. 

    '''

    img = cv.imread(path)

    limit = math.floor((img.shape[0]*img.shape[1]*img.shape[2]-8)/8)

    if len(text) <= (img.shape[0]*img.shape[1]*img.shape[2]-8)/8 :

        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        img_str = np.reshape(img, (np.product(img.shape)))

        bit_str=""
        a = ' '.join(format(ord(x), 'b') for x in text)
        LL = list(a.split(' '))
        for i, bit in enumerate(LL):
            bit_str = bit_str + bit.zfill(8)

        bit_str = bit_str + "01111110"
        #print(bit_str)

        for i in range(len(bit_str)):
            #print(bit_str[i],img_str[i])

            if bit_str[i] == '0':
                if img_str[i]%2 != 0:

                    img_str[i] = img_str[i] + 1
                #print(bit_str[i],img_str[i])
            else:
                if img_str[i]%2 == 0:

                    img_str[i] = img_str[i] + 1
                #print(bit_str[i],img_str[i])

        final_image = np.reshape(img_str , img.shape)

        cv.imwrite("Encoded_image.png", cv.cvtColor(final_image, cv.COLOR_RGB2BGR))
        print(r"Encoded image is saved as 'Encoded_image.png'")
        return final_image

    else:
        print("Try again with higher resolution image!\nNo.of characters to encode exceed maximum capacity of the image\n")
        print("\nMaximum Characters allowed are : ",limit)



    