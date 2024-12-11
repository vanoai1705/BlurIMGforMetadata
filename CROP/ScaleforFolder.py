from PIL import Image
import os

def crop_images_to_fixed_ratio(input_folder, output_folder, target_width, target_height):
    # Tạo thư mục đầu ra nếu chưa tồn tại
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Duyệt qua tất cả các file trong thư mục đầu vào
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            try:
                # Mở ảnh
                with Image.open(input_path) as img:
                    original_width, original_height = img.size
                    target_aspect_ratio = target_width / target_height
                    original_aspect_ratio = original_width / original_height

                    # Crop ảnh để đạt đúng tỉ lệ
                    if original_aspect_ratio > target_aspect_ratio:
                        # Crop chiều ngang (ảnh quá rộng)
                        new_width = int(original_height * target_aspect_ratio)
                        left = (original_width - new_width) // 2
                        right = left + new_width
                        cropped_img = img.crop((left, 0, right, original_height))
                    else:
                        # Crop chiều dọc (ảnh quá cao)
                        new_height = int(original_width / target_aspect_ratio)
                        top = (original_height - new_height) // 2
                        bottom = top + new_height
                        cropped_img = img.crop((0, top, original_width, bottom))

                    # Resize ảnh về đúng kích thước đích (nếu cần)
                    cropped_img = cropped_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                    
                    # Lưu ảnh đã crop
                    cropped_img.save(output_path)
                    print(f"Đã crop: {filename}")

            except Exception as e:
                print(f"Lỗi khi xử lý file {filename}: {e}")

# Cấu hình thư mục và kích thước
input_folder = "D:\Fakemetadata\Input\Badminton Club - Da Nang"  # Thay bằng đường dẫn thư mục chứa ảnh đầu vào
output_folder = "D:\Fakemetadata\OutputCrop\Badminton Club - Da Nang"  # Thay bằng đường dẫn thư mục lưu ảnh đầu ra
target_width = 4032
target_height = 3024

#VERTICAL
# target_width = 3024
# target_height = 4032
crop_images_to_fixed_ratio(input_folder, output_folder, target_width, target_height)
