from ultralytics import YOLO
import cv2
model = YOLO("C:\\Users\\Admin\\Downloads\\AI\\AI\\model2.pt")
image_list = [
    "C:\\Users\\Admin\\Downloads\\AI\\AI\\616472268_1599514237868593_5815527645498762054_n.jpg"
]
results = model(image_list, save=True, conf=0.5)
for i, result in enumerate(results):
    print(f"\nKết quả cho ảnh thứ {i+1}:")
    
    # Lấy các hộp giới hạn (Bounding boxes)
    boxes = result.boxes
    
    for box in boxes:
        # Lấy tọa độ, độ tin cậy và class
        coords = box.xyxy[0].tolist() # [x1, y1, x2, y2]
        confidence = box.conf[0].item()
        class_id = int(box.cls[0].item())
        class_name = model.names[class_id]
        
        print(f"- Phát hiện: {class_name} ({confidence:.2f}) tại {coords}")