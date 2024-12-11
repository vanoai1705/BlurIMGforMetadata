import cv2
import numpy as np
from PIL import Image
import piexif

# Đọc ảnh JPG và dữ liệu EXIF bằng Pillow
original_image = Image.open("D:/metadata/OriginalPhoto/DaiNoiHue/IMG_8885.jpg")
exif_data = original_image.info.get("exif")

# Chuyển ảnh sang định dạng OpenCV
image = cv2.cvtColor(np.array(original_image), cv2.COLOR_RGB2BGR)
original_height, original_width = image.shape[:2]

# Tỷ lệ scale để ảnh hiển thị 
scale_percent = 20  # Giảm kích thước xuống còn 20% cho vừa màn hình
new_width = int(original_width * scale_percent / 100)
new_height = int(original_height * scale_percent / 100)
resized_image = cv2.resize(image, (new_width, new_height))

# Hàm làm mờ vùng được chọn
def blur_region(img, x1, y1, x2, y2, blur_strength=500):
    # Tăng giá trị blur_strength để làm mờ 
    kernel_width = (blur_strength // 2) * 2 + 1
    kernel_height = (blur_strength // 2) * 2 + 1
    # Áp dụng Gaussian Blur cho vùng được chọn
    face = img[y1:y2, x1:x2]
    face = cv2.GaussianBlur(face, (kernel_width, kernel_height), 0)
    img[y1:y2, x1:x2] = face
    return img

# Sử dụng OpenCV để cho phép người dùng chọn vùng làm mờ
roi = cv2.selectROI("Select Region to Blur", resized_image, fromCenter=False, showCrosshair=True)
cv2.destroyAllWindows()

# Lấy tọa độ vùng được chọn và chuyển về kích thước gốc
x, y, w, h = roi
x = int(x * 100 / scale_percent)
y = int(y * 100 / scale_percent)
w = int(w * 100 / scale_percent)
h = int(h * 100 / scale_percent)

if w > 0 and h > 0:
    # Áp dụng làm mờ cho vùng đã chọn với độ mạnh hơn
    image = blur_region(image, x, y, x + w, y + h, blur_strength=500)

# Lưu ảnh đã làm mờ tạm thời
temp_path = "temp_blurred_image.jpg"
cv2.imwrite(temp_path, image)

# Mở lại ảnh đã làm mờ bằng Pillow và lưu với EXIF gốc
blurred_image = Image.open(temp_path)
blurred_image.save("D:/metadata/Blurred/610/P004S001IMG001.jpg", exif=exif_data)

print("Image saved as 'blurred_with_gps.jpg' with EXIF data retained.")
