# Introduction

Check if the JSON data format meets the required specifications.

Note: This check involves multiple coordinate system transformations, such as conversions between global and local coordinate systems.

# How to use

Prerequisite: Python 3 environment

```SHELL
python main_data_format_check.py root_folder_path
```

Example(Linux/Mac): python main_data_format_check.py /Users/admin/Downloads/marker-test
Example(Linux/Mac): python main_data_format_check.py /Users/admin/Downloads/marker-test True
Example(Linux/Mac): python main_data_format_check.py /Users/admin/Downloads/marker-test True False
Example(Windows): python main_data_format_check.py C:\\Users\\admin\\Downloads\\marker-test
Example(Windows): python main_data_format_check.py C:\\Users\\admin\\Downloads\\marker-test True
Example(Windows): python main_data_format_check.py C:\\Users\\admin\\Downloads\\marker-test True False

# Dependency package installation
```SHE
pip install scipy
pip install geos
pip install shapely
pip install pyproj
pip install numpy-quaternion
```