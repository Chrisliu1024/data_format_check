# Description: This file contains the functions to check the common attributes of the 4D marker layers
from error_log import ErrorLog
from error_type import ErrorType
from simple_check_functions import *
from common_settings import *

# Check if the specific attribute exists and is not empty
def check_attribute_existence_and_not_empty(element, layer_name, attribute_name) -> ErrorLog:
    if not check_attribute_existence(element, attribute_name):
        # record the error message
        return ErrorLog(layer_name, element.get(id_attribute_name), attribute_name, ErrorType.ATTRIBUTE_NOT_EXISTENCE, element)
    else:
        # check the class attribute is not empty or None
        if not check_attribute_value_existence(element, attribute_name):
            # record the error message
            return ErrorLog(layer_name, element.get(id_attribute_name), attribute_name, ErrorType.ATTRIBUTE_NOT_EMPTY, element)

# Check if the specific attribute is existence, not empty and unique
def check_attribute_existence_and_not_empty_and_unique(element, layer_name, attribute_name, element_list) -> ErrorLog:
    if not check_attribute_existence(element, attribute_name):
        # record the error message
        return ErrorLog(layer_name, element.get(id_attribute_name), attribute_name, ErrorType.ATTRIBUTE_NOT_EXISTENCE, element)
    else:
        # check the class attribute is not empty or None
        if not check_attribute_value_existence(element, attribute_name):
            # record the error message
            return ErrorLog(layer_name, element.get(id_attribute_name), attribute_name, ErrorType.ATTRIBUTE_NOT_EMPTY, element)
        else:
            # check the class attribute is unique
            if not check_attribute_value_is_unique(element, attribute_name, element_list):
                # record the error message
                return ErrorLog(layer_name, element.get(id_attribute_name), attribute_name, ErrorType.ATTRIBUTE_VALUE_NOT_UNIQUE, element)

# Check if the specific attribute exists and is in the enum values
def check_attribute_existence_and_in_enum(element, layer_name, attribute_name, enum_values) -> ErrorLog:
    if not check_attribute_existence(element, attribute_name):
        # record the error message
        return ErrorLog(layer_name, element.get(id_attribute_name), attribute_name, ErrorType.ATTRIBUTE_NOT_EXISTENCE, element)
    else:
        # check the class attribute is in enum value list
        if not check_attribute_value_in_enum(element, attribute_name, enum_values):
            # customised error message
            ErrorType.SELF_CUSOMIZED.description = ErrorType.ATTRIBUTE_NOT_IN_ENUM.description + str(enum_values)
            ErrorType.SELF_CUSOMIZED.group_index = ErrorType.ATTRIBUTE_NOT_IN_ENUM.group_index
            # record the error message
            return ErrorLog(layer_name, element.get(id_attribute_name), attribute_name, ErrorType.SELF_CUSOMIZED, element)

# Check if the points(with visiable) attribute of an element exists and is valid
def check_points_visiable_attribute_existence_and_valid(element, layer_name, attribute_name) -> ErrorLog:
    if not check_attribute_existence(element, attribute_name):
        # record the error message
        return ErrorLog(layer_name, element.get(id_attribute_name), attribute_name, ErrorType.ATTRIBUTE_NOT_EXISTENCE, element)
    else:
        # check the points attribute is valid
        if not check_points_visiable_attribute_style_valid(element, attribute_name):
            # record the error message
            return ErrorLog(layer_name, element.get(id_attribute_name), attribute_name, ErrorType.ATTRIBUTE_POINTS_VALUE_INVALID, element)

# Check if the points attribute of an element exists and is valid
def check_points_attribute_existence_and_valid(element, layer_name, attribute_name) -> ErrorLog:
    if not check_attribute_existence(element, attribute_name):
        # record the error message
        return ErrorLog(layer_name, element.get(id_attribute_name), attribute_name, ErrorType.ATTRIBUTE_NOT_EXISTENCE, element)
    else:
        # check the points attribute is valid
        if not check_points_attribute_style_valid(element, attribute_name):
            # record the error message
            return ErrorLog(layer_name, element.get(id_attribute_name), attribute_name, ErrorType.ATTRIBUTE_POINTS_VALUE_INVALID, element)

# Check if the orientation vector attribute of an element exists and is valid
def check_orientation_vector_attribute_existence_and_valid(element, layer_name, attribute_name) -> ErrorLog:
    if not check_attribute_existence(element, attribute_name):
        # record the error message
        return ErrorLog(layer_name, element.get(id_attribute_name), attribute_name, ErrorType.ATTRIBUTE_NOT_EXISTENCE, element)
    else:
        # check the orientation attribute is valid
        if not check_orientation_vector_attribute_style_valid(element, attribute_name):
            # record the error message
            return ErrorLog(layer_name, element.get(id_attribute_name), attribute_name, ErrorType.ATTRIBUTE_ORIENTATION_VECTOR_VALUE_INVALID, element)

# Append to a list
def append_to_list(element, element_list):
    if element:
        element_list.append(element)
    
def append_list_to_list(element_list, total_element_list):
    total_element_list.extend(element_list)

def handle_common_attribute(element, element_list, layer_name) -> list:
    error_log_list = []
    # check the existence of id attribute
    attribute_name = id_attribute_name
    append_to_list(check_attribute_existence_and_not_empty_and_unique(element, layer_name, attribute_name, element_list), error_log_list)
    # check the existence of points attribute and valid
    attribute_name = points_attribute_name
    if layer_name in [lane_layer_name, curb_layer_name]:
        append_to_list(check_points_visiable_attribute_existence_and_valid(element, layer_name, attribute_name), error_log_list)
    else:
        append_to_list(check_points_attribute_existence_and_valid(element, layer_name, attribute_name), error_log_list)
    # check the existence of class attribute and in enum values
    attribute_name = class_attribute_name
    enum_values = [layer_name]
    append_to_list(check_attribute_existence_and_in_enum(element, layer_name, attribute_name, enum_values), error_log_list)
    return error_log_list
