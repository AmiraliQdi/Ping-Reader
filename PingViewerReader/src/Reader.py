import os
import numpy as np

import Helper
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
        self.memory_monitor = Helper.MemoryMonitor()

    def start(self):
        self.memory_monitor.start()
        try:
            self.print_file_list()
            self.extract_data()
            self.process_data()
            self.print_main_matrix_shape()
        except KeyboardInterrupt:
            self.memory_monitor.stop()
            self.memory_monitor.join()

    def list_files_in_folder(self):
        print("Addressed files...")
        file_addresses = []
        for root, dirs, files in os.walk(self.__folder_path):
            for file in files:
                if file.endswith(".bin"):
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
            if self.__is_data_corrupted(log, file_index, file):
                continue
            self.__files_data[file] = []
            for index, (timestamp, decoded_message) in enumerate(log.parser()):
                self.__files_data[file].append(decoded_message)
            print(f"{file_index}| {file} read successfully ({len(self.__files_data[file])} ping messages)")

    def __is_data_corrupted(self, log, file_index, file):
        for index, (timestamp, decoded_message) in enumerate(log.parser()):
            if len(decoded_message.data) != self.__samples_count:
                print(
                    f"\033[91m{file_index}| {file} corrupted (sample_count::{len(decoded_message.data)}!={self.__samples_count})\033[0m")
                return True

    def process_data(self):
        print("Processing...")
        for file_index, (key, value) in enumerate(self.__files_data.items()):
            self.__extract_example(key, value, file_index)
        self.reshape_main_matrix()

    def __extract_example(self, file, ping_messages, file_index, example_limit=-1):
        examples_count = int(len(ping_messages) / self.__reading_angle)
        if example_limit == -1 or example_limit > examples_count:
            example_limit = examples_count
        if examples_count < 1:
            print(f"{file_index} | {0} examples processed!")
            return
        for i in range(example_limit):
            for j in range(self.__reading_angle):
                self.__extract_values_from_messages(file_index, ping_messages[j + (i * self.__reading_angle)])
        print(f"{file_index} | {example_limit} examples processed successfully")

    def __extract_values_from_messages(self, file_index, message):
        if len(message.data) != self.__samples_count:
            raise Exception(
                f"{file_index}| file is corrupted (wrong sample count:{len(message.data)} != {self.__samples_count})")
        for value in message.data:
            self.__main_matrix.append(value)

    def print_main_matrix_shape(self):
        print(np.array(self.__main_matrix).shape)

    def reshape_main_matrix(self):
        print(np.array(self.__main_matrix).shape)
        self.__main_matrix = np.reshape(self.__main_matrix, (-1, self.__samples_count * self.__reading_angle))


reader = Reader("../Ping-360")
reader.start()
