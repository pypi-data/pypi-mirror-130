import matplotlib.pyplot as plt
import math
import cv2 as cv 
import numpy as np
# Stop command is by ~
class TextStega:
    
    '''
    Methods
    -------
    Public:
        encode : encodes the text to the image
        decode : decodes the text from the image
    '''
    
    def decode(self, path):    
        """
        Input parameter 
        path(str) : Path of the image from which the encoded message is to be decoded

        Output
        text(str) : Decoded message from the image  

        Example
        msg = decode(path)

        Decode function decodes all the characters till it encounters ~(tilda) character.  
        """

        self.img = cv.imread(path)

        self.img = cv.cvtColor(self.img, cv.COLOR_BGR2RGB)
        self.img_str = np.reshape(self.img, (np.product(self.img.shape)))

        self.text = ""

        for i in range(int(len(self.img_str)/8)):
            self.bit = self.img_str[8*i:8*(i+1)]
            #print(bit.shape)
            #print(bit)
            self.bit = np.remainder(self.bit, 2)
            #print(bit.shape)
            #print(bit)
            self.bit = ''.join(map(str, self.bit))
            #print(bit)

            self.ascii_character = chr(int(self.bit, 2))
            #print(ascii_character)
            if self.ascii_character == '~' :
                break
            else:
                self.text = self.text + self.ascii_character
            i+=8
        return self.text


    def encode(self, path, text):
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

        self.img = cv.imread(path)

        self.limit = math.floor((self.img.shape[0]*self.img.shape[1]*self.img.shape[2]-8)/8)

        if len(text) <= (self.img.shape[0]*self.img.shape[1]*self.img.shape[2]-8)/8 :

            self.img = cv.cvtColor(self.img, cv.COLOR_BGR2RGB)
            self.img_str = np.reshape(self.img, (np.product(self.img.shape)))

            self.bit_str=""
            self.a = ' '.join(format(ord(x), 'b') for x in text)
            self.LL = list(self.a.split(' '))
            for i, bit in enumerate(self.LL):
                self.bit_str = self.bit_str + bit.zfill(8)

            self.bit_str = self.bit_str + "01111110"
            #print(bit_str)

            for i in range(len(self.bit_str)):
                #print(bit_str[i],img_str[i])

                if self.bit_str[i] == '0':
                    if self.img_str[i]%2 != 0:

                        self.img_str[i] = self.img_str[i] + 1
                    #print(bit_str[i],img_str[i])
                else:
                    if self.img_str[i]%2 == 0:

                        self.img_str[i] = self.img_str[i] + 1
                    #print(bit_str[i],img_str[i])

            self.final_image = np.reshape(self.img_str , self.img.shape)

            cv.imwrite("Encoded_image.png", cv.cvtColor(self.final_image, cv.COLOR_RGB2BGR))
            print(r"Encoded image is saved as 'Encoded_image.png'")
            return self.final_image

        else:
            print("Try again with higher resolution image!\nNo.of characters to encode exceed maximum capacity of the image\n")
            print("\nMaximum Characters allowed are : ",self.limit)
            
            return None



    