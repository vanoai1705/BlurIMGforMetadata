import os
import pyexiv2

def copy_metadata_to_folder(source_image_path, target_folder_path):
    # Đọc metadata từ ảnh gốc
    source_image = pyexiv2.Image(source_image_path)
    exif_data = source_image.read_exif()
    iptc_data = source_image.read_iptc()
    xmp_data = source_image.read_xmp()
    source_image.close()

    # Lặp qua từng file trong thư mục đích
    for file_name in os.listdir(target_folder_path):
        target_path = os.path.join(target_folder_path, file_name)

        # Kiểm tra xem file có phải là ảnh không
        if os.path.isfile(target_path) and file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            print(f"Copying metadata to: {file_name}")
            target_image = pyexiv2.Image(target_path)

            # Ghi metadata vào ảnh đích
            target_image.modify_exif(exif_data)
            target_image.modify_iptc(iptc_data)
            target_image.modify_xmp(xmp_data)
            target_image.close()

    print("Metadata copied to all images in the folder!")

# Đường dẫn tới ảnh gốc
source_image_path = 'D:/Fakemetadata/srcEXIF11.jpg'

# Đường dẫn tới thư mục chứa ảnh đích
target_folder_path = 'D:/Fakemetadata/OutputEXIF'

# Thực thi sao chép
copy_metadata_to_folder(source_image_path, target_folder_path)
