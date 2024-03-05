import os

import numpy as np

from PingViewerReader.PingDecoder import PingViewerLogReader


class Reader:

    def __init__(self, folder_path):
        self.__folder_path = folder_path
        self.__files_address = self.list_files_in_folder()
        self.__main_matrix = []
        self.__files_data = {}
        self.__files_count = len(self.__files_address)
        self.__samples_count = 1200
        self.__reading_angle = 90

    def list_files_in_folder(self):
        print("Addressed files...")
        file_addresses = []
        for root, dirs, files in os.walk(self.__folder_path):
            for file in files:
                file_address = os.path.join(root, file)
                file_addresses.append(file_address)
        return file_addresses

    def print_file_list(self):
        for (index, file) in enumerate(self.__files_address):
            print(f"{index}| {file}")

    def extract_data(self):
        print("Extracting from all files...")
        for (file_index, file) in enumerate(self.__files_address):
            log = PingViewerLogReader(str(file))
            self.__files_data[file] = []
            for index, (timestamp, decoded_message) in enumerate(log.parser()):
                self.__files_data[file].append(decoded_message)
            print(f"{file_index}| {file} read successfully ({len(self.__files_data[file])} ping messages)")

    def process_data(self):
        print("Processing...")
        for key, value in self.__files_data.items():
            for index, ping_message in enumerate(value):
                for intensity in ping_message.data:
                    self.__main_matrix.append(intensity)
                if index == self.__reading_angle - 1:
                    print(f"Angle limit reached ({len(value) - index} ping messages ignored)")
                    break
            print(f"{key} file's data processed successfully")
        self.reshape_main_matrix()

    def print_main_matrix_shape(self):
        print(np.array(self.__main_matrix).shape)

    def reshape_main_matrix(self):
        self.__main_matrix = np.reshape(self.__main_matrix, (-1, self.__samples_count * self.__reading_angle))


reader = Reader("../input")
reader.print_file_list()
reader.extract_data()
reader.process_data()
reader.print_main_matrix_shape()
