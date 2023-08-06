import os


def get_path():
    current_path = os.path.abspath(__file__)
    father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    so_path = os.path.join(father_path, 'cfunction.so')
    return so_path

