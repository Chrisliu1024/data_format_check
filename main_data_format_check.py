import os
import json
import sys
import ast
import tarfile
import math
from error_log import ErrorLog
from error_type import ErrorType
from point_element import PointElement
from compose_check_functions import *
from asc2utmpose import save_to_pose_csv
from common_settings import *
from crs_transform import *
from angle import *
from shapely.geometry import Point

# global settings
wgs84_crs = False

# Handle the arrow element
def handle_arrow(element, element_list, layer_name) -> list:
    error_log_list = []
    # handle the common attribute(id, points, class)
    append_list_to_list(handle_common_attribute(element, element_list, layer_name), error_log_list)
    # check the existence of vertices attribute
    attribute_name = 'vertices'
    append_to_list(check_points_attribute_existence_and_valid(element, layer_name, attribute_name), error_log_list)
    # check the existence of subclass attribute and in enum values
    attribute_name = 'subclass'
    append_to_list(check_attribute_existence_and_not_empty(element, layer_name, attribute_name), error_log_list)
    # enum_values = ['straight', 'left', 'right', 'uturn', 'straight_left', 'straight_right', 'straight_uturn', 'left_uturn', 'left_right', 'left_diversion', 'right_diversion', 'no_uturn', 'no_left', 'no_right', 'left_straight_right']
    # append_to_list(check_attribute_existence_and_in_enum(element, layer_name, attribute_name, enum_values), error_log_list)
    return error_log_list

# Handle the crosswolk element
def handle_crosswalk(element, element_list, layer_name) -> list:
    error_log_list = []
    # handle the common attribute(id, points, class)
    append_list_to_list(handle_common_attribute(element, element_list, layer_name), error_log_list)
    # check the existence of orientation attribute and in enum values
    attribute_name = 'orientation'
    append_to_list(check_orientation_vector_attribute_existence_and_valid(element, layer_name, attribute_name), error_log_list)
    return error_log_list

# Handle the curb element
def handle_curb(element, element_list, layer_name) -> list:
    error_log_list = []
    # handle the common attribute(id, points, class)
    append_list_to_list(handle_common_attribute(element, element_list, layer_name), error_log_list)
    # check the existence of predecessor attribute and not empty
    attribute_name = 'predecessor'
    append_to_list(check_attribute_existence_and_not_empty(element, layer_name, attribute_name), error_log_list)
    # check the existence of successor attribute and not empty
    attribute_name = 'successor'
    append_to_list(check_attribute_existence_and_not_empty(element, layer_name, attribute_name), error_log_list)
    # check the existence of subclass attribute and in enum values
    attribute_name = 'subclass'
    append_to_list(check_attribute_existence_and_not_empty(element, layer_name, attribute_name), error_log_list)
    # enum_values = ['curb', 'barrier', 'movable']
    # append_to_list(check_attribute_existence_and_in_enum(element, layer_name, attribute_name, enum_values), error_log_list)
    # check the existence of orientation attribute and in enum values
    attribute_name = 'orientation'
    enum_values = [False]
    append_to_list(check_attribute_existence_and_in_enum(element, layer_name, attribute_name, enum_values), error_log_list)
    return error_log_list

# Handle the lane element
def handle_lane(element, element_list, layer_name) -> list:
    error_log_list = []
    # handle the common attribute(id, points, class)
    append_list_to_list(handle_common_attribute(element, element_list, layer_name), error_log_list)
    # check the existence of predecessor attribute and not empty
    attribute_name = 'predecessor'
    append_to_list(check_attribute_existence_and_not_empty(element, layer_name, attribute_name), error_log_list)
    # check the existence of successor attribute and not empty
    attribute_name = 'successor'
    append_to_list(check_attribute_existence_and_not_empty(element, layer_name, attribute_name), error_log_list)
    # check the existence of dashtype attribute and in enum values
    attribute_name = 'dashtype'
    append_to_list(check_attribute_existence_and_not_empty(element, layer_name, attribute_name), error_log_list)
    # enum_values = ['dash', 'solid']
    # append_to_list(check_attribute_existence_and_in_enum(element, layer_name, attribute_name, enum_values), error_log_list)
    # check the existence of subclass attribute and in enum values
    attribute_name = 'subclass'
    append_to_list(check_attribute_existence_and_not_empty(element, layer_name, attribute_name), error_log_list)
    # enum_values = ['double_solid', 'double_dash', 'solid_dash', 'dash_solid', 'waiting', 'directing', 'thick', 'thickdash', 'fishbone', 'variable', 'distance', 'other']
    # append_to_list(check_attribute_existence_and_in_enum(element, layer_name, attribute_name, enum_values), error_log_list)
    # check the existence of color attribute and in enum values
    attribute_name = 'color'
    append_to_list(check_attribute_existence_and_not_empty(element, layer_name, attribute_name), error_log_list)
    # enum_values = ['white', 'yellow', 'red', 'orange', 'other']
    # append_to_list(check_attribute_existence_and_in_enum(element, layer_name, attribute_name, enum_values), error_log_list)
    # check the existence of orientation attribute and in enum values
    attribute_name = 'orientation'
    enum_values = [True, False]
    append_to_list(check_attribute_existence_and_in_enum(element, layer_name, attribute_name, enum_values), error_log_list)
    return error_log_list

