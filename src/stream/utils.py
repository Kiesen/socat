# -*- coding: utf-8 -*-
"""
Utilities module of the stream package.

Contains most of the I/O functionality for the
streamer classes.
"""
import os
import json
from sys import stdout


def print_initial_info(path):
    print("\nStart streaming social media entries")
    print("----------------------------------------------------")
    print(
        "\nRecived entries getting written to: %s\n"
        % path
    )


def print_summary(elapsed_time, recived_data):
    print(
        "\n\nTotal runtime: %s\nTotal amount of entries: %d\n\n"
        % (elapsed_time, recived_data)
    )


def print_info(recived_data):
    print(
        "Entries recieved: %d"
        % recived_data,
        end='\r'
    )
    stdout.flush()


def set_output_path(path, rel_dir_path):
    if path is not None:
        path = path + rel_dir_path
    else:
        path = '.' + rel_dir_path

    if not os.path.exists(path):
        os.makedirs(path)
    return path


def data_to_json(path, json_data):
    with open(path, "w") as f:
        f.write(json.dumps(json_data))


def data_from_json(path):
    data = []
    with open(path) as f:
        data = json.load(f)
    return data
