import cv2
import numpy as np
from PIL import Image, ExifTags
import piexif
import os

# Đường dẫn tuyệt đối của file gốc và thư mục lưu file kết quả
# input_path = "D:/metadataS2/OriginalPhoto/Huyen/SS2_114/IMG_7020.jpg" 
input_path = "D:\metadataS2\OriginalPhoto\Oai\SS2_046/IMG_5541.jpg" # Đường dẫn tuyệt đối đến file gốc
output_dir = "D:/metadataS2/Output"       # Đường dẫn tuyệt đối đến thư mục lưu kết quả

# Đảm bảo thư mục đầu ra tồn tại
os.makedirs(output_dir, exist_ok=True)

# Đọc ảnh JPG và dữ liệu EXIF bằng Pillow

original_image = Image.open(input_path)
exif_data = original_image.info.get("exif")

# Kiểm tra và xoay ảnh dựa trên Orientation trong EXIF để hiển thị đúng chiều
orientation = None
for tag, value in ExifTags.TAGS.items():
    if value == 'Orientation':
        orientation = tag
        break

# Xoay ảnh nếu có thông tin Orientation
exif = original_image._getexif()
if exif is not None and orientation in exif:
    orientation_value = exif[orientation]
    if orientation_value == 3:
        display_image = original_image.rotate(180, expand=True)
    elif orientation_value == 6:
        display_image = original_image.rotate(270, expand=True)
    elif orientation_value == 8:
        display_image = original_image.rotate(90, expand=True)
    else:
        display_image = original_image.copy()
else:
    display_image = original_image.copy()

# Chuyển đổi ảnh hiển thị về OpenCV sau khi xoay đúng hướng
image = cv2.cvtColor(np.array(display_image), cv2.COLOR_RGB2BGR)
original_height, original_width = image.shape[:2]

# Tỷ lệ scale để ảnh hiển thị vừa màn hình
scale_percent = 20
new_width = int(original_width * scale_percent / 100)
new_height = int(original_height * scale_percent / 100)
resized_image = cv2.resize(image, (new_width, new_height))

# Hàm làm mờ vùng được chọn
def blur_region(img, x1, y1, x2, y2, blur_strength=700):
    kernel_width = (blur_strength // 2) * 2 + 1
    kernel_height = (blur_strength // 2) * 2 + 1
    face = img[y1:y2, x1:x2]
    face = cv2.GaussianBlur(face, (kernel_width, kernel_height), 0)
    img[y1:y2, x1:x2] = face
    return img

# Cho phép người dùng chọn nhiều vùng làm mờ
while True:
    roi = cv2.selectROI("Select Region to Blur (Press ENTER to confirm, ESC to finish)", resized_image, fromCenter=False, showCrosshair=True)
    if roi == (0, 0, 0, 0):
        break

    x, y, w, h = roi
    x = int(x * 100 / scale_percent)
    y = int(y * 100 / scale_percent)
    w = int(w * 100 / scale_percent)
    h = int(h * 100 / scale_percent)

    if w > 0 and h > 0:
        image = blur_region(image, x, y, x + w, y + h, blur_strength=700)

    resized_image = cv2.resize(image, (new_width, new_height))

cv2.destroyAllWindows()

# Chuyển ảnh về chiều gốc
final_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
if orientation_value == 3:
    final_image = final_image.rotate(180, expand=True)
elif orientation_value == 6:
    final_image = final_image.rotate(90, expand=True)
elif orientation_value == 8:
    final_image = final_image.rotate(270, expand=True)

# Tạo đường dẫn cho file đầu ra
filename = os.path.basename(input_path)
output_path = os.path.join(output_dir, f"{filename}")

# Lưu ảnh đã làm mờ với EXIF vào đường dẫn đầu ra
final_image.save(output_path, exif=exif_data)

print(f"Image saved as '{output_path}' with EXIF data retained.")
