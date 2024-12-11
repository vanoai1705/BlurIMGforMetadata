from PIL import Image

def crop_image_to_aspect_ratio(input_file, output_file, target_width, target_height):
    try:
        # Mở file ảnh
        with Image.open(input_file) as img:
            original_width, original_height = img.size

            # Tính toán vị trí crop để giữ trung tâm
            target_aspect_ratio = target_width / target_height
            original_aspect_ratio = original_width / original_height

            if original_aspect_ratio > target_aspect_ratio:
                # Ảnh quá rộng, cần crop chiều ngang
                new_width = int(original_height * target_aspect_ratio)
                offset = (original_width - new_width) // 2
                crop_box = (offset, 0, offset + new_width, original_height)
            else:
                # Ảnh quá cao, cần crop chiều dọc
                new_height = int(original_width / target_aspect_ratio)
                offset = (original_height - new_height) // 2
                crop_box = (0, offset, original_width, offset + new_height)

            # Crop ảnh
            cropped_img = img.crop(crop_box)

            # Resize để đảm bảo kích thước đúng (nếu cần)
            final_img = cropped_img.resize((target_width, target_height), Image.Resampling.LANCZOS)

            # Lưu ảnh đã crop
            final_img.save(output_file)
            print(f"Ảnh đã được crop và lưu: {output_file}")

    except Exception as e:
        print(f"Lỗi khi crop ảnh: {e}")

# Đường dẫn file và cấu hình kích thước
input_file = "D:\Fakemetadata\Input\Lunar New Year photo - Quang Tri/NIK_1320.jpg"  # Đường dẫn ảnh đầu vào
output_file = "D:\Fakemetadata\Output\Lunar New Year photo - Quang Tri/NIK_1320.jpg"  # Đường dẫn ảnh đầu ra
target_width = 4032
target_height = 3024

crop_image_to_aspect_ratio(input_file, output_file, target_width, target_height)
# from PIL import Image, ExifTags

# def crop_image_to_aspect_ratio(input_file, output_file, target_width, target_height):
#     try:
#         # Mở file ảnh
#         with Image.open(input_file) as img:
#             # Xử lý thông tin EXIF để xoay ảnh về hướng đúng
#             try:
#                 for orientation in ExifTags.TAGS.keys():
#                     if ExifTags.TAGS[orientation] == 'Orientation':
#                         break
#                 exif = img._getexif()
#                 if exif and orientation in exif:
#                     if exif[orientation] == 3:
#                         img = img.rotate(180, expand=True)
#                     elif exif[orientation] == 6:
#                         img = img.rotate(270, expand=True)
#                     elif exif[orientation] == 8:
#                         img = img.rotate(90, expand=True)
#             except Exception as e:
#                 print(f"Lỗi khi xử lý EXIF: {e}")

#             original_width, original_height = img.size

#             # Tính toán tỉ lệ crop
#             target_aspect_ratio = target_width / target_height
#             original_aspect_ratio = original_width / original_height

#             if original_aspect_ratio > target_aspect_ratio:
#                 # Ảnh quá rộng, cần crop chiều ngang
#                 new_width = int(original_height * target_aspect_ratio)
#                 offset = (original_width - new_width) // 2
#                 crop_box = (offset, 0, offset + new_width, original_height)
#             else:
#                 # Ảnh quá cao, cần crop chiều dọc
#                 new_height = int(original_width / target_aspect_ratio)
#                 offset = (original_height - new_height) // 2
#                 crop_box = (0, offset, original_width, offset + new_height)

#             # Crop ảnh
#             cropped_img = img.crop(crop_box)

#             # Resize để đảm bảo kích thước đúng
#             final_img = cropped_img.resize((target_width, target_height), Image.Resampling.LANCZOS)

#             # Lưu ảnh đã crop
#             final_img.save(output_file)
#             print(f"Ảnh đã được crop và lưu: {output_file}")

#     except Exception as e:
#         print(f"Lỗi khi crop ảnh: {e}")

# # Đường dẫn file và cấu hình kích thước
# input_file = "D:/Fakemetadata/demGPS/DSC_1559.jpg"  # Đường dẫn ảnh đầu vào
# output_file = "D:/Fakemetadata/Output/DSC_1559.jpg"  # Đường dẫn ảnh đầu ra
# target_width = 4032
# target_height = 3024

# crop_image_to_aspect_ratio(input_file, output_file, target_width, target_height)