# Handle the deceleration_line element
def handle_deceleration_line(element, element_list, layer_name) -> list:
    error_log_list = []
    # handle the common attribute(id, points, class)
    append_list_to_list(handle_common_attribute(element, element_list, layer_name), error_log_list)
    # check the existence of orientation attribute and in enum values
    attribute_name = 'orientation'
    append_to_list(check_orientation_vector_attribute_existence_and_valid(element, layer_name, attribute_name), error_log_list)
    return error_log_list

# Handle the deceleration_zone element
def handle_deceleration_zone(element, element_list, layer_name) -> list:
    error_log_list = []
    # handle the common attribute(id, points, class)
    append_list_to_list(handle_common_attribute(element, element_list, layer_name), error_log_list)
    # check the existence of orientation attribute and in enum values
    attribute_name = 'orientation'
    append_to_list(check_orientation_vector_attribute_existence_and_valid(element, layer_name, attribute_name), error_log_list)
    return error_log_list

# Handle the special_points element
def handle_special_points(element, element_list, layer_name) -> list:
    error_log_list = []
    # handle the common attribute(id, points, class)
    append_list_to_list(handle_common_attribute(element, element_list, layer_name), error_log_list)
    # check the existence of type attribute and in enum values
    attribute_name = 'type'
    append_to_list(check_attribute_existence_and_not_empty(element, layer_name, attribute_name), error_log_list)
    # enum_values = ['color_change', 'type_change', 'affiliated', 'merge', 'split', 'join', 'division']
    # append_to_list(check_attribute_existence_and_in_enum(element, layer_name, attribute_name, enum_values), error_log_list)
    return error_log_list

# Handle the stop_line element
def handle_stop_line(element, element_list, layer_name) -> list:
    error_log_list = []
    # handle the common attribute(id, points, class)
    append_list_to_list(handle_common_attribute(element, element_list, layer_name), error_log_list)
    # check the existence of subclass attribute and in enum values
    attribute_name = 'subclass'
    append_to_list(check_attribute_existence_and_not_empty(element, layer_name, attribute_name), error_log_list)
    # enum_values = ['solid', 'dash', 'other']
    # append_to_list(check_attribute_existence_and_in_enum(element, layer_name, attribute_name, enum_values), error_log_list)
    return error_log_list

