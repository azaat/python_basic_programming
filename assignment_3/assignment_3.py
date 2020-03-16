import numpy as np
import cv2

img1 = cv2.imread('in.png')

img2 = cv2.resize(img1,None,fx=0.5, fy=0.5)
img4 = cv2.resize(img1,None,fx=0.25, fy=0.25)

h, w, c = img1.shape
h2, w2, c2 = img2.shape
h4, w4, c4 = img4.shape
w_res = w + w // 2

result = np.zeros((h, w_res, c))
result[:h,:w] = img1

edges = cv2.Canny(img2,100,200)
edges1 = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
result[0:h2, w:w_res] = edges1

blur = cv2.blur(img4,(5,5))
gblur = cv2.GaussianBlur(img4, (5,5), 0)
result[h2:h2 + h4, w:w + w4] = blur
result[h2:h2 + h4, w + w4:w + w2] = gblur

kernel = np.random.randint(low=0, high=15, size=(5,5))
flt = cv2.filter2D(img4,3,kernel / 100)
rand = np.random.randint(0, 255, img4.shape)

result[h - h4:h, w:w + w4] = flt
result[h - h4:h, w + w4:w + w2] = rand

cv2.imwrite('out.png', result)