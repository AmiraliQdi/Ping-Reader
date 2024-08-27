from PingViewerReader.src.Render import Render
from Reader import Reader

#reader = Reader(f"../input")
#reader.save_data(f"output")
Render(matrix_path='../output/output.npy', mode='rgb',resolution=(200, 90)).run()