# Handle the topology of lane and special_points
def handle_topology_lane_special_points(data, lane_layer_name, special_points_layer_name) -> list:
    lane_elements = data.get(lane_layer_name)
    special_points_elements = data.get(special_points_layer_name)
    error_log_list = []
     # store the start and point list
    start_end_point_list = []
    # store the special points list
    special_points_list = []
    # check if the elements exist
    if lane_elements:
        # loop
        for lane_element in lane_elements:
            points_list = lane_element.get(points_attribute_name)
            if points_list == None or len(points_list) == 0:
                continue
            # start point of the lane
            start_point = Point(points_list[0][0:3])
            start_end_point_list.append(PointElement(start_point, lane_element))
            # end point of the lane
            end_point = Point(points_list[-1][0:3])
            start_end_point_list.append(PointElement(end_point, lane_element))
    if special_points_elements:
        # loop
        for special_points_element in special_points_elements:
            points_list = special_points_element.get(points_attribute_name)
            if points_list:
                for point in points_list:
                    special_point = Point(point[0:3])
                    special_points_list.append(PointElement(special_point, special_points_element))
    # check the topology of lane and special_points
    for start_end_point_element in start_end_point_list:
        # create 2cm buffer
        start_end_point_buffer = start_end_point_element.point.buffer(get_crs_distance(0.02))
        # check if the start_end_point_buffer intersects with other start_end_point
        intersert_lane_points_list = []
        intersert_special_points_list = []
        for other_start_end_point_element in start_end_point_list:
            if start_end_point_element.element.get(id_attribute_name) != other_start_end_point_element.element.get(id_attribute_name):
                if start_end_point_buffer.intersects(other_start_end_point_element.point):
                    intersert_lane_points_list.append(other_start_end_point_element)
        if len(intersert_lane_points_list) > 0:
            # check if the start_end_point_buffer intersects with special_points
            for special_points_element in special_points_list:
                if start_end_point_buffer.intersects(special_points_element.point):
                    intersert_special_points_list.append(special_points_element)
            # if not intersect with special_points, record the error log
            if len(intersert_special_points_list) == 0:
                # stringfy the intersert_lane_points_list
                points_str = ''
                for intersert_lane_point in intersert_lane_points_list:
                    points_str += intersert_lane_point.point.wkt
                    if intersert_lane_point != intersert_lane_points_list[-1]:
                        points_str += ','
                # customised error message
                ErrorType.SELF_CUSOMIZED.description = ErrorType.TOPOLOGY_ERROR.description + ", 错误点: " + points_str
                ErrorType.SELF_CUSOMIZED.group_index = ErrorType.TOPOLOGY_ERROR.group_index
                error_log_list.append(ErrorLog(lane_layer_name, other_start_end_point_element.element.get(id_attribute_name), points_attribute_name, ErrorType.SELF_CUSOMIZED, other_start_end_point_element.element))
        else:
            # check if the start_end_point_buffer intersects with special_points
            for special_points_element in special_points_list:
                if start_end_point_buffer.intersects(special_points_element.point):
                    intersert_special_points_list.append(special_points_element)
            # if intersect with lane, record the error log
            if len(intersert_special_points_list) > 0:
               # stringfy the intersert_special_points_list
                points_str = ''
                for intersert_special_point in intersert_special_points_list:
                    points_str += intersert_special_point.point.wkt
                    if intersert_special_point != intersert_special_points_list[-1]:
                        points_str += ','
                # customised error message
                ErrorType.SELF_CUSOMIZED.description = ErrorType.TOPOLOGY_ERROR.description + ", 错误点: " + points_str
                ErrorType.SELF_CUSOMIZED.group_index = ErrorType.TOPOLOGY_ERROR.group_index
                error_log_list.append(ErrorLog(lane_layer_name, other_start_end_point_element.element.get(id_attribute_name), points_attribute_name, ErrorType.SELF_CUSOMIZED, other_start_end_point_element.element))
    return error_log_list

# Handle the orientation vector
def handle_orientation_vector(data, track_point_list, layer_name, timestamp, gnss2CarRT) -> list:
    elements = data.get(layer_name)
    if not elements:
        return []
    error_log_list = []
    # check the orientation vector of the element
    for element in elements:
        append_to_list(check_orientation_vector_valid(element, layer_name, points_attribute_name, orientation_attribute_name, track_point_list, timestamp, gnss2CarRT), error_log_list)
    return error_log_list

# Handle the line orientation vector
def handle_line_orientation_vector(data, track_point_list, layer_name, timestamp, gnss2CarRT) -> list:
    elements = data.get(layer_name)
    if not elements:
        return []
    error_log_list = []
    # check the orientation vector of the element
    for element in elements:
        append_to_list(check_line_vector_valid(element, layer_name, points_attribute_name, orientation_attribute_name, track_point_list, timestamp, gnss2CarRT), error_log_list)
    return error_log_list

# Handle the corsswalk orientation vector
def handle_crosswalk_orientation_vector(data, layer_name) -> list:
    elements = data.get(layer_name)
    if not elements:
        return []
    error_log_list = []
    # check the orientation vector of the element
    for element in elements:
        append_to_list(check_crosswalk_orientation_vector_valid(element, layer_name, points_attribute_name, orientation_attribute_name), error_log_list)
    return error_log_list

# Handle the orientation vector of an element
def check_orientation_vector_valid(element, layer_name, points_attribute_name, orientation_attribute_name, track_point_list, timestamp, gnss2CarRT) -> ErrorLog:
    # get the orientation vector of the element
    orientation_array = element.get(orientation_attribute_name)
    if orientation_array == None or len(orientation_array) != 2:
        return None
    orientation_points = []
    for orientation in orientation_array:
        orientation_points.append(Point(orientation[0:3]))
    orientation_vector = Point(orientation_points[-1].x - orientation_points[0].x, orientation_points[-1].y - orientation_points[0].y)
    # get the points of the element
    points_array = element.get(points_attribute_name)
    if points_array == None or len(points_array) < 2:
        return None
    points = []
    for point in points_array:
        points.append(Point(point[0:3]))
    # get the the start point
    first_point = points[0]
    # get the last point
    if len(points) > 2:
        last_point = points[-2]
    else:
        last_point = points[-1]
    if first_point == last_point:
        return None
    if timestamp == None:
        # get the track orientation vector of the element
        track_orientation_vector = get_nearest_vector_with_global_coordinate(first_point, track_point_list)
    else:
        track_orientation_vector = get_nearest_vector_with_car_coordinate(track_point_list, timestamp, gnss2CarRT)
    # calulate the angle of the track vector and the orientation vector
    angle = get_angle_of_two_vectors(track_orientation_vector, orientation_vector)
    abs_angle = abs(math.degrees(angle))
    # if the angle is greater than 45 degrees, record the error message
    if abs_angle > 45:
        return ErrorLog(layer_name, element.get(id_attribute_name), orientation_attribute_name, ErrorType.ORIENTATION_ERROR, element)

