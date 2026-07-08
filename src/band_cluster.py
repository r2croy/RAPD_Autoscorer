"""
band_cluster.py

Estimated band organization module
for RAPD Auto Scorer.

Responsibilities
----------------
1. Collect estimated bands
2. Group bands by lane
3. Preserve band ID
4. Preserve gel position (Y)
5. Prepare export-ready data

Author : Ridoy Roy
Platform : Ubuntu
"""


class BandCluster:
    """
    Organizes estimated RAPD bands into
    lane-wise structures while preserving
    their original gel position.

    This module DOES NOT export files.

    Exporting is handled by exporter.py
    """

    # --------------------------------------------------
    # Constructor
    # --------------------------------------------------

    def __init__(self):

        # Dictionary

        # Example
        #
        # {
        #     1 : [],
        #     2 : [],
        #     ...
        # }

        self.lanes = {}

        # Export grid
        #
        # Will be generated later.

        self.grid = []

        # Maximum lane number

        self.total_lanes = 0

    # --------------------------------------------------
    # Reset Everything
    # --------------------------------------------------

    def clear(self):

        self.lanes.clear()

        self.grid.clear()

        self.total_lanes = 0

    # --------------------------------------------------
    # Total Lane
    # --------------------------------------------------

    def lane_count(self):

        return self.total_lanes

    # --------------------------------------------------
    # Total Bands
    # --------------------------------------------------

    def band_count(self):

        total = 0

        for lane in self.lanes.values():

            total += len(lane)

        return total

    # --------------------------------------------------
    # Has Data
    # --------------------------------------------------

    def has_data(self):

        return self.band_count() > 0

    # --------------------------------------------------
    # Get Lane Dictionary
    # --------------------------------------------------

    def get_lanes(self):

        return self.lanes

    # --------------------------------------------------
    # Get Export Grid
    # --------------------------------------------------

    def get_grid(self):

        return self.grid
    
    # --------------------------------------------------
    # Load Estimated Bands
    # --------------------------------------------------

    def load_bands(self, bands):

        """
        Parameters
        ----------
        bands : list

        Expected format

        {
            "id"   : 13,
            "lane" : 2,
            "x"    : 210.5,
            "y"    : 185.4,
            "bp"   : 382.7
        }
        """

        # Reset previous data

        self.clear()

        if bands is None:
            return

        # ------------------------------------------
        # Read every band
        # ------------------------------------------

        for band in bands:

            # Ignore invalid band

            if "bp" not in band:
                continue

            if band["bp"] is None:
                continue

            if "lane" not in band:
                continue

            if band["lane"] is None:
                continue

            lane_id = int(
                band["lane"]
            )

            # Create lane automatically

            if lane_id not in self.lanes:

                self.lanes[lane_id] = []

            # Store only required information

            self.lanes[lane_id].append(

                {
                    "id": int(
                        band["id"]
                    ),

                    "lane": lane_id,

                    "x": float(
                        band["x"]
                    ),

                    "y": float(
                        band["y"]
                    ),

                    "bp": float(
                        band["bp"]
                    )
                }

            )

        # ------------------------------------------
        # Update total lane
        # ------------------------------------------

        if len(self.lanes) > 0:

            self.total_lanes = max(

                self.lanes.keys()

            )

        else:

            self.total_lanes = 0

        # ------------------------------------------
        # Sort every lane
        # ------------------------------------------

        self.sort_all_lanes()

    # --------------------------------------------------
    # Get One Lane
    # --------------------------------------------------

    def get_lane(self, lane_id):

        return self.lanes.get(
            lane_id,
            []
        )
    
    # --------------------------------------------------
    # Sort One Lane
    # --------------------------------------------------

    def sort_lane(self, lane_id):

        """
        Sort one lane from
        top -> bottom
        according to Y coordinate.
        """

        if lane_id not in self.lanes:
            return

        self.lanes[lane_id].sort(

            key=lambda band: band["y"]

        )

    # --------------------------------------------------
    # Sort All Lanes
    # --------------------------------------------------

    def sort_all_lanes(self):

        """
        Sort every lane
        independently.
        """

        for lane_id in sorted(

            self.lanes.keys()

        ):

            self.sort_lane(

                lane_id

            )

    # --------------------------------------------------
    # Get Top Band
    # --------------------------------------------------

    def first_band(self, lane_id):

        lane = self.get_lane(

            lane_id

        )

        if len(lane) == 0:
            return None

        return lane[0]

    # --------------------------------------------------
    # Get Bottom Band
    # --------------------------------------------------

    def last_band(self, lane_id):

        lane = self.get_lane(

            lane_id

        )

        if len(lane) == 0:
            return None

        return lane[-1]

    # --------------------------------------------------
    # Maximum Bands In Any Lane
    # --------------------------------------------------

    def max_band_per_lane(self):

        maximum = 0

        for lane in self.lanes.values():

            if len(lane) > maximum:

                maximum = len(lane)

        return maximum
    
    # --------------------------------------------------
    # Build Global Grid
    # --------------------------------------------------

    def build_grid(self):

        """
        Create export-ready grid based on
        actual gel position.

        Every row represents one physical
        band position on the gel.

        Columns represent lanes.
        """

        self.grid = []

        # ------------------------------------------
        # Collect every estimated band
        # ------------------------------------------

        all_bands = []

        for lane_id in sorted(

            self.lanes.keys()

        ):

            for band in self.lanes[lane_id]:

                all_bands.append(band)

        # ------------------------------------------
        # Sort by gel position
        # ------------------------------------------

        all_bands.sort(

            key=lambda band: band["y"]

        )

        # ------------------------------------------
        # Create one row for each band
        # ------------------------------------------

        for band in all_bands:

            row = {}

            # Empty every lane

            for lane in range(

                1,

                self.total_lanes + 1

            ):

                row[lane] = ""

            # Put current band
            # into its own lane

            row[band["lane"]] = {

                "id": band["id"],

                "bp": band["bp"],

                "y": band["y"]

            }

            self.grid.append(row)

    # --------------------------------------------------
    # Total Grid Rows
    # --------------------------------------------------

    def row_count(self):

        return len(self.grid)

    # --------------------------------------------------
    # Get One Row
    # --------------------------------------------------

    def get_row(self, index):

        if index < 0:

            return None

        if index >= len(self.grid):

            return None

        return self.grid[index]
    
    # --------------------------------------------------
    # Build Grid With Y Tolerance
    # --------------------------------------------------

    def build_grid_with_tolerance(
        self,
        tolerance=5
    ):

        """
        Build export grid while preserving
        gel band position.

        Bands whose Y coordinates differ by
        less than 'tolerance' pixels will be
        placed on the same Excel row.
        """

        self.grid = []

        # ------------------------------------------
        # Collect all estimated bands
        # ------------------------------------------

        all_bands = []

        for lane_id in sorted(self.lanes.keys()):

            for band in self.lanes[lane_id]:

                all_bands.append(band)

        # ------------------------------------------
        # Sort globally by Y
        # ------------------------------------------

        all_bands.sort(
            key=lambda band: band["y"]
        )

        # ------------------------------------------
        # Create grid
        # ------------------------------------------

        for band in all_bands:

            inserted = False

            # Try to merge into existing row

            for row in self.grid:

                reference_y = row["_y"]

                if abs(

                    band["y"] - reference_y

                ) <= tolerance:

                    lane = band["lane"]

                    # Same lane already occupied?

                    if row[lane] != "":

                        continue

                    row[lane] = {

                        "id": band["id"],

                        "bp": band["bp"],

                        "y": band["y"]

                    }

                    inserted = True

                    break

            # --------------------------------------
            # New row required
            # --------------------------------------

            if not inserted:

                new_row = {

                    "_y": band["y"]

                }

                for lane in range(

                    1,

                    self.total_lanes + 1

                ):

                    new_row[lane] = ""

                new_row[band["lane"]] = {

                    "id": band["id"],

                    "bp": band["bp"],

                    "y": band["y"]

                }

                self.grid.append(new_row)

        # ------------------------------------------
        # Final sort
        # ------------------------------------------

        self.grid.sort(

            key=lambda row: row["_y"]

        )

    # --------------------------------------------------
    # Format One Cell
    # --------------------------------------------------

    def format_cell(self, cell):

        """
        Convert one band dictionary into
        export-ready text.

        Example
        -------

        13.
        382 bp
        """

        if cell == "":
            return ""

        if cell is None:
            return ""

        band_id = cell["id"]

        bp = round(
            cell["bp"]
        )

        return f"{band_id}.\n{bp} bp"

    # --------------------------------------------------
    # Get Export Table
    # --------------------------------------------------

    def export_table(self):

        """
        Returns a 2D list.

        First row contains

        L1 ... L10

        Remaining rows contain

        formatted cells.
        """

        table = []

        # ------------------------------
        # Header
        # ------------------------------

        header = []

        for lane in range(

            1,

            self.total_lanes + 1

        ):

            header.append(

                f"L{lane}"

            )

        table.append(header)

        # ------------------------------
        # Data
        # ------------------------------

        for row in self.grid:

            output = []

            for lane in range(

                1,

                self.total_lanes + 1

            ):

                output.append(

                    self.format_cell(

                        row[lane]

                    )

                )

            table.append(output)

        return table

    # --------------------------------------------------
    # Print Table
    # --------------------------------------------------

    def print_table(self):

        """
        Debug only.
        """

        table = self.export_table()

        for row in table:

            print(row)
