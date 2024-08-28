from PingViewerReader.src.Render import Render
from Reader import Reader

# Make Reader to parse logs in 'input' folder
reader = Reader(f"../input")

# Save out of parser in 'output' folder as .npy file
reader.save_data(f"output")

# Sonar view of third ( index = 2) log file
reader.sonar_view(2)

# Render class for making images of output file
Render(matrix_path='../output/output.npy', mode='rgb').run()