# Handle the crosswalk orientation vector
def check_crosswalk_orientation_vector_valid(element, layer_name, points_attribute_name, orientation_attribute_name) -> ErrorLog:
    # get the orientation vector of the element
    orientation_array = element.get(orientation_attribute_name)
    if orientation_array == None or len(orientation_array) != 2:
        return None
    orientation_points = []
    for orientation in orientation_array:
        orientation_points.append(Point(orientation[0:3]))
    orientation_vector = Point(orientation_points[-1].x - orientation_points[0].x, orientation_points[-1].y - orientation_points[0].y)
    # get the points of the element
    points_array = element.get(points_attribute_name)
    if points_array == None or len(points_array) < 4:
        return None
    points = []
    for point in points_array:
        points.append(Point(point[0:3])) 
    # devide the points into sub_point_list
    point_list = []
    sub_point_list = []
    first_point = points[0]
    mid_point = points[1]
    sub_point_list.append(first_point)
    sub_point_list.append(mid_point)
    point_list.append(sub_point_list)
    # loop, devide the points into sub_point_list, with the angle between the two vectors less than 15 degrees
    for i in range(len(points) - 2):
        first_point = points[i]
        mid_point = points[i + 1]
        last_point = points[i + 2]
        first_line_vector = Point(mid_point.x - first_point.x, mid_point.y - first_point.y)
        second_line_vector = Point(last_point.x - mid_point.x, last_point.y - mid_point.y)
        angle = get_angle_of_two_vectors(first_line_vector, second_line_vector)
        abs_angle = abs(math.degrees(angle))
        if abs_angle <= 15:
            sub_point_list.append(last_point)
        else:
            sub_point_list = []
            sub_point_list.append(mid_point)
            sub_point_list.append(last_point)
            point_list.append(sub_point_list)
    # get the lengthest line
    max_length = 0
    max_start_point = None
    max_end_point = None
    for sub_point_list in point_list:
        start_point = sub_point_list[0]
        end_point = sub_point_list[-1]
        length = start_point.distance(end_point)
        if length > max_length:
            max_length = length
            max_start_point = start_point
            max_end_point = end_point
    # get the vector of the lengthest line
    line_vector = Point(max_end_point.x - max_start_point.x, max_end_point.y - max_start_point.y)
    # calculate the angle of the line vector and the orientation vector
    angle = get_angle_of_two_vectors(line_vector, orientation_vector)
    abs_angle = abs(math.degrees(angle))
    # if the angle is not greater than 45 degrees and less than 135, record the error message
    if abs_angle < 45 or abs_angle > 135:
        return ErrorLog(layer_name, element.get(id_attribute_name), orientation_attribute_name, ErrorType.ORIENTATION_ERROR, element)

# Handle the line vector of an element
def check_line_vector_valid(element, layer_name, points_attribute_name, orientation_attribute_name, track_point_list, timestamp, gnss2CarRT) -> ErrorLog:
    # get the points of the element
    points_array = element.get(points_attribute_name)
    if points_array == None or len(points_array) < 2:
        return None
    points = []
    for point in points_array:
        points.append(Point(point[0:3]))
    
    result = None
    # loop the second to last point
    for i in range(1, len(points)):
        # get the the start point
        first_point = points[i - 1]
        # get the point
        last_point = points[i]
        if timestamp == None:
            # get the track orientation vector of the element
            track_orientation_vector = get_nearest_vector_with_global_coordinate(first_point, track_point_list)
        else:
            track_orientation_vector = get_nearest_vector_with_car_coordinate(track_point_list, timestamp, gnss2CarRT)
        # get the vector of the element
        line_vector = Point(last_point.x - first_point.x, last_point.y - first_point.y)
        # get the angle of the track vector and the orientation vector
        angle = get_angle_of_two_vectors(track_orientation_vector, line_vector)
        abs_angle = abs(math.degrees(angle))
        # if the angle is greater than 45 degrees, record the error message
        if abs_angle > 45:
            # return and break
            result = ErrorLog(layer_name, element.get(id_attribute_name), orientation_attribute_name, ErrorType.ORIENTATION_ERROR, element)
            break
    return result

