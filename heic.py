import cv2
import numpy as np
from PIL import Image
import pyheif
import piexif

# Đọc file HEIC và chuyển đổi sang định dạng mà OpenCV có thể xử lý
heif_file = pyheif.read("ĐƯỜNG DẪN TUYỆT ĐỐI CỦA HÌNH ẢNH") #VÍ DỤ: D:/folder/IMG_1102.HEIC
original_image = Image.frombytes(
    heif_file.mode, 
    heif_file.size, 
    heif_file.data, 
    "raw", 
    heif_file.mode, 
    heif_file.stride,
)
exif_data = original_image.info.get("exif")

image = cv2.cvtColor(np.array(original_image.convert("RGB")), cv2.COLOR_RGB2BGR)
original_height, original_width = image.shape[:2]

# Tỷ lệ scale để ảnh hiển thị vừa màn hình
scale_percent = 25  # Giảm kích thước xuống còn 25%
new_width = int(original_width * scale_percent / 100)
new_height = int(original_height * scale_percent / 100)
resized_image = cv2.resize(image, (new_width, new_height))

# Hàm làm mờ vùng được chọn
def blur_region(img, x1, y1, x2, y2, blur_strength=25):
    kernel_width = (blur_strength // 2) * 2 + 1
    kernel_height = (blur_strength // 2) * 2 + 1
    face = img[y1:y2, x1:x2]
    face = cv2.GaussianBlur(face, (kernel_width, kernel_height), 0)
    img[y1:y2, x1:x2] = face
    return img

# Danh sách để lưu các vùng đã chọn
regions = []

while True:
    roi = cv2.selectROI("Select Region to Blur (Press Enter to confirm, Esc to finish)", resized_image, fromCenter=False, showCrosshair=True)
    x, y, w, h = roi
    if w > 0 and h > 0:
        x = int(x * 100 / scale_percent)
        y = int(y * 100 / scale_percent)
        w = int(w * 100 / scale_percent)
        h = int(h * 100 / scale_percent)
        regions.append((x, y, x + w, y + h))
    else:
        break

cv2.destroyAllWindows()

# Áp dụng làm mờ cho tất cả các vùng đã chọn
for (x1, y1, x2, y2) in regions:
    image = blur_region(image, x1, y1, x2, y2, blur_strength=400) # tăng giá trị blur_strength để làm mờ hơn

# Lưu ảnh đã làm mờ tạm thời
temp_path = "temp_blurred_image.jpg"
cv2.imwrite(temp_path, image)

# lưu với EXIF gốc
blurred_image = Image.open(temp_path)
blurred_image.save("Đường dẫn folder lưu ảnh + tên ảnh", exif=exif_data) #VÍ DỤ: D:/folder/save/P004S001IMG001.jpg

print("Image saved as 'blurred_with_gps.jpg' with EXIF data retained.")
