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

image = TextStega.encode(path, encode_text)

# path(str) : "path of the image" 
# encode_text(str) : "Text to be encoded in the image"

```

Example to decode the text from the image

```python

from TextStega import TextStega

decoded_text = TextStega.decode(path) 

# path(str) : path of the image which was previously encoded with the message.

```


## FAQs
***
A list of frequenctly asked questions
1. **What is text steganography?**
Steganography is the technique of hiding secret data within an ordinary, non-secret, file or message in order to avoid detection. More information can be found on this [Wikipedia](https://en.wikipedia.org/wiki/Steganography) page.

2. **Where can I use this package?**
This tool is used to craftfully hide the data in images. So this package can be used to hide secret text messages by encoding them in images to maintain the secrecy.

3. **How does this algorithm works?**





