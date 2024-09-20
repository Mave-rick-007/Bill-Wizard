import cv2

# Read the image
image = cv2.imread('D:\\billDetection\\captured_images\\book_3.png')

# Convert to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Save or process further
cv2.imwrite('grayscale_image.png', gray_image)


# Apply Otsu's thresholding
_, binary_image = cv2.threshold(gray_image, 0, 255,  cv2.THRESH_OTSU)

# Save the binary image
cv2.imwrite('binary_image.png', binary_image)
