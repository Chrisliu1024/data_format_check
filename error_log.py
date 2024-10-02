# Error log class
class ErrorLog:
    error_layer = ''
    error_id = ''
    error_attribute = ''
    error_description = ''
    error_type = ''

    def __init__(self, error_layer, error_id, error_attribute, error_type, error_element=None, error_file_path=''):
        # Error layer is the layer where the error occurred
        self.error_layer = error_layer
        # Error id is the id of element where the error occurred
        self.error_id = error_id
        # Error attribute is the attribute of the element where the error occurred
        self.error_attribute = error_attribute
        # Error description is the description of the error
        self.error_description = error_type.description
        # Error type is the type of the error
        self.error_type = error_type.group_index
        # Error element is the element where the error occurred
        self.error_element = error_element
        # Error file path is the file where the error occurred
        self.error_file_path = error_file_path

# example
# [file_name]lane.123: attribute 'name' is not exist