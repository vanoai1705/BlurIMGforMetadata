#DUPLICATE GPS
# from PIL import Image
# import piexif
# import os

# def add_gps_to_images(input_dir, output_dir, latitude, longitude):
#     def _to_dms(value, ref_positive, ref_negative):
#         """
#         Chuyển đổi tọa độ thập phân sang định dạng DMS (Degrees, Minutes, Seconds).
#         """
#         if value < 0:
#             ref = ref_negative
#         else:
#             ref = ref_positive
#         value = abs(value)
#         degrees = int(value)
#         minutes = int((value - degrees) * 60)
#         seconds = round((value - degrees - minutes / 60) * 3600, 6)
#         return ((degrees, 1), (minutes, 1), (int(seconds * 100), 100)), ref

#     # Chuyển đổi latitude và longitude sang DMS
#     lat_dms, lat_ref = _to_dms(latitude, 'N', 'S')
#     lon_dms, lon_ref = _to_dms(longitude, 'E', 'W')

#     # Kiểm tra và tạo thư mục đầu ra nếu chưa tồn tại
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)

#     # Duyệt qua tất cả các tệp trong thư mục đầu vào
#     for filename in os.listdir(input_dir):
#         if filename.lower().endswith(('.jpg', '.jpeg', '.png')):  # Chỉ xử lý tệp ảnh
#             input_path = os.path.join(input_dir, filename)
#             output_path = os.path.join(output_dir, filename)

#             try:
#                 # Tải EXIF metadata của ảnh
#                 exif_dict = piexif.load(input_path)
#                 gps_ifd = {
#                     piexif.GPSIFD.GPSLatitudeRef: lat_ref.encode(),
#                     piexif.GPSIFD.GPSLatitude: lat_dms,
#                     piexif.GPSIFD.GPSLongitudeRef: lon_ref.encode(),
#                     piexif.GPSIFD.GPSLongitude: lon_dms,
#                 }

#                 # Thêm metadata GPS
#                 exif_dict['GPS'] = gps_ifd
#                 exif_bytes = piexif.dump(exif_dict)

#                 # Lưu ảnh với metadata mới
#                 image = Image.open(input_path)
#                 image.save(output_path, exif=exif_bytes)
#                 print(f"GPS đã được thêm vào: {output_path}")

#             except Exception as e:
#                 print(f"Lỗi xử lý {filename}: {e}")

# # Sử dụng hàm
# input_directory = "D:/metadataS2/OriginalPhoto/Oai/SS2_004/GPS5"  # Thư mục chứa ảnh đầu vào
# output_directory = "D:/metadataS2/OriginalPhoto/Oai/SS2_004"  # Thư mục để lưu ảnh đã xử lý
# latitude    = 16.91272051111111 # Vĩ độ  
# longitude   = 107.1893568888888 # Kinh độ

# add_gps_to_images(input_directory, output_directory, latitude, longitude)

#=============================================

#RANDOM GPS
from PIL import Image
import piexif
import os
import random

def add_gps_to_images(input_dir, output_dir, latitude, longitude, offset_range=0.0001):
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

    # Kiểm tra và tạo thư mục đầu ra nếu chưa tồn tại
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Duyệt qua tất cả các tệp trong thư mục đầu vào
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):  # Chỉ xử lý tệp ảnh
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            try:
                # Sinh giá trị random offset cho tọa độ
                random_lat = latitude + random.uniform(-offset_range, offset_range)
                random_lon = longitude + random.uniform(-offset_range, offset_range)

                # Chuyển đổi tọa độ random sang DMS
                lat_dms, lat_ref = _to_dms(random_lat, 'N', 'S')
                lon_dms, lon_ref = _to_dms(random_lon, 'E', 'W')

                # Tải EXIF metadata của ảnh
                exif_dict = piexif.load(input_path)
                gps_ifd = {
                    piexif.GPSIFD.GPSLatitudeRef: lat_ref.encode(),
                    piexif.GPSIFD.GPSLatitude: lat_dms,
                    piexif.GPSIFD.GPSLongitudeRef: lon_ref.encode(),
                    piexif.GPSIFD.GPSLongitude: lon_dms,
                }

                # Thêm metadata GPS
                exif_dict['GPS'] = gps_ifd
                exif_bytes = piexif.dump(exif_dict)

                # Lưu ảnh với metadata mới
                image = Image.open(input_path)
                image.save(output_path, exif=exif_bytes)
                print(f"GPS đã được thêm vào: {output_path} (Lat: {random_lat}, Lon: {random_lon})")

            except Exception as e:
                print(f"Lỗi xử lý {filename}: {e}")

# Sử dụng hàm
input_directory = "D:\Fakemetadata\OutputEXIF"  # Thư mục chứa ảnh đầu vào
output_directory = "D:\Fakemetadata\OutputGPS"  # Thư mục để lưu ảnh đã xử lý
latitude    = 10.8008239999
longitude   = 106.6685266666
offset_range = 0.00001  # Biên độ lệch ngẫu nhiên (tạo độ chênh lệch nhỏ)

add_gps_to_images(input_directory, output_directory, latitude, longitude, offset_range)

