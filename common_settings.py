import os

# attribute settings
id_attribute_name = 'id'
points_attribute_name = 'points'
class_attribute_name = 'class'
orientation_attribute_name = 'orientation'
# layer settings
arrow_layer_name = 'arrow'
crosswalk_layer_name = 'crosswalk'
curb_layer_name = 'curb'
deceleration_line_layer_name = 'deceleration_line'
deceleration_zone_layer_name = 'deceleration_zone'
lane_layer_name = 'lane'
special_points_layer_name = 'special_points'
stop_line_layer_name = 'stop_line'
# input or output file settings
# input_ins_file_sub_path = '/ego_raw/ins_traj.csv'
# input_gps_msg_file_sub_path = '/cloud_las/gps_msg.txt'
pose_sub_path = "/ego_raw/IE_post_traj.asc"
pose_output_sub_path = "/ego_raw/pose_traj.csv"
# if the system is Windows, assemble the path with '\\'
if os.name == 'nt':
    pose_sub_path = pose_sub_path.replace('/', '\\')
    pose_output_sub_path = pose_output_sub_path.replace('/', '\\')
output_result_detail_file_name = 'error_detail_log.csv'
output_result_sum_file_name = 'error_sum_log.csv'

# os settings
split_str = '/'
# if the os is windows, change the split_str to '\\'
if os.name == 'nt':
    split_str = '\\'

# remove buffer meter
buffer_meter = 0.8