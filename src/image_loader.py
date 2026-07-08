"""
image_loader.py

Image loading module for RAPD Auto Scorer
"""

import cv2
import os


class ImageLoader:
    def __init__(self):
        self.image = None
        self.image_path = None

    # ---------------------------------------------------------
    # Load Image
    # ---------------------------------------------------------
    def load_image(self, filepath):
        """
        Load an image using OpenCV and convert BGR -> RGB.

        Parameters
        ----------
        filepath : str
            Path to the image.

        Returns
        -------
        image : numpy.ndarray
            RGB image.
        """

        if not os.path.exists(filepath):
            raise FileNotFoundError(
                f"Image not found:\n{filepath}"
            )

        image = cv2.imread(filepath)

        if image is None:
            raise ValueError(
                "Unable to load image."
            )

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        self.image = image
        self.image_path = filepath

        return image

    # ---------------------------------------------------------
    # Get Image
    # ---------------------------------------------------------
    def get_image(self):
        return self.image

    # ---------------------------------------------------------
    # Get Image Size
    # ---------------------------------------------------------
    def get_size(self):
        if self.image is None:
            return None

        height, width = self.image.shape[:2]

        return width, height

    # ---------------------------------------------------------
    # Get Image Path
    # ---------------------------------------------------------
    def get_path(self):
        return self.image_path

    # ---------------------------------------------------------
    # Check Loaded
    # ---------------------------------------------------------
    def is_loaded(self):
        return self.image is not None

    # ---------------------------------------------------------
    # Reset
    # ---------------------------------------------------------
    def clear(self):
        self.image = None
        self.image_path = None
