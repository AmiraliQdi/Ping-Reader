import os

import cv2
import numpy as np
from PIL import Image
from matplotlib import cm, pyplot as plt
from pip._internal import resolution


class Render:

    def __init__(self, matrix_path, mode='rgb', resolution=(1200, 90)):
        self.output_file_path = matrix_path
        self.matrix = np.load(self.output_file_path)
        self.cmap = plt.get_cmap('jet')
        self.raw_resolution = resolution

    def run(self, output_path='../output/images'):
        self._make_raw_pictures(path=output_path + '/raw', target_resolution=self.raw_resolution)
        # self._make_slice_pictures(path=output_path + '/slice')

    def _make_slice_pictures(self, path):
        colormap = self.cmap
        center = (640 // 2, 640 // 2)  # Ensure center is integer
        max_range = 60  # Max range in meters
        meters_per_pixel = max_range / center[0]  # Calculate meters per pixel
        n, degrees, length = self.matrix.shape
        for p in range(1):
            image = np.zeros((640, 640, 3), dtype=np.uint8)
            current_angle = 150
            for d in range(degrees):
                data = self.matrix[p, d, :]
                linear_factor = len(data) / center[0]
                for i in range(int(center[0])):
                    if i < center[0] * 60 / 60:
                        intensity_value = data[int(i * linear_factor - 1)]
                    else:
                        intensity_value = 0

                    normalized_value = intensity_value / 255.0
                    rgb_color = colormap(normalized_value)[:3]  # Get RGB tuple, discard alpha channel
                    rgb_color = (np.array(rgb_color) * 255).astype(np.uint8)

                    # Reverse the RGB channels to make blue red and red blue
                    rgb_color = rgb_color[[2, 1, 0]]  # Swap red and blue

                    for k in np.linspace(0, 1, 8 * 1):
                        x = int(center[0] + i * np.cos(2 * np.pi * (current_angle + k) / 400))
                        y = int(center[1] + i * np.sin(2 * np.pi * (current_angle + k) / 400))
                        image[x, y] = rgb_color  # Assign reversed RGB color to the pixel

                current_angle = (current_angle + 1) % 400

                cv2.imshow(f"file name:", image)
                cv2.waitKey(5)

    def _make_raw_pictures(self, path, target_resolution):
        for i in range(self.matrix.shape[0]):
            # Select the i-th image
            img = self.matrix[i]

            # Normalize the image to the range [0, 1] for colormap
            img_normalized = img / 255.0

            # Apply the colormap (it returns a 4D array (H, W, 4))
            img_colored = self.cmap(img_normalized)

            # Drop the alpha channel (RGBA to RGB)
            img_colored = img_colored[:, :, :3]

            # Convert to 8-bit color values (0-255)
            img_colored = (img_colored * 255).astype(np.uint8)

            # Convert numpy array to an Image object
            img_pil = Image.fromarray(img_colored)

            # Resize the image to the target resolution
            img_resized = img_pil.resize(target_resolution, Image.ANTIALIAS)

            # Ensure the output directory exists
            output_dir = os.path.join(path, '')
            os.makedirs(output_dir, exist_ok=True)

            # Save the image with the desired resolution
            img_resized.save(os.path.join(output_dir, f'image_{i + 1:03d}.png'))