# Get the vector of the two points in the car coordinate   
def get_nearest_vector_with_car_coordinate(ego_points, timestamp, gnss2CarRT):
    poses_in_range = find_poses_in_range(ego_points, timestamp)
    if len(poses_in_range) != 2:
        poses_in_range_near = find_poses_near(ego_points, timestamp)
        new_poses_in_range = [poses_in_range[0], poses_in_range_near[-1]]
    else:
        new_poses_in_range = poses_in_range
    # transform to car coordinate
    world2CarRT = get_world2CarRT(new_poses_in_range[0], gnss2CarRT)
    for i in range(len(new_poses_in_range)):
        car_xyz = world_to_car(new_poses_in_range[i], world2CarRT)
        new_poses_in_range[i] = EgoPose( new_poses_in_range[i].timestamp, car_xyz[0], car_xyz[1], car_xyz[2])
    return Point(new_poses_in_range[1].longitude - new_poses_in_range[0].longitude, new_poses_in_range[1].latitude - new_poses_in_range[0].latitude)

# Get the nearest point of the point list
def get_nearest_vector_with_global_coordinate(point, ego_points) -> Point:
    nearest_point = None
    min_distance = sys.maxsize
    for p in ego_points:
        distance = point.distance(Point(p.longitude, p.latitude, p.height))
        if distance < min_distance:
            min_distance = distance
            nearest_point = p
    poses_in_range_near = find_poses_near(ego_points, nearest_point.timestamp)
    return Point(poses_in_range_near[-1].longitude - nearest_point.longitude, poses_in_range_near[-1].latitude - nearest_point.latitude)

# Get the nearest point of the point list
def get_nearest_point(point, ego_points) -> Point:
    nearest_point = None
    min_distance = sys.maxsize
    for p in ego_points:
        distance = point.distance(Point(p.longitude, p.latitude, p.height))
        if distance < min_distance:
            min_distance = distance
            nearest_point = p
    return nearest_point

# Get the distance in crs
def get_crs_distance(distance) -> float:
    return meter_to_degree(distance) if wgs84_crs else distance

# Meter to degree
def meter_to_degree(meter):
    return meter / 111195.077837585166667

# Remove the list with the same error_file_path, error_id and error_description
def remove_same_error_file_path_and_error_id_and_error_description(error_log_list) -> list:
    error_id_description_list = []
    error_log_list_new = []
    for error_log in error_log_list:
        error_id_description = error_log.error_file_path + str(error_log.error_id) + error_log.error_description
        if error_id_description not in error_id_description_list:
            error_id_description_list.append(error_id_description)
            error_log_list_new.append(error_log)
    return error_log_list_new

# Store the error log to a csv file with layer level aggregation
def store_error_sum_log_to_csv_file_level(error_log_list, root_folder_path):
    # According to the file_path, error_layer, error_type of error, aggregate the num of errors
    error_sum_log_num_layer = {}
    for error in error_log_list:
        if error.error_file_path in error_sum_log_num_layer:
            if error.error_layer in error_sum_log_num_layer[error.error_file_path]:
                if error.error_type in error_sum_log_num_layer[error.error_file_path][error.error_layer]:
                    error_sum_log_num_layer[error.error_file_path][error.error_layer][error.error_type] += 1
                else:
                    error_sum_log_num_layer[error.error_file_path][error.error_layer][error.error_type] = 1
            else:
                error_sum_log_num_layer[error.error_file_path][error.error_layer] = {}
                error_sum_log_num_layer[error.error_file_path][error.error_layer][error.error_type] = 1
        else:
            error_sum_log_num_layer[error.error_file_path] = {}
            error_sum_log_num_layer[error.error_file_path][error.error_layer] = {}
            error_sum_log_num_layer[error.error_file_path][error.error_layer][error.error_type] = 1

    # Output the sum of the error logs to a csv file named 'error_sum_log.csv'
    with open(root_folder_path + '/error_sum_log.csv', 'w') as f:
        # write the header
        f.write('文件路径,图层名,')
        error_group = ErrorType.getErrorGroupList()
        for layer_name in range(len(error_group)):
            f.write(error_group[layer_name])
            if layer_name != len(error_group) - 1:
                f.write(',')
        f.write('\n')
        # write the error log num
        for file_path in error_sum_log_num_layer:
            for layer_name in error_sum_log_num_layer[file_path]:
                f.write(file_path + ',')
                f.write(layer_name + ',')
                for j in range(len(error_group)):
                    if j in error_sum_log_num_layer[file_path][layer_name]:
                        if error_sum_log_num_layer[file_path][layer_name][j] > 0: 
                            f.write('1')
                    else:
                        f.write('0')
                    if j != len(error_group) - 1:
                        f.write(',')
                f.write('\n')        
        f.close()

