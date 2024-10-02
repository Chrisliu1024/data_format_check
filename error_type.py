from enum import Enum
# Enum for error types, with an attribute to record error description, group_index to record the error group
class ErrorType(Enum):
    SELF_CUSOMIZED = -1 # 自定义错误类型
    JSON_FORMAT_INVALID = 0
    ATTRIBUTE_NOT_EXISTENCE = 1
    ATTRIBUTE_NOT_EMPTY = 2
    ATTRIBUTE_VALUE_NOT_UNIQUE = 3
    ATTRIBUTE_POINTS_VALUE_INVALID = 4
    ATTRIBUTE_NOT_INTEGER = 5
    ATTRIBUTE_NOT_IN_ENUM = 6
    ATTRIBUTE_ORIENTATION_VECTOR_VALUE_INVALID= 7
    TOPOLOGY_ERROR = 8
    ORIENTATION_ERROR = 9

    @staticmethod
    def getErrorGroupList():
        return ['格式完整性错误', '字段完整性错误', '属性完整性错误', 'ID唯一性错误', '拓扑正确性错误', '朝向正确性错误', '未划分错误类型']


# type：0 格式完整性错误 1 字段完整性错误, 2 属性完整性错误, 3 ID唯一性错误, 4 拓扑正确性错误, 5 朝向正确性错误  
# Error type for json format invalid
ErrorType.JSON_FORMAT_INVALID.detail_description = '[{}]: json format is invalid'
ErrorType.JSON_FORMAT_INVALID.description = '文件的json格式错误'
ErrorType.JSON_FORMAT_INVALID.group_index = 0
# Error type for attribute not existence
ErrorType.ATTRIBUTE_NOT_EXISTENCE.detail_description = '[{}]{}.{}: attribute[{}] is not exist'
ErrorType.ATTRIBUTE_NOT_EXISTENCE.description = '字段{}缺失'
ErrorType.ATTRIBUTE_NOT_EXISTENCE.group_index = 1 
# Error type for attribute value is not empty or None
ErrorType.ATTRIBUTE_NOT_EMPTY.detail_description = '[{}]{}.{}: attribute[{}] is not empty or None'
ErrorType.ATTRIBUTE_NOT_EMPTY.description = '字段{}不能为空'
ErrorType.ATTRIBUTE_NOT_EMPTY.group_index = 2
# Error type for attribute value not unique
ErrorType.ATTRIBUTE_VALUE_NOT_UNIQUE.detail_description = '[{}]{}.{}: attribute[{}] value is not unique'
ErrorType.ATTRIBUTE_VALUE_NOT_UNIQUE.description = '字段{}不唯一'
ErrorType.ATTRIBUTE_VALUE_NOT_UNIQUE.group_index = 3
# Error type for [points] attribute value is valid
ErrorType.ATTRIBUTE_POINTS_VALUE_INVALID.detail_description = '[{}]{}.{}: attribute[{}] value is invalid'
ErrorType.ATTRIBUTE_POINTS_VALUE_INVALID.description = '字段{}的值不合法'
ErrorType.ATTRIBUTE_POINTS_VALUE_INVALID.group_index = 2
# Error type for attribute not integer
ErrorType.ATTRIBUTE_NOT_INTEGER.detail_description = '[{}]{}.{}: attribute[{}] is not integer'
ErrorType.ATTRIBUTE_NOT_INTEGER.description = '字段{}不是整数'
ErrorType.ATTRIBUTE_NOT_INTEGER.group_index = 2
# Error type for attribute not in enum list
ErrorType.ATTRIBUTE_NOT_IN_ENUM.detail_description = '[{}]{}.{}: attribute[{}] is not in enum value list'
ErrorType.ATTRIBUTE_NOT_IN_ENUM.description = '字段{}不在枚举值列表'
ErrorType.ATTRIBUTE_NOT_IN_ENUM.group_index = 2
# Error type for attribute orientation vector value is invalid
ErrorType.ATTRIBUTE_ORIENTATION_VECTOR_VALUE_INVALID.detail_description = '[{}]{}.{}: attribute[{}] value is invalid'
ErrorType.ATTRIBUTE_ORIENTATION_VECTOR_VALUE_INVALID.description = '字段{}的值不合法'
ErrorType.ATTRIBUTE_ORIENTATION_VECTOR_VALUE_INVALID.group_index = 5
# Error type for topology error
ErrorType.TOPOLOGY_ERROR.detail_description = '[{}]{}.{}: topology is error'
ErrorType.TOPOLOGY_ERROR.description = '拓扑错误'
ErrorType.TOPOLOGY_ERROR.group_index = 4
# Error type for orientation error
ErrorType.ORIENTATION_ERROR.detail_description = '[{}]{}.{}: orientation is error'
ErrorType.ORIENTATION_ERROR.description = '朝向错误'
ErrorType.ORIENTATION_ERROR.group_index = 5