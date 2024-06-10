import numpy as np

# 相机内参矩阵
K = np.array([[978.54, 0, 626.88],
              [0, 979.6, 346.92],
              [0, 0, 1]])

# 旋转矩阵
R = np.array([[0.999, 0.00255, -0.0417],
              [-0.00151, 0.999, 0.0252],
              [0.0418, -0.0251, 0.998]])

# 平移向量
T = np.array([[-175.85, -9.216, 4.030]]).T

# 用户输入像素坐标
x_pixel = float(input("Enter x pixel coordinate: "))
y_pixel = float(input("Enter y pixel coordinate: "))

# 像素坐标
pixel_coords = np.array([[x_pixel], [y_pixel], [1]]) # 扩展为3x1列向量

# 计算世界坐标
world_coords = np.linalg.inv(K) @ pixel_coords
world_coords = R @ world_coords + T

# 输出结果
print("世界坐标：", world_coords.flatten())
