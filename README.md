# BÀI TẬP LỚN: XÁC ĐỊNH VẬT THỂ QUA MÁY ẢNH BẰNG MÔ HÌNH AI YOLO

## Giới thiệu dự án
Dự án này ứng dụng mô hình YOLOv11 để giải quyết bài toán phát hiện đối tượng (Object Detection) theo thời gian thực. Mục tiêu của dự án là triển khai một mô hình cân bằng tối ưu giữa tốc độ (latency) và độ chính xác (mAP), khắc phục những hạn chế của các mô hình tiền nhiệm và có khả năng chạy tốt trên các thiết bị tài nguyên hạn chế.

## Nhóm nghiên cứu
- **Đơn vị:** Trường Đại học Thăng Long
- **Giảng viên hướng dẫn:** ThS. Ngô Mạnh Cường

**Thành viên:**
- A49651 Huỳnh Hải Nam
- A49971 Lê Nguyễn Nhật Huy
- A50059 Đõ Quốc Hoàn

## 2. Kiến trúc và Công nghệ cốt lõi
Dự án sử dụng YOLOv11 với những cải tiến mang tính cách mạng về kiến trúc:
* **Backbone C3k2:** Thay thế khối C2f bằng C3k2 giúp giảm 22% số lượng tham số và khối lượng tính toán, tối ưu tốc độ suy luận trên CPU mà vẫn mở rộng được vùng tiếp nhận.
* **Cơ chế Attention C2PSA:** Tích hợp mô-đun C2PSA (Cross-Stage Partial with Spatial Attention) giúp mạng tập trung vào các đặc trưng quan trọng, cải thiện rõ rệt khả năng phát hiện các đối tượng nhỏ hoặc bị che khuất[cite: 1].
* **Decoupled Head & Anchor-free:** Dự đoán trực tiếp khoảng cách từ tâm đối tượng đến các cạnh hộp giới hạn, tách biệt nhánh phân loại và nhánh hồi quy giúp hội tụ nhanh và chính xác hơn[cite: 1].
* **Hàm mất mát và Gán nhãn động:** Sử dụng Task Alignment Learning (TAL) kết hợp VFL, DFL và CIoU Loss để định hình phân phối xác suất và tăng độ chính xác định vị[cite: 1].

## 3. Quá trình Huấn luyện (Training)
* **Dữ liệu (Dataset):** Sử dụng tập dữ liệu tùy chỉnh gồm hơn 50 hình ảnh chụp sẵn đã được gắn nhãn toàn bộ vật thể[cite: 1].
* **Cấu hình huấn luyện:** 
  * Mô hình khởi tạo: `yolo11s.pt` (Pretrained weights từ framework Ultralytics)[cite: 1].
  * Số chu kỳ (Epochs): 60[cite: 1].
  * Kích thước ảnh đầu vào (Image size): 640x640[cite: 1].
* **Kỹ thuật áp dụng:** Sử dụng các kỹ thuật tăng cường dữ liệu như Mosaic và Mixup để làm phong phú dữ liệu, giúp mô hình tổng quát hóa tốt hơn[cite: 1].
* **Kết quả đầu ra:** Tệp trọng số tối ưu nhất được lưu trữ tại `my_model.pt`[cite: 1].

## 4. Kết quả Thực nghiệm
* **Độ chính xác (mAP):** YOLOv11 đạt chỉ số mAP vượt trội (ví dụ bản YOLOv11n đạt 39.5 mAP trên tập COCO, cao hơn YOLOv8n)[cite: 1].
* **Chỉ số mAP@50-95 cao:** Chứng tỏ mô hình không chỉ phát hiện đúng lớp vật thể mà còn định vị hộp bao cực kỳ khít và chính xác với đối tượng thực tế[cite: 1].
* **Hoạt động suy luận (Inference):** Ứng dụng thành công vào bài toán nhận diện thời gian thực qua webcam, tận dụng tối đa khả năng tối ưu hóa của thư viện Ultralytics để trả về tọa độ và xác suất lớp nhanh chóng[cite: 1].

## 5. Hướng dẫn chạy mô hình thời gian thực (Inference)
Dưới đây là đoạn mã nguồn cơ bản để khởi chạy mô hình nhận diện qua camera[cite: 1]:

```python
from ultralytics import YOLO
import cv2

# Tải mô hình đã huấn luyện
model = YOLO("my_model.pt")

# Mở camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Khong the mo camera.")
    exit()

# Vòng lặp nhận diện thời gian thực
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Dự đoán
    results = model(frame)
    annotated_frame = results[0].plot()
    
    # Hiển thị
    cv2.imshow("YOLOv11 Object Detection", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

## Trích dẫn
Nếu bạn sử dụng repository này, vui lòng trích dẫn:

```bibtex
@misc{btlyolo,
  title        = {BTL: xác định vật thể bằng mô hình YOLO},
  author       = {Huynh Hai Nam and Le Nguyen Nhat Huy and Do Quoc Hoan},
  year         = {2026},
  howpublished = {GitHub repository},
  url          = {https://github.com/duy1sme/NCKH-3D-Face-Recognition}
}
```

## Tài liệu tham khảo
- YOLOv11: Revolutionizing Real-Time Object Detection - Viso Suite.
- YOLO11: Redefining Real-Time Object Detection - Tutorial - Learn OpenCV.
- YOLOv11 Architecture: Advanced Object Detection - Emergent Mind.
- YOLOv11: An Overview of the Key Architectural Enhancements - arXiv.
- YOLOv11 Is Officially Out! What You Need To Know! | by Zain Shariff - Medium.
- All you need to know about Ultralytics YOLO11 and its applications.
- YOLO11 vs YOLOv8: Architectural Evolution and Performance Analysis - Ultralytics YOLO Docs.
- YOLOv8 vs YOLO11: Evolution of Real-Time Object Detection - Ultralytics YOLO Docs.
- YOLOv9 vs YOLO11: Architectural Evolution and Performance Analysis - Ultralytics YOLO Docs.
- YOLO11 vs YOLOv9: A Comprehensive Technical Comparison - Ultralytics YOLO Docs.
- YOLOv8 vs YOLOv10: A Comprehensive Technical Comparison - Ultralytics YOLO Docs.  
