from Reader import Reader

input_folder = "input"
reader = Reader(f"../{input_folder}")
reader.sonar_view(0)
reader.save_data(f"{input_folder}_output")
