import cv2
import numpy as np


frame = cv2.imread("C:\\Users\\Hemhalatha V R\\drone\\images\\test_pic.jpg")

blur = cv2.GaussianBlur(frame, (5, 5), 0)
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(blur, 50, 150)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    
    area = cv2.contourArea(cnt)
    if area< 500:
        continue

    peri = cv2.arcLength(cnt, True)
    #circularity = 4 * np.pi * (area / (peri * peri))  
    approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
    (x, y), radius = cv2.minEnclosingCircle(cnt)
    circle_area = np.pi * (radius ** 2)

    circularity = area / circle_area
    

    x, y, w, h = cv2.boundingRect(approx)

    sides = len(approx)
    shape = "Unidentified"
    if circularity> 0.90:
        shape = "circle"
    elif sides == 3:
        shape = "Triangle"
    elif sides == 4:
        aspect_ratio = float(w) / h
        shape = "Square" if 0.95 <= aspect_ratio <= 1.05 else "Rectangle"
    elif sides == 5:
        shape = "Pentagon"
    else:
        shape= "polygon"

    
    cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)
    cv2.putText(frame, shape, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

cv2.imwrite("img3.jpg",frame)
cv2.destroyAllWindows()
