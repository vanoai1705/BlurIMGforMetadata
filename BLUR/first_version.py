import cv2
import numpy as np
from PIL import Image
import piexif

# Đọc ảnh JPG và dữ liệu EXIF bằng Pillo
original_image = Image.open("D:/metadata/OriginalPhoto/HS029/IMG_5251.jpg")
# original_image = Image.open("IMG_7105_Original.jpg")
exif_data = original_image.info.get("exif")

# Chuyển ảnh sang định dạng OpenCV
image = cv2.cvtColor(np.array(original_image), cv2.COLOR_RGB2BGR)
original_height, original_width = image.shape[:2]

# Tỷ lệ scale để ảnh hiển thị vừa màn hình
scale_percent = 25 # Ví dụ: Giảm kích thước xuống còn 25%
new_width = int(original_width * scale_percent / 100)
new_height = int(original_height * scale_percent / 100)
resized_image = cv2.resize(image, (new_width, new_height))

# Hàm làm mờ vùng được chọn
def blur_region(img, x1, y1, x2, y2, blur_strength=450):
    # Tăng blur_strength để làm mờ mạnh hơn
    kernel_width = (blur_strength // 2) * 2 + 1
    kernel_height = (blur_strength // 2) * 2 + 1
    # Áp dụng Gaussian Blur cho vùng được chọn
    face = img[y1:y2, x1:x2]
    face = cv2.GaussianBlur(face, (kernel_width, kernel_height), 0)
    img[y1:y2, x1:x2] = face
    return img

# Danh sách để lưu các vùng đã chọn
regions = []

# Vòng lặp để chọn nhiều vùng liên tiếp
while True:
    roi = cv2.selectROI("Select Region to Blur (Press Enter to confirm, Esc to finish)", resized_image, fromCenter=False, showCrosshair=True)
    
    # Nếu vùng chọn là hợp lệ (khác 0) thì lưu vào danh sách
    x, y, w, h = roi
    if w > 0 and h > 0:
        # Chuyển tọa độ về ảnh gốc
        x = int(x * 100 / scale_percent)
        y = int(y * 100 / scale_percent)
        w = int(w * 100 / scale_percent)
        h = int(h * 100 / scale_percent)
        
        # Lưu tọa độ vùng vào danh sách regions
        regions.append((x, y, x + w, y + h))
    else:
        # Nếu không có vùng chọn nào hoặc người dùng nhấn Esc thì kết thúc
        break

cv2.destroyAllWindows()

# Áp dụng làm mờ cho tất cả các vùng đã chọn
for (x1, y1, x2, y2) in regions:
    image = blur_region(image, x1, y1, x2, y2, blur_strength=450)

# Lưu ảnh đã làm mờ tạm thời
temp_path = "temp_blurred_image.jpg"
cv2.imwrite(temp_path, image)

# Mở lại ảnh đã làm mờ bằng Pillow và lưu với EXIF gốc
blurred_image = Image.open(temp_path)
blurred_image.save("D:/metadata/P006S029IMG009.jpg", exif=exif_data)

print("Image saved as 'blurred_with_gps.jpg' with EXIF data retained.")
