import tkinter as tk
from tkinter import filedialog
import numpy as np
import math
from PIL import Image, ImageTk

# 相机内参矩阵
K = np.array([[2848.23936, 0, 1480.86663],
              [0, 2829.20319, 1263.07547],
              [0, 0, 1]])

# 旋转矩阵
R = np.array([[0.40159264, -0.0315387, 0.00658168],
              [0.01169769, 0.13829139, 0.9198773],
              [-0.02910238, -0.37732655, 0.39062604]])

# 平移向量
T = np.array([[4.237718], [-0.33933666], [17.933045]])

earth_semi_major_axis = 6378136.49  # 椭球体长半轴
earth_semi_minor_axis = 6356755.00  # 椭球体短半轴

# 默认的初始图片路径
default_image_path = "C:/Users/86138/Desktop/yolov5/images/up.jpeg"

# 默认相机位置经纬度
camera_latitude = 23.156679
camera_longitude = 113.354722


def calculate_lat_lon(pixel_x, pixel_y):
    # 像素坐标
    print(pixel_x, pixel_y)
    pixel_coords = np.array([[pixel_x], [pixel_y], [1]])

    # 计算世界坐标
    world_coords = np.linalg.inv(K) @ pixel_coords
    world_coords = R @ world_coords + T
    print(world_coords)
    # 将世界坐标系中的Xc和Yc坐标转换为地球表面的经纬度坐标
    Xc, Yc = world_coords[2][0], world_coords[0][0]

    # 根据用户输入的经纬度值更新相机位置并计算新的经纬度值
    new_camera_latitude = float(entry_camera_latitude.get())
    new_camera_longitude = float(entry_camera_longitude.get())
    world_latitude = new_camera_latitude + math.degrees(Yc / earth_semi_major_axis)
    world_longitude = new_camera_longitude - math.degrees(
        1.414*Xc / (earth_semi_major_axis * math.cos(math.radians(new_camera_latitude))))
    world_latitude = round(world_latitude, 6)
    world_longitude = round(world_longitude, 6)
    print(world_latitude, world_longitude)
    return world_latitude, world_longitude


def open_image():
    global width_orig, height_orig  # 声明全局变量
    file_path = filedialog.askopenfilename(initialdir=default_image_path)

    if file_path:
        image = Image.open(file_path)
        width_orig, height_orig = image.size

        max_size = (600, 600)
        image.thumbnail(max_size)

        root.geometry(f"1000x750")

        photo_image = ImageTk.PhotoImage(image)

        image_label.config(image=photo_image)
        image_label.image = photo_image

def calculate_and_show_result():
    pixel_x = width_orig / 2
    pixel_y = height_orig / 2
    latitude, longitude = calculate_lat_lon(pixel_x, pixel_y)

    confirm_button.pack_forget()  # 隐藏确认按钮
    result_label.pack_forget()  # 隐藏结果标签

    result_label.config(text=f"计算结果：\n纬度: {latitude}\n经度: {longitude}")

    # 显示确认按钮和结果标签，并设置垂直间距
    confirm_button.pack(pady=10)
    result_label.pack(pady=10)

root = tk.Tk()
root.title('图片中心点定位')
root.geometry("1000x750")

default_image = Image.open(default_image_path)
default_photo = ImageTk.PhotoImage(default_image)

image_label = tk.Label(root, image=default_photo)
image_label.pack(pady=10)

open_button_frame = tk.Frame(root)
open_button_frame.pack(pady=10)

open_button = tk.Button(open_button_frame, text='打开图片', command=open_image, bg='skyblue', fg='white', font=('Arial', 12))
open_button.pack(side='left')

entry_frame = tk.Frame(root)
entry_frame.pack(pady=10)

entry_camera_latitude_label = tk.Label(entry_frame, text="请输入相机纬度:")
entry_camera_latitude_label.pack(side='left')

entry_camera_latitude = tk.Entry(entry_frame)
entry_camera_latitude.insert(0, str(camera_latitude))
entry_camera_latitude.pack(side='left')

entry_camera_longitude_label = tk.Label(entry_frame, text="请输入相机经度:")
entry_camera_longitude_label.pack(side='left')

entry_camera_longitude = tk.Entry(entry_frame)
entry_camera_longitude.insert(0, str(camera_longitude))
entry_camera_longitude.pack(side='left')

confirm_button = tk.Button(root, text='确定', command=calculate_and_show_result, bg='green', fg='white', font=('Arial', 12))
confirm_button.pack(pady=10)

result_label = tk.Label(root, text="", font=('Arial', 12))
result_label.pack(pady=10)

root.mainloop()

