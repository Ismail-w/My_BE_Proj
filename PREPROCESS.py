


import cv2
import numpy as np

img = cv2.imread('Y16.jpg')

print("Image Properties")
print("- Number of Pixels: " + str(img.size))
print("- Shape/Dimensions: " + str(img.shape))
cv2.imshow('org',img)
cv2.waitKey(0)

blue, green, red = cv2.split(img) # Split the image into its channels
resized_image = cv2.resize(img, (200, 200))
print("Image Properties")
print("- Number of Pixels: " + str(resized_image.size))
print("- Shape/Dimensions: " + str(resized_image.shape))
cv2.imshow('res',resized_image) # Display the grayscale version of image
cv2.waitKey(0)

img_gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
cv2.imshow('grayscale',img_gray) # Display the grayscale version of image
cv2.waitKey(0)

r, threshold = cv2.threshold(img_gray, 125, 255, cv2.THRESH_BINARY)
cv2.imshow('threshold',threshold)
cv2.waitKey(0)


edged = cv2.Canny(img_gray, 100,200)
cv2.imshow('Edge',edged)
cv2.waitKey(0)

contours, hierarchy = cv2.findContours(edged,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  
print("Number of Contours found = " + str(len(contours)))

cv2.drawContours(resized_image, contours, -1, (0, 255, 0), 3)  
cv2.imshow('Contours', resized_image) 
cv2.waitKey(0) 
