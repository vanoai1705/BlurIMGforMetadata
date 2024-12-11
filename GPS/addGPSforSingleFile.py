from PIL import Image
import piexif

def add_gps_to_image(image_path, output_path, latitude, longitude):
    def _to_dms(value, ref_positive, ref_negative):
        """
        Chuyển đổi tọa độ thập phân sang định dạng DMS (Degrees, Minutes, Seconds).
        """
        if value < 0:
            ref = ref_negative
        else:
            ref = ref_positive
        value = abs(value)
        degrees = int(value)
        minutes = int((value - degrees) * 60)
        seconds = round((value - degrees - minutes / 60) * 3600, 6)
        return ((degrees, 1), (minutes, 1), (int(seconds * 100), 100)), ref

    # Chuyển đổi latitude và longitude sang DMS
    lat_dms, lat_ref = _to_dms(latitude, 'N', 'S')
    lon_dms, lon_ref = _to_dms(longitude, 'E', 'W')

    # Tạo metadata GPS
    exif_dict = piexif.load(image_path)
    gps_ifd = {
        piexif.GPSIFD.GPSLatitudeRef: lat_ref.encode(),
        piexif.GPSIFD.GPSLatitude: lat_dms,
        piexif.GPSIFD.GPSLongitudeRef: lon_ref.encode(),
        piexif.GPSIFD.GPSLongitude: lon_dms,
    }

    exif_dict['GPS'] = gps_ifd

    # Lưu hình ảnh với metadata mới
    exif_bytes = piexif.dump(exif_dict)
    image = Image.open(image_path)
    image.save(output_path, exif=exif_bytes)
    print(f"GPS đã được thêm vào hình ảnh và lưu tại {output_path}")

# Sử dụng hàm
image_path = "D:\metadataS2\OriginalPhoto\Oai\SS2_027/IMG_4201.jpg"  # Đường dẫn đến ảnh gốc
output_path = "D:\metadataS2\OriginalPhoto\Oai\SS2_027/IMG_4201.jpg"  # Đường dẫn để lưu ảnh với GPS
latitude = 15.87744722222222222# Vĩ độ  
longitude = 108.326127755555555

add_gps_to_image(image_path, output_path, latitude, longitude)
