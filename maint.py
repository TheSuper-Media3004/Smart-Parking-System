import cv2
import pickle
import cvzone
import numpy as np

# -----------------------------
# Config
# -----------------------------
video_path = 'carPark.mp4'
width, height = 103, 43
slot_file = 'CarParkPos1'  # Pickle file for slot positions

# -----------------------------
# Load slot dictionary (slot_name -> (x, y))
# -----------------------------
try:
    with open(slot_file, 'rb') as f:
        slotDict = pickle.load(f)  # e.g., {'Slot 1': (x, y), ...}
        slotDict = {f"Slot {i+1}": pos for i, pos in enumerate(old_list)}
except:
    slotDict = {}  # empty dictionary

# -----------------------------
# Trackbars for tuning
# -----------------------------
def empty(a):
    pass

cv2.namedWindow("Vals")
cv2.resizeWindow("Vals", 640, 240)
cv2.createTrackbar("Val1", "Vals", 25, 50, empty)
cv2.createTrackbar("Val2", "Vals", 16, 50, empty)
cv2.createTrackbar("Val3", "Vals", 5, 50, empty)

# -----------------------------
# Mouse click function
# -----------------------------
def mouseClick(event, x, y, flags, params):
    global slotDict
    if event == cv2.EVENT_LBUTTONDOWN:
        # Add slot with auto name
        slot_name = f"Slot {len(slotDict)+1}"
        slotDict[slot_name] = (x, y)
        print(f"Added {slot_name} at {(x, y)}")
    if event == cv2.EVENT_RBUTTONDOWN:
        # Remove slot if clicked inside
        for name, pos in list(slotDict.items()):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                slotDict.pop(name)
                print(f"Removed {name}")
    # Save slots
    with open(slot_file, 'wb') as f:
        pickle.dump(slotDict, f)

# -----------------------------
# Video capture
# -----------------------------
cap = cv2.VideoCapture(video_path)
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", mouseClick)

# -----------------------------
# Function to check parking spaces
# -----------------------------
def checkSpaces(img, imgThres):
    free_slots = 0
    for slot_name, pos in slotDict.items():
        x, y = pos
        x_end = min(x + width, imgThres.shape[1])
        y_end = min(y + height, imgThres.shape[0])

        imgCrop = imgThres[y:y_end, x:x_end]
        count = cv2.countNonZero(imgCrop)

        if count < 900:
            color = (0, 200, 0)
            thickness = 5
            free_slots += 1
        else:
            color = (0, 0, 200)
            thickness = 2

        # Draw rectangle and name
        cv2.rectangle(img, pos, (x + width, y + height), color, thickness)
        cvzone.putTextRect(img, f"{slot_name}: {count}", (x, y + height - 6),
                           scale=1, thickness=2, offset=0, colorR=color)
    # Display total free
    cvzone.putTextRect(img, f'Free: {free_slots}/{len(slotDict)}', (50, 50),
                       scale=3, thickness=5, offset=20, colorR=(0, 200, 0))
    return free_slots

# -----------------------------
# Main loop
# -----------------------------
while True:
    success, img = cap.read()
    if not success:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # Preprocess frame
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)

    val1 = cv2.getTrackbarPos("Val1", "Vals")
    val2 = cv2.getTrackbarPos("Val2", "Vals")
    val3 = cv2.getTrackbarPos("Val3", "Vals")
    if val1 % 2 == 0: val1 += 1
    if val3 % 2 == 0: val3 += 1

    imgThres = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, val1, val2)
    imgThres = cv2.medianBlur(imgThres, val3)
    kernel = np.ones((3, 3), np.uint8)
    imgThres = cv2.dilate(imgThres, kernel, iterations=1)

    # Check slots
    checkSpaces(img, imgThres)

    # Show frame
    cv2.imshow("Image", img)

    key = cv2.waitKey(1)
    if key == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
