"""
bp_estimator.py

Base Pair (bp) Estimation Module
RAPD Auto Scorer

Responsibilities
----------------
1. Store ladder band information
2. Store ladder bp values
3. Prepare calibration data
4. Estimate unknown band size
5. Export estimated bp

Author : Ridoy Roy
Platform : Ubuntu
"""

import math


class BPEstimator:

    # ==================================================
    # Constructor
    # ==================================================

    def __init__(self):

        # ------------------------------------------
        # Ladder Bands
        #
        # Each item:
        # {
        #     "x": float,
        #     "y": float,
        #     "bp": float
        # }
        # ------------------------------------------

        self.ladder_bands = []

        # ------------------------------------------
        # Calibration Parameters
        # ------------------------------------------

        self.slope = None

        self.intercept = None

        self.r_squared = None

        # Calibration available?

        self.calibrated = False

    # ==================================================
    # Clear Everything
    # ==================================================

    def clear(self):

        self.ladder_bands.clear()

        self.slope = None

        self.intercept = None

        self.r_squared = None

        self.calibrated = False

    # ==================================================
    # Add Ladder Band
    # ==================================================

    def add_ladder_band(self, x, y, bp):

        band = {

            "x": float(x),

            "y": float(y),

            "bp": float(bp)

        }

        self.ladder_bands.append(band)

        # Always keep top → bottom

        self.ladder_bands.sort(
            key=lambda band: band["y"]
        )

        return band

    # ==================================================
    # Remove Last Ladder Band
    # ==================================================

    def undo(self):

        if self.ladder_bands:

            self.ladder_bands.pop()

    # ==================================================
    # Total Ladder Bands
    # ==================================================

    def count(self):

        return len(self.ladder_bands)

    # ==================================================
    # Get All Ladder Bands
    # ==================================================

    def get_all(self):

        return self.ladder_bands

    # ==================================================
    # Get Ladder Band
    # ==================================================

    def get(self, index):

        if index < 0:

            return None

        if index >= len(self.ladder_bands):

            return None

        return self.ladder_bands[index]

    # ==================================================
    # Check Calibration
    # ==================================================

    def is_calibrated(self):

        return self.calibrated
    
    # ==================================================
    # Update Ladder BP
    # ==================================================

    def update_bp(self, index, bp):

        if index < 0:
            return False

        if index >= len(self.ladder_bands):
            return False

        self.ladder_bands[index]["bp"] = float(bp)

        return True

    # ==================================================
    # Delete Ladder Band
    # ==================================================

    def delete(self, index):

        if index < 0:
            return False

        if index >= len(self.ladder_bands):
            return False

        self.ladder_bands.pop(index)

        return True

    # ==================================================
    # Prepare Calibration Data
    # ==================================================

    def calibration_data(self):

        """
        Returns
        -------
        x_values : Migration distance (Y)

        y_values : log10(bp)
        """

        x_values = []

        y_values = []

        for band in self.ladder_bands:

            bp = band["bp"]

            if bp <= 0:
                continue

            x_values.append(
                band["y"]
            )

            y_values.append(
                math.log10(bp)
            )

        return x_values, y_values

    # ==================================================
    # Check Enough Ladder Bands
    # ==================================================

    def ready(self):

        """
        At least 3 ladder bands
        are required.
        """

        return len(self.ladder_bands) >= 3

    # ==================================================
    # Get BP List
    # ==================================================

    def bp_values(self):

        return [

            band["bp"]

            for band in self.ladder_bands

        ]

    # ==================================================
    # Get Y Positions
    # ==================================================

    def migration_distance(self):

        return [

            band["y"]

            for band in self.ladder_bands

        ]

    # ==================================================
    # Sort Ladder Bands
    # ==================================================

    def sort(self):

        self.ladder_bands.sort(
            key=lambda band: band["y"]
        )

    # ==================================================
    # Check Duplicate BP
    # ==================================================

    def has_duplicate_bp(self):

        values = self.bp_values()

        return len(values) != len(set(values))
    
    # ==================================================
    # Linear Regression
    # ==================================================

    def calibrate(self):

        """
        Calculates

        log10(bp) = slope * y + intercept

        using least squares regression.
        """

        x, y = self.calibration_data()

        n = len(x)

        if n < 3:

            self.calibrated = False

            return False

        mean_x = sum(x) / n

        mean_y = sum(y) / n

        numerator = 0.0

        denominator = 0.0

        for xi, yi in zip(x, y):

            numerator += (
                (xi - mean_x) *
                (yi - mean_y)
            )

            denominator += (
                (xi - mean_x) ** 2
            )

        if denominator == 0:

            self.calibrated = False

            return False

        self.slope = numerator / denominator

        self.intercept = (
            mean_y -
            self.slope * mean_x
        )

        # ------------------------------------------
        # Calculate R²
        # ------------------------------------------

        ss_total = 0.0

        ss_residual = 0.0

        for xi, yi in zip(x, y):

            predicted = (
                self.slope * xi +
                self.intercept
            )

            ss_total += (
                yi - mean_y
            ) ** 2

            ss_residual += (
                yi - predicted
            ) ** 2

        if ss_total == 0:

            self.r_squared = 1.0

        else:

            self.r_squared = (
                1 -
                (ss_residual / ss_total)
            )

        self.calibrated = True

        return True

    # ==================================================
    # Regression Equation
    # ==================================================

    def equation(self):

        if not self.calibrated:

            return None

        return (

            self.slope,

            self.intercept

        )

    # ==================================================
    # R Squared
    # ==================================================

    def r2(self):

        return self.r_squared

    # ==================================================
    # Predict BP
    # ==================================================

    def estimate_bp(self, y_position):

        """
        Estimate unknown band size
        from migration distance.
        """

        if not self.calibrated:

            return None

        log_bp = (

            self.slope *
            y_position +

            self.intercept

        )

        bp = 10 ** log_bp

        return bp

    # ==================================================
    # Estimate Multiple Bands
    # ==================================================

    def estimate_all(self, bands):

        if not self.calibrated:

            return bands

        for band in bands:

            # Skip ladder bands
            if band.get("bp") is not None:

                continue

            band["bp"] = self.estimate_bp(
                band["y"]
            )

        return bands
    
    # ==================================================
    # Estimate One Band
    # ==================================================

    def estimate_band(self, band):

        """
        Estimate bp of a single band.

        Returns
        -------
        Updated band dictionary
        """

        if not self.calibrated:

            return band

        bp = self.estimate_bp(
            band["y"]
        )

        if bp is None:

            return band

        band["bp"] = round(bp, 2)

        return band

    # ==================================================
    # Estimate All Sample Bands
    # ==================================================

    def estimate_all(self, bands):

        """
        Estimate bp for every sample band.

        Ladder bands are skipped.
        """

        if not self.calibrated:

            return bands

        output = []

        for band in bands:

            # Skip ladder bands

            if band.get("bp") is not None:

                output.append(band)

                continue

            output.append(
                self.estimate_band(band)
            )

        return output

    # ==================================================
    # Get Calibration Information
    # ==================================================

    def calibration_info(self):

        if not self.calibrated:

            return None

        return {

            "slope": self.slope,

            "intercept": self.intercept,

            "r_squared": self.r_squared

        }

    # ==================================================
    # Print Calibration (Debug)
    # ==================================================

    def summary(self):

        if not self.calibrated:

            return "Calibration not available."

        return (

            f"Slope      : {self.slope:.6f}\n"

            f"Intercept  : {self.intercept:.6f}\n"

            f"R²         : {self.r_squared:.4f}\n"

            f"Ladder     : {len(self.ladder_bands)} bands"

        )

    # ==================================================
    # Export Calibration Data
    # ==================================================

    def export_ladder(self):

        return list(self.ladder_bands)
    
    # ==================================================
    # Reset Calibration
    # ==================================================

    def reset_calibration(self):

        self.slope = None

        self.intercept = None

        self.r_squared = None

        self.calibrated = False

    # ==================================================
    # Remove All Ladder Bands
    # ==================================================

    def clear_ladder(self):

        self.ladder_bands.clear()

        self.reset_calibration()

    # ==================================================
    # Calibration Available ?
    # ==================================================

    def has_calibration(self):

        return self.calibrated

    # ==================================================
    # Total Ladder Points
    # ==================================================

    def total_ladder_points(self):

        return len(self.ladder_bands)

    # ==================================================
    # Get Slope
    # ==================================================

    def get_slope(self):

        return self.slope

    # ==================================================
    # Get Intercept
    # ==================================================

    def get_intercept(self):

        return self.intercept

    # ==================================================
    # Export Estimated Bands
    # ==================================================

    def export(self, bands):

        """
        Returns a simplified list
        for CSV export.
        """

        output = []

        for band in bands:

            output.append({

                "id": band.get("id"),

                "lane": band.get("lane"),

                "x": band.get("x"),

                "y": band.get("y"),

                "bp": band.get("bp")

            })

        return output

    # ==================================================
    # Print Object
    # ==================================================

    def __repr__(self):

        return (

            f"BPEstimator("
            f"ladder={len(self.ladder_bands)}, "
            f"calibrated={self.calibrated})"

        )
