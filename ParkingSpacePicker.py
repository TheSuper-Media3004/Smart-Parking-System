import cv2
import pickle

width, height = 107, 48
try:
    with open('sample', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)
    with open('sample', 'wb') as f:
        pickle.dump(posList, f)
img = cv2.imread('1.jpg')
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", mouseClick)

while True:
    imgCopy = img.copy()
    for pos in posList:
        cv2.rectangle(imgCopy, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
