# Text Steganography
***

## Table of Contents
1. [General Info](#general-info)
2. [Technologies](#technologies)
3. [FAQs](#faqs)

## General Info
***
This project deals with hiding text message inside a image. 
Also called as Text Steganography. It is extremely useful technique
for conceling text messages. In this project there are two function namely:
* 'encode' which encode the entered text to an also image entered 
by a user. 
*'decode' which decodes the text from the image which 
is previously encoded by the encode function. 

## Technologies
***
A list of libraries used within the project:
* matplotlib(https://matplotlib.org): Version 3.3.4
* math(https://docs.python.org/3/library/math.html): Version 
* openCV(https://opencv.org): Version 4.2.0
* numpy(https://numpy.org): Version 1.21.4

## FAQs
***
A list of frequenctly asked questions
1. **What is text steganography?**
Steganography is the technique of hiding secret data within an ordinary, non-secret, file or message in order to avoid detection. More information can be found on this [Wikipedia](https://en.wikipedia.org/wiki/Steganography) page.

2. **Where can I use this package?**
This tool is used to craftfully hide the data in images. So this package can be used to hide secret text messages by encoding them in images.

3. **How to encode the image with desired secret message?**
It is a user-friendly package to use. The user just needs to call the encode function and pass the image and the message to encode. The function will create a new image with encoded message and save it in the Working directory under the name of 'Encoded_image.png'. Voila you have the encoded image!! 





