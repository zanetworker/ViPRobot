__author__ = 'zanetworker'


import os
import json

def get_parent_dir_location():
    src_dir = os.path.dirname(__file__)
    parent_dir = os.path.split(src_dir)[0]
    return parent_dir

def get_file_dir_location(file_dir):
    return os.path.join(get_parent_dir_location(), file_dir)

def get_file_location(file_dir, filename):
    return os.path.join(get_file_dir_location(file_dir), filename)


def log_this (module_name, message_to_log, object_to_log=""):
    print '[', module_name, ']', ": ", message_to_log,
    print object_to_log


def write_to_file(file_directory, destination_file, value_to_write):

    with open(get_file_location(file_directory, destination_file), 'a+') as file:
        if check_empty_file(file_directory, destination_file):
            log_this(__name__, "Token Already Created, reading token value..!!")
            file_content = file.read()
            return file_content
        else:
            file.write(value_to_write + '\n')
            return ''

def read_file(file_directory, destination_file):
    with open(get_file_location(file_directory, destination_file), 'r') as file:
        file_content = file.read()
        return file_content


def check_empty_file(file_directory, file_to_check):
    return True if os.path.getsize(get_file_location(file_directory, file_to_check)) else False


def convert_dict_to_json(dict_to_convert):
    return json.dumps(dict_to_convert, ensure_ascii=False)