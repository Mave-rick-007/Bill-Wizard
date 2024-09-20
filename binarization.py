import cv2

_, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Save the binary image
cv2.imwrite('binary_image.png', binary_image)
