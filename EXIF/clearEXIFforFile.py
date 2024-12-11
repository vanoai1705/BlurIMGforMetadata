from PIL import Image

def clear_exif(image_path, output_path):
    # Mở ảnh và loại bỏ EXIF
    with Image.open(image_path) as img:
        data = list(img.getdata())  # Lấy dữ liệu pixel
        img_no_exif = Image.new(img.mode, img.size)  # Tạo ảnh mới không có EXIF
        img_no_exif.putdata(data)
        img_no_exif.save(output_path)

    print(f"EXIF metadata cleared and saved to {output_path}")

# Đường dẫn ảnh gốc và ảnh xuất ra
input_image = "D:/metadataS2/OriginalPhoto/Oai/SS2_004/DSC_0894.jpg"
output_image = "D:/metadataS2/OriginalPhoto/Oai/SS2_004/image_no_exif.jpg"

# Thực thi xóa EXIF
clear_exif(input_image, output_image)
