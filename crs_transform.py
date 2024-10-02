# import cv2
import json
import numpy as np
import quaternion
import bisect
import os
from math import sin, cos, sqrt, radians
from common_settings import pose_output_sub_path

print_switch = False

# struct EgoPose
class EgoPose:
    def __init__(self, timestamp = 0, longitude = 0, latitude = 0, height = 0, utmx = 0, utmy = 0, px = 0, py = 0, pz = 0, quaternion = [0, 0, 0, 0]):
        self.timestamp = timestamp
        self.longitude = longitude
        self.latitude = latitude
        self.height = height
        self.utmx = utmx
        self.utmy = utmy
        self.px = px
        self.py = py
        self.pz = pz
        self.quaternion = quaternion

    distance = lambda self, other: sqrt((self.px - other.px) ** 2 + (self.py - other.py) ** 2 + (self.pz - other.pz) ** 2)
    to_string = lambda self: "{" + f"\"timestamp\": {self.timestamp}, \"longitude\": {self.longitude}, \"latitude\": {self.latitude}, \"height\": {self.height}, \"utmx\": {self.utmx}, \"utmy\": {self.utmy}, \"px\": {self.px}, \"py\": {self.py}, \"pz\": {self.pz}, \"quaternion\": {self.quaternion}" + "}"

# loadJsonMatrix函数，用于加载JSON文件中的4✖️4矩阵
def load_json_matrix(jsonFile, paths) -> np.ndarray:
    matrix = np.zeros((4, 4), dtype=np.float64)
    if not os.path.exists(jsonFile):
        print(f"file {jsonFile} not exist")
        return None

    with open(jsonFile, 'r') as f:
        data = json.load(f)
        for path in paths:
            if path not in data:
                print(f"key {path} not exist in {jsonFile}")
                return None
            data = data[path]

        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                if i < len(data) and j < len(data[i]):
                    matrix[i, j] = data[i][j]
                else:
                    print(f"load {jsonFile} data error")
                    return None
    
    return matrix

