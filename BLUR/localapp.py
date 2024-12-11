import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ExifTags
import cv2
import numpy as np
import os

# Hàm xoay ảnh dựa trên thông tin EXIF Orientation
def correct_orientation(image):
    orientation_tag = None
    for tag, value in ExifTags.TAGS.items():
        if value == "Orientation":
            orientation_tag = tag
            break

    exif = image._getexif()
    if exif is not None and orientation_tag in exif:
        orientation = exif[orientation_tag]
        if orientation == 3:
            image = image.rotate(180, expand=True)
        elif orientation == 6:
            image = image.rotate(270, expand=True)
        elif orientation == 8:
            image = image.rotate(90, expand=True)
    return image

# Hàm scale ảnh theo tỷ lệ màn hình
def scale_image(image, max_width, max_height):
    width, height = image.size
    scale_factor = min(max_width / width, max_height / height)
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS), scale_factor

# Hàm chọn file ảnh
def open_file():
    global img, img_cv, filename, img_tk, scale_factor, exif_data
    filename = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.jpeg *.png")]
    )
    if not filename:
        return

    # Đọc ảnh và xoay đúng chiều
    image = Image.open(filename)
    exif_data = image.info.get("exif")
    image = correct_orientation(image)

    # Scale ảnh theo kích thước màn hình
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight() - 100  # Trừ đi chiều cao giao diện
    scaled_image, scale_factor = scale_image(image, screen_width, screen_height)

    # Cập nhật hình ảnh
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    img = scaled_image
    img_tk = ImageTk.PhotoImage(scaled_image)
    canvas.config(width=scaled_image.width, height=scaled_image.height)
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

# Hàm vẽ hình chữ nhật
def draw_rectangle(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y

def release_rectangle(event):
    global img_cv
    end_x, end_y = event.x, event.y
    if start_x != end_x and start_y != end_y:
        # Chuyển tọa độ vùng từ ảnh đã scale về ảnh gốc
        x1, y1 = int(start_x / scale_factor), int(start_y / scale_factor)
        x2, y2 = int(end_x / scale_factor), int(end_y / scale_factor)

        # Áp dụng Gaussian Blur lên vùng được chọn
        blur_strength = 700
        kernel_width = (blur_strength // 2) * 2 + 1
        kernel_height = (blur_strength // 2) * 2 + 1
        img_cv[y1:y2, x1:x2] = cv2.GaussianBlur(img_cv[y1:y2, x1:x2], (kernel_width, kernel_height), 0)

        # Cập nhật lại hình ảnh đã làm mờ
        updated_image = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
        scaled_updated_image, _ = scale_image(updated_image, img.width, img.height)
        img_tk_updated = ImageTk.PhotoImage(scaled_updated_image)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk_updated)
        canvas.image = img_tk_updated

# Hàm lưu file
def save_file():
    if img_cv is None:
        messagebox.showerror("Error", "No image to save!")
        return

    # Yêu cầu người dùng chọn thư mục lưu
    save_dir = filedialog.askdirectory()
    if not save_dir:
        return

    # Sử dụng tên file gốc
    base, ext = os.path.splitext(os.path.basename(filename))
    output_path = os.path.join(save_dir, f"{base}{ext}")

    final_image = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))

    # Kiểm tra và lưu EXIF nếu có
    if exif_data is not None:
        final_image.save(output_path, exif=exif_data)
    else:
        final_image.save(output_path)

    messagebox.showinfo("Saved", f"File saved to {output_path}")

# Tạo giao diện Tkinter
root = tk.Tk()
root.title("Blur Region Tool")

frame = tk.Frame(root)
frame.pack(pady=10)

btn_open = tk.Button(frame, text="Open Image", command=open_file)
btn_open.pack(side=tk.LEFT, padx=5)

btn_save = tk.Button(frame, text="Save Image", command=save_file)
btn_save.pack(side=tk.LEFT, padx=5)

canvas = tk.Canvas(root, bg="gray")
canvas.pack()

canvas.bind("<ButtonPress-1>", draw_rectangle)
canvas.bind("<ButtonRelease-1>", release_rectangle)

root.mainloop()
