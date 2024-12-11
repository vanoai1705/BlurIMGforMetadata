import os
from PIL import Image

def clear_exif_folder(input_folder, output_folder):
    # Tạo thư mục đích nếu chưa tồn tại
    os.makedirs(output_folder, exist_ok=True)

    # Duyệt qua từng file trong thư mục nguồn
    for file_name in os.listdir(input_folder):
        input_path = os.path.join(input_folder, file_name)

        # Kiểm tra xem file có phải là ảnh không
        if os.path.isfile(input_path) and file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            print(f"Processing: {file_name}")

            # Mở ảnh và xóa EXIF
            try:
                with Image.open(input_path) as img:
                    data = list(img.getdata())  # Lấy dữ liệu pixel
                    img_no_exif = Image.new(img.mode, img.size)  # Tạo ảnh mới không có EXIF
                    img_no_exif.putdata(data)

                    # Lưu ảnh vào thư mục đích
                    output_path = os.path.join(output_folder, file_name)
                    img_no_exif.save(output_path)
                    print(f"Saved without EXIF: {output_path}")
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

# Đường dẫn thư mục nguồn (có ảnh gốc)
input_folder = "D:\Fakemetadata\OutputCrop\Badminton Club - Da Nang"

# Đường dẫn thư mục đích (để lưu ảnh không có EXIF)
output_folder = "D:/Fakemetadata/OutputEXIF"

# Thực thi
clear_exif_folder(input_folder, output_folder)
