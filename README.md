# Sonar Data Reader

The Sonar Data Reader is a Python module designed to extract, process, visualize, and save sonar data stored in binary
files. This module provides functionalities to easily work with sonar data collected from underwater surveys,
experiments, or similar applications.

## Installation

To use the Sonar Data Reader, follow these steps:

1. Clone the repository to your local machine


2. Install the required dependencies:

### pip

```sh
$ pip install bluerobotics-ping --upgrade
```
## Required Libraries

Before running the code, make sure you have the following Python libraries installed:

```python
# pathlib
# cv2
# numpy
# matplotlib
# re
# struct
# psutil
```

## Usage

### Initializing the Reader

The primary script processes log files located in the input directory and outputs processed data and images in the output directory. Below is a brief overview of how the provided code works.

```python
from PingViewerReader.src.Render import Render
from Reader import Reader

# Make Reader to parse logs in 'input' folder
reader = Reader(f"../input")

# Save output of parser in 'output' folder as .npy file
reader.save_data(f"output")

# Sonar view of third (index = 2) log file
reader.sonar_view(2)

# Render class for making images of output file
Render(matrix_path='../output/output.npy', mode='rgb').run()

```

---

### Visualizing Sonar Data

You can visualize sonar data using the sonar_view method. Provide the index of the file you want to visualize.

```pycon
reader.sonar_view(0)
```

---

### Saving Processed Data

Processed data can be saved to a file using the save_data method. Specify the desired output file name.

```pycon
reader.save_data(f"output")
```

---

### Making Images

Processed data then can be rendered to images based on output matrix with 'Render' class

```pycon
Render(matrix_path='../output/output.npy', mode='rgb').run()
```

---

### Examples

Check out the provided examples to see the Sonar Data Reader in action:

`/PingViewrReader/src/example.py` : Demonstrates basic usage of the Reader and Render classes.

---

## Customization

The Reader class allows for customization through parameters:

samples_count: Number of samples per ping message (default: 1200).
reading_angle: Angle for reading data from ping messages (default: 90).
memory_monitor_flag: Flag to enable memory monitoring (default: False).
Additional Functionalities
The module also provides additional functionalities such as:

Extracting custom samples from input data using extract_custom_samples.
Advanced visualization capabilities with the _SonarView class.

#### The library is ready to use: `import brping`. If you would like to use the command line [examples](/examples) or [tools](/tools) provided by this package, follow the notes in python's [installing to user site](https://packaging.python.org/tutorials/installing-packages/#installing-to-the-user-site) directions (eg `export PATH=$PATH:~/.local/bin`).

---
