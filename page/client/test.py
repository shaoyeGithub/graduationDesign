from graduation.diagnosis import testclassify
from graduation.page.client import preprocess
from  PIL import Image
import numpy as np
import  cv2
import matplotlib.pyplot as plt
from skimage import measure,draw
image = Image.open("./Image/ca_result.jpg")
img = np.array(image)
imshow = Image.open("./Image/show.jpg")
imshow = np.array(imshow)
shapemax = -1
contours = measure.find_contours(img, 0.5)
plt.figure()

plt.figure(figsize=(3.5,2.2))
plt.axis('off')
plt.imshow(imshow, plt.cm.gray)
plt.margins(0,0)
for i in range(len(contours)):
    if (contours[i].shape)[0] > shapemax:
        shapemax = (contours[i].shape)[0]

for n, contour in enumerate(contours):
    if (contour.shape)[0] == shapemax:
        plt.plot(contour[:, 1], contour[:, 0], color="red", linewidth=1)
        plt.savefig("./image/result_contour.jpg")



