import os
import pyexiv2
import random

def update_random_iso(input_folder):
    # Các giá trị ISO có thể chọn
    iso_values = [50, 75, 100]

    # Lấy danh sách file trong thư mục
    files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.jpg', '.jpeg'))]

    for file_name in files:
        file_path = os.path.join(input_folder, file_name)

        # Chọn giá trị ISO ngẫu nhiên
        random_iso = random.choice(iso_values)
        print(f"Updating '{file_name}' with ISO: {random_iso}")

        try:
            # Mở ảnh và đọc metadata
            image = pyexiv2.Image(file_path)
            metadata = image.read_exif()
            
            # Ghi giá trị ISO vào metadata
            metadata['Exif.Photo.ISOSpeedRatings'] = str(random_iso)
            image.modify_exif(metadata)
            image.close()

        except Exception as e:
            print(f"Error updating {file_name}: {e}")

# Đường dẫn tới thư mục chứa ảnh
input_folder = "D:\Fakemetadata\OutputEXIF"

# Thực thi
update_random_iso(input_folder)
