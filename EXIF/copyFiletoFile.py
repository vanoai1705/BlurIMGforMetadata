import pyexiv2

def copy_all_metadata(source_path, target_path):
    # Mở ảnh nguồn và ảnh đích
    source_image = pyexiv2.Image(source_path)
    target_image = pyexiv2.Image(target_path)

    # Đọc tất cả các loại metadata từ ảnh nguồn
    exif_data = source_image.read_exif()  # EXIF data
    iptc_data = source_image.read_iptc()  # IPTC data
    xmp_data = source_image.read_xmp()    # XMP data

    # Ghi các loại metadata vào ảnh đích
    target_image.modify_exif(exif_data)
    target_image.modify_iptc(iptc_data)
    target_image.modify_xmp(xmp_data)

    # Đóng file
    source_image.close()
    target_image.close()

    print("All metadata copied successfully!")

# Đường dẫn tới ảnh
source_image_path = 'D:/metadataS2/OriginalPhoto/Oai/SS2_004/IMG_4244.jpg'  # Ảnh nguồn
target_image_path = 'D:/metadataS2/OriginalPhoto/Oai/SS2_004/DSC_1559.jpg'  # Ảnh đích

# Thực thi sao chép
copy_all_metadata(source_image_path, target_image_path)
