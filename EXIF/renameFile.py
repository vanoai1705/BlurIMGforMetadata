# import os

# # Đường dẫn tới folder chứa các file
# folder_path = "D:/Fakemetadata/OutputEXIF"

# # Lặp qua tất cả các file trong folder
# for filename in os.listdir(folder_path):
#     # Kiểm tra nếu file bắt đầu bằng "DSC_"
#     if filename.startswith("DSC_"):
#         # Đổi "DSC_" thành "IMG_"
#         new_name = filename.replace("DSC_", "IMG_", 1)
#         # Đường dẫn đầy đủ của file cũ và file mới
#         old_file = os.path.join(folder_path, filename)
#         new_file = os.path.join(folder_path, new_name)
#         # Đổi tên file
#         os.rename(old_file, new_file)
#         print(f"Đã đổi tên: {filename} -> {new_name}")


#RANDOM NAME FOR MOBILE FILE
import os
import random

# Đường dẫn tới folder chứa các file
folder_path = "D:\Fakemetadata\OutputEXIF"

# Lấy danh sách file trong folder
files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

# Sắp xếp danh sách file (để đảm bảo thứ tự cố định khi đổi tên)
files.sort()

# Tạo danh sách số ngẫu nhiên tăng dần từ 1000
random_numbers = sorted(random.sample(range(5501, 5550), len(files)))

# Đổi tên từng file
for file, rand_num in zip(files, random_numbers):
    # Lấy phần mở rộng của file
    file_ext = os.path.splitext(file)[1]
    # Tạo tên mới với định dạng IMG_<random_number>
    new_name = f"IMG_{rand_num}{file_ext}"
    # Đường dẫn đầy đủ của file cũ và file mới
    old_file = os.path.join(folder_path, file)
    new_file = os.path.join(folder_path, new_name)
    # Đổi tên file
    os.rename(old_file, new_file)
    print(f"Đã đổi tên: {file} -> {new_name}")

