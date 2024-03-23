import os
from pathlib import Path
import cv2
import numpy as np
import Helper  # Importing Helper module for utility functions and classes


class Reader:
    def __init__(self, folder_path, samples_count=1200, reading_angle=90, memory_monitor_flag=False):
        """Initialize Reader object.

        Parameters:
        - folder_path (str): Path to the folder containing binary files.
        - samples_count (int): Number of samples per ping message.
        - reading_angle (int): Angle for reading data from ping messages.
        - memory_monitor_flag (bool): Flag indicating whether memory monitoring is enabled.
        """
        self.__folder_path = folder_path
        self.__files_address = self.list_files_in_folder()
        self.__main_matrix = []
        self.__files_data = {}
        self.__files_count = len(self.__files_address)
        self.__samples_count = samples_count
        self.__reading_angle = reading_angle
        self.memory_monitor = Helper.MemoryMonitor()  # Memory monitor object
        self.__mem_monitor_flag = memory_monitor_flag
        self.__viewer = _SonarView()  # SonarView object for visualizing data
        if self.__mem_monitor_flag:
            self.memory_monitor.start()  # Start memory monitoring
        self.print_file_list()
        self.extract_data()
        self.process_data()
        self.reshape_main_matrix()
        self.print_main_matrix_shape()

    def save_data(self, save_as):
        """Save main matrix data to a file.

        Parameters:
        - save_as (str): Name for the output file.
        """
        self.save_main_matrix(save_as)

    def list_files_in_folder(self):
        """List all files with '.bin' extension in the specified folder."""
        print("Addressed files...")
        file_addresses = []
        for root, dirs, files in os.walk(self.__folder_path):
            # Ignore directories with the name "corrupted"
            dirs[:] = [d for d in dirs if d.lower() != 'corrupted']

            for file in files:
                if file.endswith(".bin"):
                    file_address = os.path.join(root, file)
                    file_addresses.append(file_address)
        return file_addresses

    def print_file_list(self):
        """Print the list of files found in the folder."""
        for (index, file) in enumerate(self.__files_address):
            print(f"{index}| {file}")

    def extract_data(self):
        """Extract data from all files."""
        print("Extracting from all files...")
        for (file_index, file) in enumerate(self.__files_address):
            log = Helper.PingViewerLogReader(str(file))
            if self.__is_data_corrupted(log, file_index, file):
                continue
            self.__files_data[file] = []
            for index, (timestamp, decoded_message) in enumerate(log.parser()):
                self.__files_data[file].append(decoded_message)
            print(f"{file_index}| {file} read successfully ({len(self.__files_data[file])} ping messages)")

    def __is_data_corrupted(self, log, file_index, file):
        """Check if the data in a file is corrupted."""
        for index, (timestamp, decoded_message) in enumerate(log.parser()):
            if len(decoded_message.data) != self.__samples_count:
                print(
                    f"\033[91m{file_index}| {file} corrupted (sample_count::{len(decoded_message.data)}!="
                    f"{self.__samples_count})\033[0m")
                return True

    def process_data(self):
        """Process the extracted data."""
        print("Processing...")
        for file_index, (key, value) in enumerate(self.__files_data.items()):
            self.__extract_example(key, value, file_index)

    def __extract_example(self, file, ping_messages, file_index, example_limit=-1):
        """Extract example data from ping messages."""
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
        """Extract values from ping messages."""
        if len(message.data) != self.__samples_count:
            raise Exception(
                f"{file_index}| file is corrupted (wrong sample count:{len(message.data)} != {self.__samples_count})")
        for value in message.data:
            self.__main_matrix.append(value)

    def save_main_matrix(self, output_name):
        """Save the main matrix data to a file."""
        print("Saving output matrix...")
        outfile = Path("../output") / Path(output_name).with_suffix(".npy")
        np.save(outfile, self.__main_matrix)
        print("Saved successfully")

    def print_main_matrix_shape(self):
        """Print the shape of the main matrix."""
        print(np.array(self.__main_matrix).shape)
        print(f"Extracted {np.array(self.__main_matrix).shape[0]} examples from files")

    def reshape_main_matrix(self, output_form=3):
        """Reshape the main matrix."""
        print("Reshaping main matrix...")
        if output_form == 3:
            self.__main_matrix = np.reshape(self.__main_matrix, (-1, self.__reading_angle, self.__samples_count))
        elif output_form == 2:
            self.__main_matrix = np.reshape(self.__main_matrix, (-1, self.__reading_angle * self.__samples_count))

    def sonar_view(self, file_index):
        """Visualize sonar data from a file."""
        file_name = list(self.__files_data.keys())[file_index]
        messages = self.__files_data[file_name]
        file_name_without_extension = os.path.splitext(os.path.basename(file_name))[0]
        self.__viewer.view(messages, file_name_without_extension)


# noinspection PyShadowingNames
def extract_custom_samples(input_data, indexing):
    """Extract custom samples from input data."""
    output_data = []
    for i in range(len(input_data) // indexing):
        temp_list = 0
        for j in range(indexing):
            temp_list += input_data[j + (i * indexing)]
        temp_list //= indexing
        output_data.append(temp_list)
    return output_data


class _SonarView:
    def __init__(self, length=640, step=1):
        """Initialize SonarView object."""
        self.__image_length = length
        self.__image = np.zeros((self.__image_length, self.__image_length, 1), np.uint8)
        self.__max_range = 80 * 200 * 1450 / 2
        self.__step = step
        self.__current_angle = 0

    def view(self, ping_messages, file_name):
        """View sonar data."""
        print(f"making image for '{file_name}' with len {len(ping_messages)}")
        for decoded_message in ping_messages:
            data = np.frombuffer(decoded_message.data, dtype=np.uint8)
            data_lst = extract_custom_samples(data, 1)  # default value for indexing is 1
            center = (self.__image_length / 2, self.__image_length / 1)
            linear_factor = len(data_lst) / center[0]
            for i in range(int(center[0])):
                if i < center[0] * self.__max_range / self.__max_range:
                    point_color = data_lst[int(i * linear_factor - 1)]
                else:
                    point_color = 0
                for k in np.linspace(0, self.__step, 8 * self.__step):
                    self.__image[int(center[0] + i * np.cos(2 * np.pi * (self.__current_angle + k) / 400)), int(
                        center[1] + i * np.sin(2 * np.pi * (self.__current_angle + k) / 400)), 0] = point_color
            self.__current_angle = (self.__current_angle + self.__step) % 400
            cv2.imshow(f"file name: {file_name}", self.__image)
            cv2.waitKey(25)