# gnss到lidar的转换矩阵
def get_gnss2lidar(clip_path) -> np.ndarray:
    paths = ["gnss-to-lidar-top", "param", "sensor_calib", "data"]
    gnss2lidar = load_json_matrix(os.path.join(clip_path, "calib_extract", "calib_gnss_to_lidar_top.json"), paths)
    if gnss2lidar.shape != (4, 4):
        print("load calib_gnss_to_lidar_top data error")
        return None

    if gnss2lidar[0, 0] > gnss2lidar[0, 1]:
        data = np.array([
            [0, 1, 0, 0],
            [-1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float64)
        gnss2lidar = np.dot(data, gnss2lidar)

    return gnss2lidar

# lidar到车的转换矩阵
def get_lidar2car(clip_path) -> np.ndarray:
    paths = ["lidar-top-to-car", "param", "sensor_calib", "data"]
    lidar2car = load_json_matrix(os.path.join(clip_path, "calib_extract", "calib_lidar_top_to_car.json"), paths)
    if lidar2car.shape != (4, 4):
        print("load calib_lidar_top_to_car data error")
        return None

    return lidar2car

# gnss到车的转换矩阵
def get_gnss2CarRT(clip_path) -> np.ndarray:
    gnss2lidar = get_gnss2lidar(clip_path)
    lidar2car = get_lidar2car(clip_path)
    gnss2CarRT = np.dot(lidar2car, gnss2lidar)
    if print_switch:
        print("gnss2lidar:")
        print(gnss2lidar)
        print("lidar2car:")
        print(lidar2car)
        print("gnss2CarRT:")
        print(gnss2CarRT)
    return gnss2CarRT

# 读取轨迹的txt文件
def read_txt_to_ego_poses(clip_path):
    ego_poses = []
    with open(clip_path + pose_output_sub_path, "r") as f:
        lines = f.readlines()
        # skip frist line
        for line in lines[1:]:
            line = line.strip()
            if line == "":
                continue
            items = line.split(",")
            if len(items) != 17:
                print(f"line {line} format error")
                continue
            pose = EgoPose()
            pose.timestamp = int(items[0])
            pose.longitude = float(items[2])
            pose.latitude = float(items[1])
            pose.height = float(items[3])
            pose.utmx = float(items[7])
            pose.utmy = float(items[8])
            pose.utmz = float(items[9])
            xyz = wgs84_to_ecef(pose.longitude, pose.latitude, pose.height)
            pose.px = xyz[0]
            pose.py = xyz[1]
            pose.pz = xyz[2]
            pose.quaternion = [float(items[13]), float(items[14]), float(items[15]), float(items[16])]
            ego_poses.append(pose)
    return ego_poses

# 查找函数，用于根据时间戳查找ego_poses中左右的元素
def find_poses_in_range(ego_poses, timestamp):
    # 使用 bisect 找到索引等于timestamp的元素
    index = bisect.bisect_left([pose.timestamp for pose in ego_poses], timestamp)
    if index < len(ego_poses) and ego_poses[index].timestamp == timestamp:
        return [ego_poses[index]]
    # 使用 bisect 找到范围的开始和结束索引
    start_index = bisect.bisect_left([pose.timestamp for pose in ego_poses], timestamp)
    end_index = bisect.bisect_right([pose.timestamp for pose in ego_poses], timestamp)
    
    if start_index == end_index:
        start_index = start_index - 1 if start_index - 1 > 0 else 0
        end_index = end_index + 1 if end_index + 1 < len(ego_poses) else len(ego_poses)
        return ego_poses[start_index:end_index]
    # 返回时间范围内的左右元素
    return ego_poses[start_index:end_index + 1]

# 查找函数，用于根据时间戳查找ego_poses中该时间戳的临近元素（默认下一个元素，没有则上一个元素）
def find_poses_near(ego_poses, timestamp):
    # 使用 bisect 找到索引等于timestamp的元素
    index = bisect.bisect_left([pose.timestamp for pose in ego_poses], timestamp)
    if index + 1 < len(ego_poses):
        return [ego_poses[index + 1]]
    else:
        return [ego_poses[index - 1]]
        
# 插值函数
def interpolate_poses(ego_poses, timestamp):
    # 查找时间范围内的左右元素
    poses_in_range = find_poses_in_range(ego_poses, timestamp)
    if print_switch:
        print("poses_in_range[0]:")
        print(poses_in_range[0].to_string())
        print("poses_in_range[1]:")
        print(poses_in_range[1].to_string())
    # return poses_in_range[1]
    if len(poses_in_range) == 0:
        return None

    # 如果左右元素都是同一个时间戳，则直接返回
    if len(poses_in_range) == 1:
        return poses_in_range[0]

    # 如果左右元素不是同一个时间戳，则进行插值
    left_pose = poses_in_range[0]
    right_pose = poses_in_range[1]
    left_time = left_pose.timestamp
    right_time = right_pose.timestamp
    if left_time == right_time:
        return left_pose

    # 计算插值比例
    ratio = (timestamp - left_time) / (right_time - left_time)
    # 插值
    pose = EgoPose()
    pose.timestamp = timestamp
    pose.longitude = left_pose.longitude + (right_pose.longitude - left_pose.longitude) * ratio
    pose.latitude = left_pose.latitude + (right_pose.latitude - left_pose.latitude) * ratio
    pose.height = left_pose.height + (right_pose.height - left_pose.height) * ratio
    pose.utmx = left_pose.utmx + (right_pose.utmx - left_pose.utmx) * ratio
    pose.utmy = left_pose.utmy + (right_pose.utmy - left_pose.utmy) * ratio
    pose.utmz = left_pose.utmz + (right_pose.utmz - left_pose.utmz) * ratio
    pose.px = left_pose.px + (right_pose.px - left_pose.px) * ratio
    pose.py = left_pose.py + (right_pose.py - left_pose.py) * ratio
    pose.pz = left_pose.pz + (right_pose.pz - left_pose.pz) * ratio
    pose.quaternion = [
        left_pose.quaternion[0] + (right_pose.quaternion[0] - left_pose.quaternion[0]) * ratio,
        left_pose.quaternion[1] + (right_pose.quaternion[1] - left_pose.quaternion[1]) * ratio,
        left_pose.quaternion[2] + (right_pose.quaternion[2] - left_pose.quaternion[2]) * ratio,
        left_pose.quaternion[3] + (right_pose.quaternion[3] - left_pose.quaternion[3]) * ratio
    ]
    return pose

# 获取世界坐标系到车坐标系的转换矩阵
def get_world2CarRT(pose, gnss2CarRT):

    quat = np.quaternion(pose.quaternion[0], pose.quaternion[1], pose.quaternion[2], pose.quaternion[3])
    rMat = quaternion.as_rotation_matrix(quat)

    sin_lon = sin(radians(pose.longitude))
    cos_lon = cos(radians(pose.longitude))
    sin_lat = sin(radians(pose.latitude))
    cos_lat = cos(radians(pose.latitude))
    data = np.array([
        [-sin_lon, -sin_lat * cos_lon, cos_lat * cos_lon, pose.px],
        [cos_lon, -sin_lat * sin_lon, cos_lat * sin_lon, pose.py],
        [0, cos_lat, sin_lat, pose.pz],
        [0, 0, 0, 1]
    ])

    # enu2Ecef = cv2.Mat(4, 4, cv2.CV_64F, data)
    # data 是一个包含16个元素的列表或numpy数组
    data = np.array(data).reshape(4, 4)
    # 创建一个4x4的矩阵，数据类型为float64，并用data填充
    enu2Ecef = np.array(data, dtype=np.float64)
    gnss2Enu = np.eye(4, dtype=np.float64)
    for i in range(3):
        for j in range(3):
            gnss2Enu[i, j] = rMat[i, j]

    gnss2Ecef = np.dot(enu2Ecef, gnss2Enu)
    ecef2GnssRT = np.linalg.inv(gnss2Ecef)
    world2CarRT = np.dot(gnss2CarRT, ecef2GnssRT)
    if print_switch:
        print("quat:")
        print(quat)
        print("rMat:")
        print(rMat)
        print("data:")
        print(data)
        print("enu2Ecef:")
        print(enu2Ecef)
        print("gnss2Enu:")
        print(gnss2Enu)
        print("gnss2Ecef:")
        print(gnss2Ecef)
        print("ecef2GnssRT:")
        print(ecef2GnssRT)
    return world2CarRT

# WGS84坐标系转换为ECEF坐标系
def wgs84_to_ecef(lng, lat, height) -> tuple:
    lng_radian = radians(lng)
    lat_radian = radians(lat)
    return wgs84_to_ecef_radian(lng_radian, lat_radian, height)

# WGS84坐标系转换为ECEF坐标系（弧度）
def wgs84_to_ecef_radian(lng_radian, lat_radian, height) -> tuple:
    # WGS84椭球模型参数  
    a = 6378137.0  # 长半轴，单位：米  
    f = 1 / 298.257223563  # 扁率  
    e2 = 2 * f - f ** 2  # 第一偏心率平方  
    b = a * (1 - f)  # 短半轴，单位：米
    n = a / sqrt(1 - e2 * sin(lat_radian) ** 2) # 卯酉圈曲率半径  
    x = (n + height) * cos(lat_radian) * cos(lng_radian)
    y = (n + height) * cos(lat_radian) * sin(lng_radian)
    z = ((1 - e2) * n + height) * sin(lat_radian)
    return x, y, z

# 世界坐标系转换为车坐标系
def world_to_car(pose, world2CarRT) -> np.ndarray:
    result = np.dot(world2CarRT, np.array([pose.px, pose.py, pose.pz, 1]))
    return result

# 世界坐标系转换为车坐标系
def world_to_car_transform(pose, gnss2CarRT) -> np.ndarray:
    world2CarRT = get_world2CarRT(pose, gnss2CarRT)
    return world_to_car(pose, world2CarRT)

# test-1
# timestamp = 1716778967600.0
# lng_lat_height = [113.4341019044475,
#                     23.041318448487875,
#                     11.8094]
# clip_path = "/Users/admin/Downloads/marker-test/GACRT015_1716778965(1)"
# gnss2CarRT = get_gnss2CarRT(clip_path)
# ego_poses = read_txt_to_ego_poses(clip_path)
# pose = interpolate_poses(ego_poses, timestamp)
# world2CarRT = get_world2CarRT(pose, gnss2CarRT)
# xyz = wgs84_to_ecef(lng_lat_height[0], lng_lat_height[1], lng_lat_height[2])
# result = np.dot(world2CarRT, np.array([xyz[0], xyz[1], xyz[2], 1]))
# print(result)

# if print_switch:
#     print("world2CarRT:")
#     print(world2CarRT)
#     print("lng_lat_height:")
#     print(lng_lat_height)
#     print("ecef_xyz:")
#     print(xyz)
#     print("result:")
#     print(result)

# test-2
# timestamp = 1720159304000
# clip_path = "/Users/admin/Downloads/marker-test/GACRT015_1720159303"
# gnss2CarRT = get_gnss2CarRT(clip_path)
# ego_poses = read_txt_to_ego_poses(clip_path)
# results = []
# pose = interpolate_poses(ego_poses, timestamp)
# world2CarRT = get_world2CarRT(pose, gnss2CarRT)
# for ego_pose in ego_poses:
#     # timestamp = ego_pose.timestamp
#     # pose = interpolate_poses(ego_poses, timestamp)
#     pose = ego_pose
#     results.append(np.dot(world2CarRT, np.array([pose.px, pose.py, pose.pz, 1])))
# # print to csv
# with open(clip_path + "/result.csv", "w") as f:
#     f.write("x,y,z\n")
#     for result in results:
#         f.write(f"{result[0]},{result[1]},{result[2]}\n")

