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
* **Cơ chế Attention C2PSA:** Tích hợp mô-đun C2PSA (Cross-Stage Partial with Spatial Attention) giúp mạng tập trung vào các đặc trưng quan trọng, cải thiện rõ rệt khả năng phát hiện các đối tượng nhỏ hoặc bị che khuất.
* **Decoupled Head & Anchor-free:** Dự đoán trực tiếp khoảng cách từ tâm đối tượng đến các cạnh hộp giới hạn, tách biệt nhánh phân loại và nhánh hồi quy giúp hội tụ nhanh và chính xác hơn.
* **Hàm mất mát và Gán nhãn động:** Sử dụng Task Alignment Learning (TAL) kết hợp VFL, DFL và CIoU Loss để định hình phân phối xác suất và tăng độ chính xác định vị.

## 3. Quá trình Huấn luyện (Training)
* **Dữ liệu (Dataset):** Sử dụng tập dữ liệu tùy chỉnh gồm hơn 50 hình ảnh chụp sẵn đã được gắn nhãn toàn bộ vật thể.
* **Cấu hình huấn luyện:** 
  * Mô hình khởi tạo: `yolo11s.pt` (Pretrained weights từ framework Ultralytics).
  * Số chu kỳ (Epochs): 60.
  * Kích thước ảnh đầu vào (Image size): 640x640.
* **Kỹ thuật áp dụng:** Sử dụng các kỹ thuật tăng cường dữ liệu như Mosaic và Mixup để làm phong phú dữ liệu, giúp mô hình tổng quát hóa tốt hơn.
* **Kết quả đầu ra:** Tệp trọng số tối ưu nhất được lưu trữ tại `my_model.pt`.

## 4. Kết quả thực nghiệm

Sau 60 chu kỳ huấn luyện (epochs), mô hình thu được (`my_model.pt`) đạt các chỉ số đánh giá hiệu suất trực quan cực kỳ tối ưu trên tập dữ liệu kiểm thử. Các chỉ số được thống kê chi tiết trong bảng dưới đây:

| Chỉ số hiệu suất | Giá trị đạt được | Ý nghĩa trong bài toán thực tế |
| :--- | :---: | :--- |
| **mAP@50** | **82.9%** | Độ chính xác tổng thể trong việc nhận diện đúng loại vật thể và định vị vùng chứa (IoU > 50%). |
| **Precision** (Độ chính xác) | **78.7%** | Tỷ lệ dự đoán đúng trên tổng số đối tượng được phát hiện (Hạn chế tối đa báo động giả/nhầm nền). |
| **Recall** (Độ nhạy) | **83.3%** | Khả năng quét và tìm thấy đối tượng, tránh bỏ sót các vật thể thực tế xuất hiện trong khung hình. |
| **mAP@50-95** | **59.8%** | Điểm số đánh giá độ khít và chuẩn xác nghiêm ngặt của hộp bao quanh vật thể khi tịnh tiến IoU từ 50% đến 95%. |
| **Inference Speed** (Tốc độ) | **~7.5 ms / ảnh** | Tốc độ xử lý siêu nhanh, tương đương **>130 FPS**, đáp ứng hoàn hảo yêu cầu thời gian thực không độ trễ. |


### Đánh giá chung:
Mô hình đạt độ nhạy (**Recall: 83.3%**) cao hơn so với **Precision**, giúp hệ thống hoạt động ổn định trong điều kiện thực tế, ưu tiên việc phát hiện tối đa vật thể để không bỏ sót mục tiêu. Tốc độ suy luận **7.5 ms** chứng minh cấu trúc cải tiến của YOLOv11 tối ưu phần cứng cực tốt.

## Bảng So Sánh Hiệu Suất Các Phiên Bản YOLO11

Dưới đây là bảng thống kê hiệu năng chuẩn, so sánh các biến thể của mạng YOLO11 được đánh giá mức độ hội tụ (kích thước ảnh đầu vào định tuyến ở 640x640):

| Mô hình | Kích thước ảnh | mAP<sup>val</sup> 50-95 | Tốc độ CPU ONNX (ms) | Tốc độ T4 TensorRT10 (ms) | Tham số (M) | FLOPs (B) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **YOLO11n** | 640 | 39.5 | 56.1 ± 0.8 | 1.5 ± 0.0 | 2.6 | 6.5 |
| **YOLO11s** | 640 | 47.0 | 90.0 ± 1.2 | 2.5 ± 0.0 | 9.4 | 21.5 |
| **YOLO11m** | 640 | 51.5 | 183.2 ± 2.0 | 4.7 ± 0.1 | 20.1 | 68.0 |
| **YOLO11l** | 640 | 53.4 | 238.6 ± 1.4 | 6.2 ± 0.1 | 25.3 | 86.9 |
| **YOLO11x** | 640 | 54.7 | 462.8 ± 6.7 | 11.3 ± 0.2 | 56.9 | 194.9 |
## 5. Hướng dẫn chạy mô hình thời gian thực (Inference)
Dưới đây là đoạn mã nguồn cơ bản để khởi chạy mô hình nhận diện qua camera:

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

## Cấu trúc thư mục
```text
BTL_AI_Object_Identify_YOLO/
  mo_hinh/
  slide/
  requirements.txt
```

## Trích dẫn
Nếu bạn sử dụng repository này, vui lòng trích dẫn:

```bibtex
@misc{btlyolo,
  title        = {BTL: xác định vật thể bằng mô hình YOLO},
  author       = {Huynh Hai Nam and Le Nguyen Nhat Huy and Do Quoc Hoan},
  year         = {2025},
  howpublished = {GitHub repository},
  url          = {https://github.com/huylee733/AI-Object-Identify-YOLO12.git}
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
