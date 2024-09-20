from billtotxt import billtotxt
from totalAmount import totalAmount

extractedText = billtotxt('.\demoPhotos\invoice3.jpg')

print(extractedText)

amount = totalAmount(extractedText)

print(amount)

