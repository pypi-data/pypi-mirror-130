# Text Steganography
***

## Table of Contents
1. [General Info](#general-info)
2. [Technologies](#technologies)
3. [Example](#example)
4. [FAQs](#faqs)

## General Info
***
This project deals with hiding text message inside a image. 
Also called as Text Steganography. It is extremely useful technique
for conceling text messages. In this project there are two function namely:
* 'encode' which encode the entered text to an also image entered by a user. 
* 'decode' which decodes the text from the image which 
is previously encoded by the encode function. 

## Technologies
***
A list of libraries used within the project:
* [matplotlib](https://matplotlib.org): Version 3.3.4
* [math](https://docs.python.org/3/library/math.html)
* [openCV](https://opencv.org): Version 4.2.0
* [numpy](https://numpy.org): Version 1.21.4


## Example
***
Example to encode the text message to image
```python

from TextStega import TextStega

image = TextStega().encode(path, encode_text)

# path(str) : "path of the image" 
# encode_text(str) : "Text to be encoded in the image"

```

Example to decode the text from the image

```python

from TextStega import TextStega

decoded_text = TextStega().decode(path) 

# path(str) : path of the image which was previously encoded with the message.

```


## FAQs
***
A list of frequenctly asked questions
1. **What is text steganography?**<br>
Steganography is the technique of hiding secret data within an ordinary, non-secret, file or message in order to avoid detection. More information can be found on this [Wikipedia](https://en.wikipedia.org/wiki/Steganography) page.

2. **Where can I use this package?**<br>
This tool is used to craftfully hide the data in images. So this package can be used to hide secret text messages by encoding them in images to maintain the secrecy.

3. **How does this algorithm works?**<br>
Let us consider a 3 * 3 RBG image for understanding the algorithm. The image consists of 3 channel and heigh and weidth equal to 3. Thus 3 * 3 * 3 = 27 values, with each value ranging from 0-255(pixel value). For instance consider. We are interested in storing the character 'H' in this image. In the encode function the H is converted into binary value which is '01001000'. Each ASCII character can be represented by 8-bit binary number which is saved in the image.<br>
Consider 3 pixel values p1, p2 and p3 as (10,200,35), (26,65,98), (100,139,35) respectively.<br>
If the bit-value to be saved is 0 the pixel value is changed to even and if 1 its converted to odd. Thus in our example, the pixel value P1, P2 and P3 changes to (10,201,36), (26,65,98), (100,140,36). If the pixel value is odd but the value to be stored is 0, then the pixel value is increased by one. Same is the case with storing 1. In this way the txt message is stored in the form of 0s and 1s string in the image.<br>
In the decode function, the pixel values are erad one by one, and then if its odd it is taken as 1 else 0. This is done till the algorithm encounter STOP character. Once is encounters the STOP character, it terminates the program and returns the decoded text message.<br> 
This STOP values is ~(tilda) in our case. So if your message consists of ~ character then the decoder will only read till that value. This is only drawback of this code. 

4. **How many characters can I save in a image?**<br>
Considering you have a RGB image with 1024 * 1024 resolution, you can encode upto (1024 * 1024 * 3 - 8) / 8 = 393215 characters. The 8 subtracted represents the bits reuiqred for STOP character.  





   





