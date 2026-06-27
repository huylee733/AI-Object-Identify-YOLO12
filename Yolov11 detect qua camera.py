from ultralytics import YOLO
import cv2
model = YOLO("C:\\Users\\Admin\\Downloads\\AI\\AI\\model2.pt")
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Khong the mo camera.")
    exit()
while True:
    ret, frame = cap.read()
    if not ret:
        break
    results = model(frame)  
    annotated_frame = results[0].plot()
    cv2.imshow("YOLO Detection", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()