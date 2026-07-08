"""
band_picker.py

Band management module
"""

import math


class BandPicker:
    def __init__(self):
        self.bands = []

    # --------------------------------------------------
    # Add Band
    # --------------------------------------------------
    def add(self, x, y):
        """
        Add a new band.

        Parameters
        ----------
        x : float
            X coordinate

        y : float
            Y coordinate

        Returns
        -------
        dict
            Newly created band
        """

        band = {
            "id": len(self.bands) + 1,
            "x": float(x),
            "y": float(y)
        }

        self.bands.append(band)

        return band

    # --------------------------------------------------
    # Undo Last Band
    # --------------------------------------------------
    def undo(self):
        """
        Remove the last added band.
        """

        if self.bands:
            self.bands.pop()

        self.renumber()

    # --------------------------------------------------
    # Delete Nearest Band
    # --------------------------------------------------
    def delete_nearest(self, x, y, tolerance=10):
        """
        Delete nearest band within tolerance.
        """

        if not self.bands:
            return False

        nearest = None
        nearest_distance = None

        for band in self.bands:

            distance = math.sqrt(
                (band["x"] - x) ** 2 +
                (band["y"] - y) ** 2
            )

            if nearest is None:
                nearest = band
                nearest_distance = distance

            elif distance < nearest_distance:
                nearest = band
                nearest_distance = distance

        if nearest_distance <= tolerance:
            self.bands.remove(nearest)
            self.renumber()
            return True

        return False

    # --------------------------------------------------
    # Renumber Bands
    # --------------------------------------------------
    def renumber(self):
        """
        Reassign band IDs.
        """

        for i, band in enumerate(self.bands, start=1):
            band["id"] = i

    # --------------------------------------------------
    # Remove All
    # --------------------------------------------------
    def clear(self):
        self.bands.clear()

    # --------------------------------------------------
    # Get All Bands
    # --------------------------------------------------
    def get_all(self):
        return self.bands

    # --------------------------------------------------
    # Total Bands
    # --------------------------------------------------
    def count(self):
        return len(self.bands)
