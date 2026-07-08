"""
lane_manager.py

Lane management module for RAPD Auto Scorer

Responsibilities
----------------
1. Store lane center positions
2. Sort lanes (Left → Right)
3. Automatic lane numbering
4. Find nearest lane
5. Assign bands to lanes
6. Store bands inside each lane
7. Ladder lane support

Author : Ridoy Roy
Platform : Ubuntu
"""

import math


class LaneManager:

    # ==================================================
    # Constructor
    # ==================================================

    def __init__(self):

        self.lanes = []

    # ==================================================
    # Add Lane
    # ==================================================

    def add(self, x):

        lane = {

            "id": len(self.lanes) + 1,

            "x": float(x),

            "bands": [],

            "is_ladder": False

        }

        self.lanes.append(lane)

        self.sort()

        return lane

    # ==================================================
    # Undo Last Lane
    # ==================================================

    def undo(self):

        if self.lanes:

            self.lanes.pop()

            self.renumber()

    # ==================================================
    # Delete Nearest Lane
    # ==================================================

    def delete_nearest(
        self,
        x,
        tolerance=20
    ):

        if len(self.lanes) == 0:
            return False

        nearest = None
        nearest_distance = None

        for lane in self.lanes:

            distance = abs(
                lane["x"] - x
            )

            if nearest is None:

                nearest = lane
                nearest_distance = distance

            elif distance < nearest_distance:

                nearest = lane
                nearest_distance = distance

        if nearest_distance <= tolerance:

            self.lanes.remove(nearest)

            self.renumber()

            return True

        return False

    # ==================================================
    # Sort Lanes
    # ==================================================

    def sort(self):

        self.lanes.sort(
            key=lambda lane: lane["x"]
        )

        self.renumber()

    # ==================================================
    # Renumber
    # ==================================================

    def renumber(self):

        for i, lane in enumerate(
            self.lanes,
            start=1
        ):

            lane["id"] = i

    # ==================================================
    # Clear
    # ==================================================

    def clear(self):

        self.lanes.clear()

    # ==================================================
    # Count
    # ==================================================

    def count(self):

        return len(self.lanes)

    # ==================================================
    # Get All
    # ==================================================

    def get_all(self):

        return self.lanes

    # ==================================================
    # Get Lane
    # ==================================================

    def get(self, lane_id):

        for lane in self.lanes:

            if lane["id"] == lane_id:
                return lane

        return None

    # ==================================================
    # Find Nearest Lane
    # ==================================================

    def nearest_lane(self, x):

        if len(self.lanes) == 0:
            return None

        nearest = None
        nearest_distance = float("inf")

        for lane in self.lanes:

            distance = abs(
                lane["x"] - x
            )

            if distance < nearest_distance:

                nearest_distance = distance
                nearest = lane

        return nearest

    # ==================================================
    # Assign One Band
    # ==================================================

    def assign_band(self, band):

        lane = self.nearest_lane(
            band["x"]
        )

        if lane is None:

            band["lane"] = None

            return band

        band["lane"] = lane["id"]

        if band not in lane["bands"]:

            lane["bands"].append(band)

        return band

    # ==================================================
    # Assign All Bands
    # ==================================================

    def assign_all(self, bands):

        # Remove previous assignment

        for lane in self.lanes:

            lane["bands"].clear()

        output = []

        for band in bands:

            output.append(
                self.assign_band(band)
            )

        return output

    # ==================================================
    # Set Ladder Lane
    # ==================================================

    def set_ladder(self, lane_id):

        for lane in self.lanes:

            lane["is_ladder"] = (
                lane["id"] == lane_id
            )

    # ==================================================
    # Get Ladder Lane
    # ==================================================

    def ladder_lane(self):

        for lane in self.lanes:

            if lane["is_ladder"]:
                return lane

        if len(self.lanes):

            return self.lanes[0]

        return None

    # ==================================================
    # Get Bands of Lane
    # ==================================================

    def lane_bands(self, lane_id):

        lane = self.get(lane_id)

        if lane is None:
            return []

        return lane["bands"]

    # ==================================================
    # Lane Center List
    # ==================================================

    def lane_centers(self):

        return [

            lane["x"]

            for lane in self.lanes

        ]

    # ==================================================
    # Check Empty
    # ==================================================

    def is_empty(self):

        return len(self.lanes) == 0
