import pybind

def open_slide(path:str, driver:str):
    return pybind.open_slide(path, driver)

def get_driver_ids():
    return pybind.get_driver_ids()