# Store the error log to a csv file with id level aggregation
def store_error_sum_log_to_csv_id_level(error_log_list, root_folder_path):
    # According to the file_path, error_layer, str(error_element), error_type of error, aggregate the num of errors
    error_sum_log_num_layer = {}
    for error in error_log_list:
        if error.error_file_path in error_sum_log_num_layer:
            if error.error_layer in error_sum_log_num_layer[error.error_file_path]:
                if str(error.error_element) in error_sum_log_num_layer[error.error_file_path][error.error_layer]:
                    if error.error_type in error_sum_log_num_layer[error.error_file_path][error.error_layer][str(error.error_element)]:
                        error_sum_log_num_layer[error.error_file_path][error.error_layer][str(error.error_element)][error.error_type] += 1
                    else:
                        error_sum_log_num_layer[error.error_file_path][error.error_layer][str(error.error_element)][error.error_type] = 1
                else:
                    error_sum_log_num_layer[error.error_file_path][error.error_layer][str(error.error_element)] = {}
                    error_sum_log_num_layer[error.error_file_path][error.error_layer][str(error.error_element)][error.error_type] = 1
            else:
                error_sum_log_num_layer[error.error_file_path][error.error_layer] = {}
                error_sum_log_num_layer[error.error_file_path][error.error_layer][str(error.error_element)] = {}
                error_sum_log_num_layer[error.error_file_path][error.error_layer][str(error.error_element)][error.error_type] = 1
        else:
            error_sum_log_num_layer[error.error_file_path] = {}
            error_sum_log_num_layer[error.error_file_path][error.error_layer] = {}
            error_sum_log_num_layer[error.error_file_path][error.error_layer][str(error.error_element)] = {}
            error_sum_log_num_layer[error.error_file_path][error.error_layer][str(error.error_element)][error.error_type] = 1

    # Output the sum of the error logs to a csv file named 'error_sum_log.csv'
    with open(root_folder_path + split_str + output_result_sum_file_name, 'w') as f:
        # write the header
        f.write('批次名,Clip名,帧名,图层名,ID,')
        error_group = ErrorType.getErrorGroupList()
        for layer_name in range(len(error_group)):
            f.write(error_group[layer_name])
            f.write(',')
        f.write('问题feature(无ID时)')
        f.write('\n')
        # split the last folder of root_folder_path as the batch name
        root_folder_path_list = root_folder_path.split(split_str)
        batch_name = root_folder_path_list[-1]
        # write the error log num
        for file_path in error_sum_log_num_layer:
            # file_path - root_folder_path, and split the first folder as the clip name
            clip_name = file_path.replace(root_folder_path, '')
            clip_name_list = clip_name.split(split_str)
            clip_name = clip_name_list[1]
            # split the last folder of file path as the frame name
            frame_name = clip_name_list[-1]
            for layer_name in error_sum_log_num_layer[file_path]:
                for error_element_str in error_sum_log_num_layer[file_path][layer_name]:
                    f.write(batch_name + ',')
                    f.write(clip_name + ',')
                    f.write(frame_name + ',')
                    f.write(layer_name + ',')
                    element_id = get_error_id(error_element_str)
                    if element_id:
                        f.write( "=\"" + str(element_id) +  "\"" + ',')
                    else:
                        f.write(',')
                    for j in range(len(error_group)):
                        if j in error_sum_log_num_layer[file_path][layer_name][error_element_str]:
                            if error_sum_log_num_layer[file_path][layer_name][error_element_str][j] > 0: 
                                f.write('1')
                        else:
                            f.write('0')
                        if j != len(error_group) - 1:
                            f.write(',')
                    if element_id == None:
                        f.write(',"' + error_element_str + '"')
                    f.write('\n')        
        f.close()

# Get the error id from the element
def get_error_id(element):
    # check if the element is not None or 'None'
    if element and element != 'None':
        try:
            # convert the element to a dictionary
            element_dict = ast.literal_eval(element)
            return element_dict.get('id')
        except json.JSONDecodeError:
            # if the element is not a JSON string, return None
            return None
    else:
        return None

# Print the log with loguru or python print
def customize_print(log):
    try:
        from loguru import logger
    except ImportError:
        logger = None
    if logger:
        logger.info(log)
    else:
        # python print
        print(log)

# Handle the common attribute
def handle(data, layer_name, error_log_list, file_path, handle_function):
    elements = data.get(layer_name)
    # check if the elements exist
    if elements:
        # loop
        for element in elements:
            # handle the element
            error_log_list_layer = handle_function(element, elements, layer_name)
            # complete the file path of the error log and append to the error log list
            complete_file_path_and_append_to_list(error_log_list_layer, error_log_list, file_path)
    else:
        # customize_print('No [%s] elements in the file[%s]' % (layer_name, file_path))
        pass

