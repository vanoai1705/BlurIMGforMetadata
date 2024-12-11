import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_exif_data(image_path):
    """Trích xuất siêu dữ liệu EXIF từ hình ảnh."""
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if not exif_data:
            return None
        exif = {}
        for tag, value in exif_data.items():
            decoded_tag = TAGS.get(tag, tag)
            exif[decoded_tag] = value
        return exif
    except Exception as e:
        print(f"Lỗi khi đọc EXIF từ {image_path}: {e}")
        return None

def get_gps_data(exif):
    """Trích xuất dữ liệu GPS từ EXIF."""
    if not exif or "GPSInfo" not in exif:
        return None
    gps_info = {}
    for key in exif["GPSInfo"].keys():
        decoded_key = GPSTAGS.get(key, key)
        gps_info[decoded_key] = exif["GPSInfo"][key]
    return gps_info

def convert_to_degrees(value):
    """Chuyển đổi giá trị GPS (độ, phút, giây) sang dạng số thập phân."""
    try:
        d = float(value[0])  # Độ
        m = float(value[1])  # Phút
        s = float(value[2])  # Giây
        return d + (m / 60.0) + (s / 3600.0)
    except Exception as e:
        print(f"Lỗi khi chuyển đổi tọa độ: {e}")
        return None

def get_coordinates(gps_data):
    """Trích xuất tọa độ GPS từ dữ liệu GPS."""
    if not gps_data:
        return None
    latitude = gps_data.get("GPSLatitude")
    latitude_ref = gps_data.get("GPSLatitudeRef")
    longitude = gps_data.get("GPSLongitude")
    longitude_ref = gps_data.get("GPSLongitudeRef")

    if not latitude or not longitude or not latitude_ref or not longitude_ref:
        return None

    lat = convert_to_degrees(latitude)
    if latitude_ref != "N":
        lat = -lat

    lon = convert_to_degrees(longitude)
    if longitude_ref != "E":
        lon = -lon

    return lat, lon

def process_folder(folder_path, output_file):
    """Xử lý tất cả các hình ảnh trong thư mục và ghi kết quả ra tệp."""
    with open(output_file, "w", encoding="utf-8") as f:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith((".jpg", ".jpeg")):  # Lọc các tệp JPEG
                    image_path = os.path.join(root, file)
                    f.write(f"Đang kiểm tra tệp: {image_path}\n")
                    print(f"Đang kiểm tra tệp: {image_path}")
                    
                    exif_data = get_exif_data(image_path)
                    gps_data = get_gps_data(exif_data)
                    if gps_data:
                        coordinates = get_coordinates(gps_data)
                        if coordinates:
                            f.write(f"Tọa độ GPS: {coordinates}\n")
                            print(f"Tọa độ GPS: {coordinates}")
                        else:
                            f.write("NONE GPS\n")
                            print("NONE GPS")
                    else:
                        f.write("NONE GPS\n")
                        print("NONE GPS")

# Đường dẫn tới thư mục chứa hình ảnh
folder_path = "D:/metadataS2/OriginalPhoto/Oai/SS2_042"

# Đường dẫn tới tệp kết quả
output_file = "GPSResults.txt"

# Kiểm tra tất cả các hình ảnh trong thư mục và ghi kết quả ra tệp
process_folder(folder_path, output_file)

print(f"Kết quả đã được ghi vào tệp: {output_file}")
