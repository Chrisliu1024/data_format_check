import numpy as np
from datetime import datetime, timedelta
import math
from pyproj import Proj, Transformer
from scipy.spatial.transform import Rotation as R
from common_settings import pose_sub_path, pose_output_sub_path

# 定义表头
header = 'timestamp,latitude,longitude,height,roll,pitch,heading,utm_x,utm_y,utm_z,euler_roll,euler_pitch,euler_yaw, quaternion_w, quaternion_x, quaternion_y, quaternion_z'

# 0-360 转为-pi到pi
def heading_to_azimuth(heading):
    if heading <= 270:
        azimuth = 90 - heading
    
    if heading > 270:
        azimuth = 450 - heading
    azimuth_rad = math.radians(azimuth)
    return azimuth_rad

def heading_to_azimuth_degree(heading):
    if heading <= 270:
        azimuth = 90 - heading
    
    if heading > 270:
        azimuth = 450 - heading
    return azimuth

def latlon_to_utm(latitude, longitude, altitude):
    # 定义UTM投影
    utm_zone = int((longitude + 180) / 6) + 1  # 自动计算UTM区
    proj_utm = Proj(proj='utm', zone=utm_zone, ellps='WGS84')

    # 创建一个WGS84和UTM之间的Transformer
    transformer = Transformer.from_crs("epsg:4326", proj_utm.srs)

    # 转换到UTM坐标
    utm_x, utm_y = transformer.transform(latitude, longitude)
    utm_z = altitude  # 海拔值无需转换

    return utm_x, utm_y, utm_z

def extract_data(input_file):
    data = []
    with open(input_file, 'r') as infile:
        count = 0
        for line in infile:
            try:
                # 分割行，以使用分号将其划分为两部分
                fine_part, ins_part = line.split(';')
                
                # FINESTEERING部分提取第4、5个字段
                fine_fields = fine_part.split(',')
                gps_week = fine_fields[5]
                week_seconds = fine_fields[6]
                timestamp = gps_to_unix_timestamp(int(gps_week), float(week_seconds))
                # 转换为整数
                timestamp = int(timestamp * 1000)

                ins_fields = ins_part.split(',')
                latitude = ins_fields[2]
                longitude = ins_fields[3]
                height = ins_fields[4]
                roll = ins_fields[9]
                pitch = ins_fields[10]
                heading = ins_fields[11]
                
                euler_roll = math.radians(float(roll))
                euler_pitch = math.radians(float(pitch))
                euler_yaw = heading_to_azimuth(float(heading))

                # phi = 0.20000000298023224  # 绕Z轴旋转（yaw）
                # theta =0.10000000149011612  # 绕Y轴旋转（pitch）
                # psi = 0.30000001192092896  # 绕X轴旋转（roll）
                azimuth = heading_to_azimuth_degree(float(heading))
                euler = [float(roll), -float(pitch), azimuth]
                r = R.from_euler('xyz', euler, degrees=True)
                # 欧拉角转换为四元数
                quaternion = r.as_quat()

                utm_x,utm_y,utm_z = latlon_to_utm(float(latitude),float(longitude),float(height))

                # 将所有提取的字段合并为一个列表
                data.append([timestamp, latitude, longitude, height, roll, pitch, heading, utm_x, utm_y, utm_z, euler_roll, euler_pitch, euler_yaw, quaternion[3], quaternion[0], quaternion[1], quaternion[2]])
            except Exception as e:
                print(f"Error processing line: {line}\n{e}")
    return data

def gps_to_unix_timestamp(gps_week, gps_seconds):
    # GPS基准时间 1980年1月6日
    gps_epoch = datetime(1980, 1, 6)
    seconds = int(gps_seconds)
    milliseconds = int((gps_seconds*1000 - seconds*1000))
    
    # GPS时间 = GPS基准时间 + GPS周数 * 7天 + 周内秒
    gps_time = gps_epoch + timedelta(weeks=gps_week, seconds=seconds, milliseconds=milliseconds)
    
    # 将datetime对象转换为UNIX时间戳
    unix_timestamp = float(gps_time.timestamp()) + 8 * 3600 -18
    return unix_timestamp

def save_to_pose_csv(root_path):
    # 提取数据
    data = extract_data(root_path + pose_sub_path)
    # 将数据转换为NumPy数组
    data_array = np.array(data)
    # 保存为带表头的NumPy文件
    np.savetxt(root_path + pose_output_sub_path, data_array, delimiter=',', header=header, comments='', fmt='%s')

# 文件路径定义
# pose_file = "/Users/admin/Downloads/marker-test/GACRT015_1720159303/ego_raw/IE_post_traj.asc"
# output_folder = "/Users/admin/Downloads/marker-test/GACRT015_1720159303/ego_raw/test_pose.csv"
# test
# save_to_pose_csv("/Users/admin/Downloads/marker-test/GACRT015_1720159303")