# Append file path to the error result list
def complete_file_path_and_append_to_list(error_log_list_layer, error_log_list, file_path):
    if len(error_log_list_layer) == 0:
        return
    for error in error_log_list_layer:
        error.error_file_path = file_path
    append_list_to_list(error_log_list_layer, error_log_list)

# Get all files in the folder with the specified suffix
def get_all_files(folder_path, suffix):
    # Get all files in the folder with the specified suffix
    files = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith(suffix):
                files.append(os.path.join(dirpath, filename))
    return files

# Remove the points in the XX meter buffer of the first point
def remove_points_in_frist_buffer(ego_points, buffer_distance):
    if len(ego_points) == 0:
        return ego_points
    # create a buffer
    frist_point = Point(ego_points[0].longitude, ego_points[0].latitude, ego_points[0].height)
    buffer = frist_point.buffer(buffer_distance)
    # remove the points in the buffer
    points_new = []
    for ego_point in ego_points:
        point = Point(ego_point.longitude, ego_point.latitude, ego_point.height)
        if not buffer.contains(point):
            points_new.append(ego_point)
    return points_new

# Main entrance
def main_entrance(root_folder_path, complex_check_switch = True, print_error_log = True):
    # store the error log
    error_log_list = []
    # extract the files in the folder
    tar_files = get_all_files(root_folder_path, '.tar')
    # Extract the tar files to the same folder
    for tar_file in tar_files:
        # if there is the same name folder, delete it
        if os.path.exists(root_folder_path + split_str + tar_file.split(split_str)[-1].split('.')[0]):
            os.system('rm -rf ' + root_folder_path + split_str + tar_file.split(split_str)[-1].split('.')[0])
        # Use tarfile module to extract tar files
        with tarfile.open(tar_file, 'r|*') as tar:
            # get exception info
            try: 
                tar.extractall(root_folder_path)
                customize_print(f'Extracted {tar_file} to {root_folder_path}')
            except Exception as e:
                customize_print(f'Error extracting {tar_file}: {e}')

    track_point_list = None
    track_idx = None
    root_backup = None
    # Loop through all the files and directory in the folder
    for root, dirs,files in os.walk(root_folder_path):
        if complex_check_switch:
            # construct the track point list and spatial index
            # if root path not contains root_backup path 
            if root_backup == None or (root_backup not in root):
                # if the IE_post_traj.asc file exists
                if os.path.exists(root + pose_sub_path) and not os.path.exists(root + pose_output_sub_path):
                    save_to_pose_csv(root)
                # if the pose_traj.csv file exists, read the file to create a point list
                if os.path.exists(root + pose_output_sub_path):
                    gnss2CarRT = get_gnss2CarRT(root)
                    track_point_list = read_txt_to_ego_poses(root)
                    # handle the case that the track_point_list with error start track
                    track_point_list = remove_points_in_frist_buffer(track_point_list, meter_to_degree(buffer_meter))
                    root_backup = root
        # Loop through all the files in the folder
        for file in files:
            # skip files that are not JSON files or start with '.'(the hidden files in Mac OS)
            if (not file.endswith('.json')) or file.startswith('.'):
                continue
            file_path = os.path.join(root, file)
            # print file path
            customize_print(file_path)
            # check the JSON file name equals to 'lb_all.json'
            global wgs84_crs
            if file == 'lb_all.json':
                wgs84_crs = True
                timestamp = None
            else:
                wgs84_crs = False
                # clip the timestamp from the file name, example: lb_1716778977399000000_50_120.json
                file_name_list = file.split('_')
                if len(file_name_list) != 4:
                    continue
                timestamp = int(file_name_list[1])/1000000
            # open the file and load the JSON data
            with open(file_path, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    customize_print('Invalid JSON format')
                    error_log_list.append(ErrorLog('file', '', '', ErrorType.JSON_FORMAT_INVALID, None, file_path))
                    continue
                # if the data is not a dictionary, skip
                if not isinstance(data, dict):
                    continue
                # handle arrow
                handle(data, arrow_layer_name, error_log_list, file_path, handle_arrow)
                # handle crosswalk
                handle(data, crosswalk_layer_name, error_log_list, file_path, handle_crosswalk)
                # handle curb
                handle(data, curb_layer_name, error_log_list, file_path, handle_curb)
                # handle deceleration_line
                handle(data, deceleration_line_layer_name, error_log_list, file_path, handle_deceleration_line)
                # handle deceleration_zone
                handle(data, deceleration_zone_layer_name, error_log_list, file_path, handle_deceleration_zone)
                # handle lane
                handle(data, lane_layer_name, error_log_list, file_path, handle_lane)
                # handle special_points
                handle(data, special_points_layer_name, error_log_list, file_path, handle_special_points)
                # handle stop_line
                handle(data, stop_line_layer_name, error_log_list, file_path, handle_stop_line)
                if complex_check_switch:
                    # handle the topology of lane and special_points
                    error_log_list_lane_topology = handle_topology_lane_special_points(data, lane_layer_name, special_points_layer_name)
                    complete_file_path_and_append_to_list(error_log_list_lane_topology, error_log_list, file_path)
                    # handle the orientation vector of deceleration_line
                    error_log_list_orientation_line = handle_orientation_vector(data, track_point_list, deceleration_line_layer_name, timestamp, gnss2CarRT)
                    complete_file_path_and_append_to_list(error_log_list_orientation_line, error_log_list, file_path)
                    # handle the orientation vector of  deceleration_zone
                    error_log_list_orientation_zone = handle_orientation_vector(data, track_point_list, deceleration_zone_layer_name, timestamp, gnss2CarRT)
                    complete_file_path_and_append_to_list(error_log_list_orientation_zone, error_log_list, file_path)
                    # handle the orientation vector of croasswalk
                    error_log_list_orientation_crosswalk = handle_crosswalk_orientation_vector(data, crosswalk_layer_name)
                    complete_file_path_and_append_to_list(error_log_list_orientation_crosswalk, error_log_list, file_path)
                    # handle the line vector of lane
                    error_log_list_line_lane = handle_line_orientation_vector(data, track_point_list, lane_layer_name, timestamp, gnss2CarRT)
                    complete_file_path_and_append_to_list(error_log_list_line_lane, error_log_list, file_path)

    # remove the duplicate error log, with the same error_file_path, error_id and error_description
    error_log_list = remove_same_error_file_path_and_error_id_and_error_description(error_log_list)

    # print all the error logs
    if(print_error_log):
        customize_print('Error log list:')
        # store the error log to a file
        with open(root_folder_path + split_str + output_result_detail_file_name, 'w') as f:
            # write header
            f.write('文件路径,批次名,Clip名,帧名,图层名,ID,属性名,错误描述,问题feature(无ID时)\n')
            # batch name
            root_folder_path_list = root_folder_path.split(split_str)
            batch_name = root_folder_path_list[-1]
            # loop
            for error in error_log_list:
                description_cn = error.error_description.format(error.error_attribute)
                detail_description = '[{}]{}.{}: ' + description_cn
                customize_print(detail_description.format(error.error_file_path, error.error_layer, error.error_id, error.error_attribute))
                # clip name
                clip_name = error.error_file_path.replace(root_folder_path, '')
                clip_name_list = clip_name.split(split_str)
                clip_name = clip_name_list[1]
                # frame name
                frame_name = clip_name_list[-1]
                row = error.error_file_path + ',' + batch_name + ',' + clip_name + ',' + frame_name + ',' + error.error_layer + ',' + "=\"" + str(error.error_id) +  "\"" + ',' + error.error_attribute + ',' + description_cn + ','
                if error.error_id == None:
                    # to string and to lower case
                    element_str = str(error.error_element).lower();
                    f.write(row + str('"' + element_str + '"') + '\n')
                else:
                    f.write(row + '\n')
            f.close()
    # store the error log to a csv file
    store_error_sum_log_to_csv_id_level(error_log_list, root_folder_path)

# Get parameters from the command line
if __name__ == '__main__':
    if len(sys.argv) == 2:
        root_folder_path = sys.argv[1]
        main_entrance(root_folder_path)
    elif len(sys.argv) == 3:
        root_folder_path = sys.argv[1]
        print_error_switch = sys.argv[2]
        main_entrance(root_folder_path, print_error_switch)
    else:
        customize_print('Please input the root folder path')
        customize_print('Usage: python main_marker_4d_check.py root_folder_path comple_check_switch print_error_switch')
        customize_print('Example(Linux/Mac): python main_marker_4d_check.py /Users/admin/Downloads/marker-test True')
        customize_print('Example(Linux/Mac): python main_marker_4d_check.py /Users/admin/Downloads/marker-test True False')
        customize_print('Example(Windows): python main_marker_4d_check.py C:\\Users\\admin\\Downloads\\marker-test True')
        customize_print('Example(Windows): python main_marker_4d_check.py C:\\Users\\admin\\Downloads\\marker-test True False')
        sys.exit(1)

# Test
# root_folder_path = '/Users/admin/Downloads/marker-test'
# main_entrance(root_folder_path)
# main_entrance(root_folder_path, False)