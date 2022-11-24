from PIL import Image,ImageDraw
import pytesseract
from googletrans import Translator
import re
import cv2

import numpy as np





filename = "test.png"

img = cv2.imread(filename)




pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
result = pytesseract.image_to_boxes(img,lang="chi_tra",config="--oem 3 --psm 4")


h, w,_ = img.shape



























result = result.split('\n')
temp = []
for x in result:
    
    if len(x) > 0:
        if x[0].isnumeric():
            temp.append(x)
        n = re.findall(r'[\u4e00-\u9fff]+', x)
        if len(n) == 0:
            temp.append(x)
    else:
        temp.append(x)

result = [x for x in result if x not in temp]
print(result)
for b in result:
    b = b.split(' ')
    img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

# show annotated image and wait for keypress
cv2.imshow(filename, img)
cv2.waitKey(0)






wImg,hImg = img.size    
x1, y1 =hImg - 513, hImg-494
x2,y2 = 311,330
chineseCharacters = [x for x in result if x not in temp] # character/
print(chineseCharacters)

trans = Translator()
#printed = trans.translate(result, dest ="english")

	
img1 = ImageDraw.Draw(img)
img1.rectangle((x1,y1,x2,y2),fill=(255,0,0))
img.show()