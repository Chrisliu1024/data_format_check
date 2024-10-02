# Description: This file contains simple check functions that are used to check the validity of the attributes of a marker_4d element

# Check if an element has a specific attribute
def check_attribute_existence(element, attribute_name):
    return attribute_name in element

# Check if the specific attribute value is not empty or None
def check_attribute_value_existence(element, attribute_name):
    return True if element.get(attribute_name) is not None and element.get(attribute_name) != "" else False

# Check if the specific attribute value of a element is unique in the element list
def check_attribute_value_is_unique(element, attribute_name, element_list):
    return True if [e.get(attribute_name) for e in element_list].count(element.get(attribute_name)) == 1 else False

# Check if the specific attribute value is a valid integer
def check_attribute_value_is_integer(element, attribute_name):
    try:
        int(element.get(attribute_name))
        return True
    except ValueError:
        return False
    
# Check if the specific attribute value is a valid enum
def check_attribute_value_in_enum(element, attribute_name, enum_values):
    return True if element.get(attribute_name) in enum_values else False

# Check if the points(with visiable) attribute of a element is valid
# example of valid points attribute: "[[x, y, z, visiable], [x, y, z, visiable]]"
def check_points_visiable_attribute_style_valid(element, attribute_name):
    points = element.get(attribute_name)
    # check if the points attribute is a list
    if not isinstance(points, list):
        return False
    # check if the points attribute is not empty
    if not points:
        return False
    # check if the points attribute is a list of list
    for point in points:
        if not isinstance(point, list):
            return False
        if len(point) != 4:
            return False
    
    return True

# Check if the points attribute of a element is valid
# example of valid points attribute: "[[x, y, z], [x, y, z]]"
def check_points_attribute_style_valid(element, attribute_name):
    points = element.get(attribute_name)
    # check if the points attribute is a list
    if not isinstance(points, list):
        return False
    # check if the points attribute is not empty
    if not points:
        return False
    # check if the points attribute is a list of list
    for point in points:
        if not isinstance(point, list):
            return False
        if len(point) != 3:
            return False
    
    return True

# Check if the orientation vector attribute of a element is valid
# example of valid orientation attribute: "[[x1, y1, z1],[x2, y2, z2]]"
def check_orientation_vector_attribute_style_valid(element, attribute_name):
    orientation = element.get(attribute_name)
    # check if the orientation attribute is a list
    if not isinstance(orientation, list):
        return False
    # check if the orientation attribute is not empty
    if not orientation:
        return False
    # check if the length of orientation vector is 2
    if len(orientation) != 2:
        return False
    # check if the orientation attribute is a list of list
    for point in orientation:
        if not isinstance(point, list):
            return False
        if len(point) != 3:
            return False
    
    return True