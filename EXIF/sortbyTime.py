# import os
# import pyexiv2
# from datetime import datetime, timedelta

# def add_date_taken(input_folder):
#     # Lấy danh sách file trong thư mục và sắp xếp theo tên
#     files = sorted(f for f in os.listdir(input_folder) if f.lower().endswith(('.jpg', '.jpeg')))
    
#     # Ngày bắt đầu và thời gian ban đầu
#     start_date = datetime(2024, 10, 3, 18 , 0, 0)  # Bắt đầu từ 8:00 sáng
#     time_increment = timedelta(minutes=3)  # Mỗi file thêm 10 phút

#     for index, file_name in enumerate(files):
#         file_path = os.path.join(input_folder, file_name)
#         current_time = start_date + index * time_increment

#         # Định dạng ngày giờ theo chuẩn EXIF
#         exif_date = current_time.strftime("%Y:%m:%d %H:%M:%S")
#         print(f"Updating '{file_name}' with Date Taken: {exif_date}")

#         # Thêm DateTimeOriginal vào metadata
#         try:
#             image = pyexiv2.Image(file_path)
#             metadata = image.read_exif()
#             metadata['Exif.Photo.DateTimeOriginal'] = exif_date
#             metadata['Exif.Photo.DateTimeDigitized'] = exif_date
#             metadata['Exif.Image.DateTime'] = exif_date  # Đồng bộ thời gian chỉnh sửa
#             image.modify_exif(metadata)
#             image.close()
#         except Exception as e:
#             print(f"Error updating {file_name}: {e}")

# # Đường dẫn tới thư mục chứa ảnh
# input_folder = "D:/metadataS2/Output/18+/BookStore"

# # Thực thi
# add_date_taken(input_folder)


#RANDOM TIME
import os
import pyexiv2
from datetime import datetime, timedelta
import random

def add_random_date_taken(input_folder):
    # Lấy danh sách file trong thư mục và sắp xếp theo tên
    files = sorted(f for f in os.listdir(input_folder) if f.lower().endswith(('.jpg', '.jpeg')))
    
    # Ngày bắt đầu và thời gian ban đầu
    start_date = datetime(2024, 9, 10, 19, 1, 0)  # Bắt đầu từ 8:00 sáng

    for file_name in files:
        file_path = os.path.join(input_folder, file_name)
        
        # Sinh khoảng thời gian ngẫu nhiên từ 1 đến 30 phút
        random_minutes = random.randint(3, 7)
        start_date += timedelta(minutes=random_minutes)

        # Định dạng ngày giờ theo chuẩn EXIF
        exif_date = start_date.strftime("%Y:%m:%d %H:%M:%S")
        print(f"Updating '{file_name}' with Date Taken: {exif_date}")

        # Thêm DateTimeOriginal vào metadata
        try:
            image = pyexiv2.Image(file_path)
            metadata = image.read_exif()
            metadata['Exif.Photo.DateTimeOriginal'] = exif_date
            metadata['Exif.Photo.DateTimeDigitized'] = exif_date
            metadata['Exif.Image.DateTime'] = exif_date  # Đồng bộ thời gian chỉnh sửa
            image.modify_exif(metadata)
            image.close()
        except Exception as e:
            print(f"Error updating {file_name}: {e}")

# Đường dẫn tới thư mục chứa ảnh
input_folder = "D:\Fakemetadata\OutputEXIF"

# Thực thi
add_random_date_taken(input_folder)
