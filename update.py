import cv2
import numpy as np
from PIL import Image
import piexif
import os

# Đường dẫn tuyệt đối của file gốc và thư mục lưu file kết quả
input_path = "D:/metadata/OriginalPhoto/1.Converted/HS037/IMG_0708.jpg"  # Đường dẫn tuyệt đối đến file gốc
output_dir = "D:/metadata/"       # Đường dẫn tuyệt đối đến thư mục lưu kết quả

# Đảm bảo thư mục đầu ra tồn tại
os.makedirs(output_dir, exist_ok=True)

# Đọc ảnh JPG và dữ liệu EXIF bằng Pillow
original_image = Image.open(input_path)
exif_data = original_image.info.get("exif")

# Chuyển ảnh sang định dạng OpenCV
image = cv2.cvtColor(np.array(original_image), cv2.COLOR_RGB2BGR)
original_height, original_width = image.shape[:2]

# Tỷ lệ scale để ảnh hiển thị vừa màn hình
scale_percent = 25  # Giảm kích thước xuống còn 50% cho dễ chọn vùng
new_width = int(original_width * scale_percent / 100)
new_height = int(original_height * scale_percent / 100)
resized_image = cv2.resize(image, (new_width, new_height))

# Hàm làm mờ vùng được chọn
def blur_region(img, x1, y1, x2, y2, blur_strength=450):
    kernel_width = (blur_strength // 2) * 2 + 1
    kernel_height = (blur_strength // 2) * 2 + 1
    face = img[y1:y2, x1:x2]
    face = cv2.GaussianBlur(face, (kernel_width, kernel_height), 0)
    img[y1:y2, x1:x2] = face
    return img

# Cho phép người dùng chọn nhiều vùng làm mờ
while True:
    roi = cv2.selectROI("Select Region to Blur (Press ENTER to confirm, ESC to finish)", resized_image, fromCenter=False, showCrosshair=True)
    
    # Thoát nếu người dùng nhấn ESC hoặc không chọn vùng nào
    if roi == (0, 0, 0, 0):
        break

    # Lấy tọa độ vùng được chọn và chuyển về kích thước gốc
    x, y, w, h = roi
    x = int(x * 100 / scale_percent)
    y = int(y * 100 / scale_percent)
    w = int(w * 100 / scale_percent)
    h = int(h * 100 / scale_percent)

    # Áp dụng làm mờ cho vùng đã chọn
    if w > 0 and h > 0:
        image = blur_region(image, x, y, x + w, y + h, blur_strength=450)

    # Cập nhật lại hình ảnh đã làm mờ để hiển thị tiếp
    resized_image = cv2.resize(image, (new_width, new_height))

# Đóng cửa sổ sau khi chọn xong
cv2.destroyAllWindows()

# Lấy tên file gốc và tạo đường dẫn cho file đầu ra với tiền tố "blurred_"
filename = os.path.basename(input_path)
output_path = os.path.join(output_dir, f"{filename}")

# Lưu ảnh đã làm mờ với EXIF vào đường dẫn đầu ra
temp_path = "temp_blurred_image.jpg"
cv2.imwrite(temp_path, image)
blurred_image = Image.open(temp_path)
blurred_image.save(output_path, exif=exif_data)

print(f"Image saved as '{output_path}' with EXIF data retained.")
