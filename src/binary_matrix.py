"""
binary_matrix.py

Binary Matrix Generator
for RAPD Auto Scorer.

Responsibilities
----------------
1. Load estimated RAPD bands
2. Cluster similar BP values
3. Build binary matrix
4. Export-ready data structure

Author : Ridoy Roy
Platform : Ubuntu
"""


class BinaryMatrix:
    """
    Generate RAPD binary matrix
    from estimated bands.

    Each unique BP cluster
    becomes one matrix row.

    Each lane becomes
    one matrix column.
    """

    # --------------------------------------------------
    # Constructor
    # --------------------------------------------------

    def __init__(self):

        self.clear()

    # --------------------------------------------------
    # Reset
    # --------------------------------------------------

    def clear(self):

        self.bands = []

        self.estimated_table = []

        self.total_samples = 0

        self.clusters = []

        self.bp_rows = []

        self.matrix = []

        self.total_lanes = 0

        self.tolerance = 10

    # --------------------------------------------------
    # Set BP Tolerance
    # --------------------------------------------------

    def set_tolerance(
        self,
        tolerance
    ):

        self.tolerance = int(
            tolerance
        )

    # --------------------------------------------------
    # Get BP Tolerance
    # --------------------------------------------------

    def get_tolerance(self):

        return self.tolerance

    # --------------------------------------------------
    # Total Bands
    # --------------------------------------------------

    def band_count(self):

        return len(
            self.bands
        )

    # --------------------------------------------------
    # Total Clusters
    # --------------------------------------------------

    def cluster_count(self):

        return len(
            self.clusters
        )

    # --------------------------------------------------
    # Total BP Rows
    # --------------------------------------------------

    def row_count(self):

        return len(
            self.bp_rows
        )

    # --------------------------------------------------
    # Total Lanes
    # --------------------------------------------------

    def lane_count(self):

        return self.total_lanes

    # --------------------------------------------------
    # Has Data
    # --------------------------------------------------

    def has_data(self):

        return self.band_count() > 0

    # --------------------------------------------------
    # Get Estimated Bands
    # --------------------------------------------------

    def get_bands(self):

        return self.bands

    # --------------------------------------------------
    # Get Clusters
    # --------------------------------------------------

    def get_clusters(self):

        return self.clusters

    # --------------------------------------------------
    # Get Representative BP Rows
    # --------------------------------------------------

    def get_bp_rows(self):

        return self.bp_rows

    # --------------------------------------------------
    # Get Binary Matrix
    # --------------------------------------------------

    def get_matrix(self):

        return self.matrix

    # --------------------------------------------------
    # Load Estimated Bands
    # --------------------------------------------------

    def load_bands(
        self,
        bands
    ):

        """
        Load estimated bands.

        Expected format
        ---------------

        {
            "id"   : 13,
            "lane" : 2,
            "bp"   : 382,
            "x"    : 220.5,
            "y"    : 315.2
        }
        """

        self.clear()

        if bands is None:
            return

        highest_lane = 0

        for band in bands:

            # ------------------------------
            # Validate Required Fields
            # ------------------------------

            if "lane" not in band:
                continue

            if "bp" not in band:
                continue

            if band["lane"] is None:
                continue

            if band["bp"] is None:
                continue

            # ------------------------------
            # Ignore Ladder Lane
            # ------------------------------

            if int(band["lane"]) == 1:
                continue

            item = {

                "id": int(
                    band["id"]
                ),

                "lane": int(
                    band["lane"]
                ),

                "bp": float(
                    band["bp"]
                ),

                "x": float(
                    band["x"]
                ),

                "y": float(
                    band["y"]
                )

            }

            self.bands.append(
                item
            )

            if item["lane"] > highest_lane:

                highest_lane = item["lane"]

        # ----------------------------------
        # Store Sample Count
        # ----------------------------------

        if highest_lane > 1:

            self.total_lanes = highest_lane - 1

        else:

            self.total_lanes = 0

        # ----------------------------------
        # Sort Estimated Bands
        # ----------------------------------

        self.bands.sort(

            key=lambda band: (

                band["bp"],

                band["lane"]

            )

        )

    # --------------------------------------------------
    # Get One Band
    # --------------------------------------------------

    def get_band(
        self,
        index
    ):

        if index < 0:
            return None

        if index >= len(self.bands):
            return None

        return self.bands[index]

    # --------------------------------------------------
    # Print Loaded Bands
    # --------------------------------------------------

    def print_bands(self):

        """
        Debug only.
        """

        for band in self.bands:

            print(

                f"Lane {band['lane']} | "

                f"Band {band['id']} | "

                f"{band['bp']:.2f} bp"

            )

    # --------------------------------------------------
    # Build BP Clusters
    # --------------------------------------------------

    def build_clusters(self):

        """
        Group similar BP values together.

        Example
        -------

        381
        382
        385

        ↓

        One Cluster
        """

        self.clusters = []

        if len(self.bands) == 0:

            return

        # ------------------------------------------
        # Bands must already be sorted by BP
        # ------------------------------------------

        current_cluster = [

            self.bands[0]

        ]

        for band in self.bands[1:]:

            previous = current_cluster[-1]

            difference = abs(

                band["bp"]

                - previous["bp"]

            )

            # --------------------------------------
            # Same Cluster
            # --------------------------------------

            if difference <= self.tolerance:

                current_cluster.append(

                    band

                )

            # --------------------------------------
            # New Cluster
            # --------------------------------------

            else:

                self.clusters.append(

                    current_cluster

                )

                current_cluster = [

                    band

                ]

        # ------------------------------------------
        # Store Last Cluster
        # ------------------------------------------

        self.clusters.append(

            current_cluster

        )

    # --------------------------------------------------
    # Get One Cluster
    # --------------------------------------------------

    def get_cluster(
        self,
        index
    ):

        if index < 0:

            return None

        if index >= len(

            self.clusters

        ):

            return None

        return self.clusters[index]

    # --------------------------------------------------
    # Print Clusters
    # --------------------------------------------------

    def print_clusters(self):

        """
        Debug only.
        """

        for index, cluster in enumerate(

            self.clusters,

            start=1

        ):

            print(

                f"\nCluster {index}"

            )

            for band in cluster:

                print(

                    f"Lane {band['lane']} | "

                    f"Band {band['id']} | "

                    f"{band['bp']:.2f} bp"

                )

    # --------------------------------------------------
    # Build Representative BP Rows
    # --------------------------------------------------

    def build_bp_rows(self):

        """
        Build representative BP
        using cluster mean.

        Example
        -------

        381
        382
        385

        ↓

        Mean = 382.67

        ↓

        Representative = 383
        """

        self.bp_rows = []

        if len(self.clusters) == 0:

            return

        # ------------------------------------------
        # Process Every Cluster
        # ------------------------------------------

        for cluster in self.clusters:

            total_bp = 0.0

            members = []

            for band in cluster:

                total_bp += band["bp"]

                members.append(

                    band["bp"]

                )

            mean_bp = (

                total_bp /

                len(cluster)

            )

            representative = int(

                round(mean_bp)

            )

            self.bp_rows.append(

                {

                    "bp": representative,

                    "mean": mean_bp,

                    "members": members,

                    "bands": cluster

                }

            )

        # ------------------------------------------
        # Sort Ascending
        # ------------------------------------------

        self.bp_rows.sort(

            key=lambda row: row["bp"]

        )

    # --------------------------------------------------
    # Get One BP Row
    # --------------------------------------------------

    def get_bp_row(
        self,
        index
    ):

        if index < 0:

            return None

        if index >= len(

            self.bp_rows

        ):

            return None

        return self.bp_rows[index]

    # --------------------------------------------------
    # Print Representative Rows
    # --------------------------------------------------

    def print_bp_rows(self):

        """
        Debug only.
        """

        for row in self.bp_rows:

            print(

                f"{row['bp']} bp"

            )

            print(

                "Members :",

                row["members"]

            )

            print()

    # --------------------------------------------------
    # Build Binary Matrix
    # --------------------------------------------------

    def build_matrix(self):

        """
        Build binary matrix.

        Rows
        ----
        Representative BP

        Columns
        -------
        Sample (Lane)

        Value
        -----
        1 = Band Present
        0 = Band Absent
        """

        self.matrix = []

        if len(self.bp_rows) == 0:

            return

        # ------------------------------------------
        # Process Every Representative BP
        # ------------------------------------------

        for row in self.bp_rows:

            matrix_row = {

                "bp": row["bp"],

                "mean": row["mean"],

                "min_bp": min(

                    row["members"]

                ),

                "max_bp": max(

                    row["members"]

                ),

                "samples": []

            }

            # --------------------------------------
            # Create Empty Sample List
            # --------------------------------------

            for sample in range(

                1,

                self.total_lanes + 1

            ):

                matrix_row["samples"].append(

                    0

                )

            # --------------------------------------
            # Fill Presence / Absence
            # --------------------------------------

            for band in row["bands"]:

                sample_index = (

                    band["lane"] - 2

                )

                if (

                    0 <= sample_index

                    < self.total_lanes

                ):

                    matrix_row["samples"][

                        sample_index

                    ] = 1

            self.matrix.append(

                matrix_row

            )

        # ------------------------------------------
        # Final Sort
        # ------------------------------------------

        self.matrix.sort(

            key=lambda row: row["bp"]

        )

    # --------------------------------------------------
    # Get One Matrix Row
    # --------------------------------------------------

    def get_matrix_row(

        self,

        index

    ):

        if index < 0:

            return None

        if index >= len(

            self.matrix

        ):

            return None

        return self.matrix[index]

    # --------------------------------------------------
    # Print Matrix
    # --------------------------------------------------

    def print_matrix(self):

        """
        Debug only.
        """

        for row in self.matrix:

            print(

                row["bp"],

                row["samples"]

            )

    # --------------------------------------------------
    # Export Table
    # --------------------------------------------------



    def export_table(
        self,
        group_names=None,
        sample_names=None
    ):

        """
        Convert binary matrix into
        export-ready table.

        Returns
        -------
        list
            2D table
        """

        table = []

        # ------------------------------------------
        # Default Sample Names
        # ------------------------------------------

        if sample_names is None:

            sample_names = [

                "S1",
                "S2",
                "S3",

                "S4",
                "S5",
                "S6",

                "S7",
                "S8",
                "S9"

            ][:self.total_lanes]

        # ------------------------------------------
        # Default Group Names
        # ------------------------------------------

        if group_names is None:

            group_names = [

                "Coastal",
                "Coastal",
                "Coastal",

                "Riverine",
                "Riverine",
                "Riverine",

                "Haor",
                "Haor",
                "Haor"

            ][:self.total_lanes]

        # ------------------------------------------
        # Group Header
        # ------------------------------------------

        group_row = [

            "Band\\Sample"

        ]

        group_row.extend(

            group_names

        )

        table.append(

            group_row

        )

        # ------------------------------------------
        # Sample Header
        # ------------------------------------------

        sample_row = [

            "BP"

        ]

        sample_row.extend(

            sample_names

        )

        table.append(

            sample_row

        )

        # ------------------------------------------
        # Matrix Rows
        # ------------------------------------------

        for row in self.matrix:

            output = [

                f"{row['bp']} bp"

            ]

            output.extend(

                row["samples"]

            )

            table.append(

                output

            )

        return table

    # --------------------------------------------------
    # Print Export Table
    # --------------------------------------------------

    def print_table(self):

        """
        Debug only.
        """

        table = self.export_table()

        for row in table:

            print(row)

    # --------------------------------------------------
    #
    # --------------------------------------------------
    # Build From Estimated Report
    # --------------------------------------------------

    def build_from_estimated_report(self):

        """
        Complete Binary Matrix pipeline
        using an Estimated Report table.
        """

        if len(self.bands) == 0:
            return

        # ------------------------------------------
        # Sort by BP
        # ------------------------------------------

        self.bands.sort(

            key=lambda band: (

                band["bp"],

                band["lane"]

            )

        )

        # ------------------------------------------
        # Create BP Clusters
        # ------------------------------------------

        self.build_clusters()

        # ------------------------------------------
        # Representative BP
        # ------------------------------------------

        self.build_bp_rows()

        # ------------------------------------------
        # Binary Matrix
        # ------------------------------------------

        self.build_matrix()

    # --------------------------------------------------
    # Run Complete Pipeline
    # --------------------------------------------------

    def run(
        self,
        bands,
        tolerance=None
    ):

        """
        Complete Binary Matrix Pipeline

        1. Load Bands
        2. Build Clusters
        3. Build Representative BP
        4. Build Binary Matrix
        """

        if tolerance is not None:

            self.set_tolerance(
                tolerance
            )

        self.load_bands(
            bands
        )

        self.build_clusters()

        self.build_bp_rows()

        self.build_matrix()

    # --------------------------------------------------
    # Matrix Statistics
    # --------------------------------------------------

    def statistics(self):

        """
        Return Binary Matrix Statistics.
        """

        return {

            "estimated_bands": len(
                self.bands
            ),

            "clusters": len(
                self.clusters
            ),

            "bp_rows": len(
                self.bp_rows
            ),

            "samples": self.total_lanes

        }

    # --------------------------------------------------
    # Summary Text
    # --------------------------------------------------

    def summary(self):

        stats = self.statistics()

        lines = [

            "Binary Matrix Summary",

            "",

            f"Estimated Bands : {stats['estimated_bands']}",

            f"Clusters        : {stats['clusters']}",

            f"Representative BP Rows : {stats['bp_rows']}",

            f"Samples         : {stats['samples']}",

            f"Tolerance       : ±{self.tolerance} bp"

        ]

        return "\n".join(
            lines
        )

    # --------------------------------------------------
    # Has Matrix
    # --------------------------------------------------

    def has_matrix(self):

        return len(
            self.matrix
        ) > 0

    # --------------------------------------------------
    # Total Samples
    # --------------------------------------------------

    def sample_count(self):

        return self.total_lanes

    # --------------------------------------------------
    # Get Representative BP List
    # --------------------------------------------------

    def representative_bp(self):

        """
        Returns

        Example

        [352,401,615,...]
        """

        return [

            row["bp"]

            for row in self.matrix

        ]

    # --------------------------------------------------
    # Debug Print Summary
    # --------------------------------------------------

    def print_summary(self):

        print()

        print(

            self.summary()

        )

        print()
    # --------------------------------------------------
    # Validate Matrix
    # --------------------------------------------------

    def validate(self):

        """
        Validate current matrix.

        Returns
        -------
        bool
        """

        if len(self.matrix) == 0:

            return False

        expected = self.total_lanes

        for row in self.matrix:

            if len(row["samples"]) != expected:

                return False

        return True

    # --------------------------------------------------
    # Duplicate Representative BP
    # --------------------------------------------------

    def has_duplicate_bp(self):

        """
        Check duplicate representative BP.
        """

        seen = set()

        for row in self.matrix:

            bp = row["bp"]

            if bp in seen:

                return True

            seen.add(bp)

        return False

    # --------------------------------------------------
    # Export Ready
    # --------------------------------------------------

    def export_ready(self):

        """
        Matrix ready for export?
        """

        if not self.has_matrix():

            return False

        if not self.validate():

            return False

        return True

    # --------------------------------------------------
    # Total Present Bands
    # --------------------------------------------------

    def total_present(self):

        total = 0

        for row in self.matrix:

            total += sum(

                row["samples"]

            )

        return total

    # --------------------------------------------------
    # Total Absent Bands
    # --------------------------------------------------

    def total_absent(self):

        total = 0

        for row in self.matrix:

            total += (

                len(row["samples"])

                -

                sum(row["samples"])

            )

        return total

    # --------------------------------------------------
    # Matrix Shape
    # --------------------------------------------------

    def shape(self):

        """
        Returns

        (rows, columns)
        """

        return (

            len(self.matrix),

            self.total_lanes

        )

    # --------------------------------------------------
    # Get One Sample Column
    # --------------------------------------------------

    def get_sample(

        self,

        sample_index

    ):

        """
        Returns one sample column.

        sample_index starts from 1.
        """

        if sample_index < 1:

            return []

        if sample_index > self.total_lanes:

            return []

        output = []

        for row in self.matrix:

            output.append(

                row["samples"][

                    sample_index - 1

                ]

            )

        return output

    # --------------------------------------------------
    # Debug Information
    # --------------------------------------------------

    def debug(self):

        print()

        print(self.summary())

        print()

        print(

            "Matrix Shape :",

            self.shape()

        )

        print(

            "Present :", self.total_present()

        )

        print(

            "Absent  :", self.total_absent()

        )

        print(

            "Export Ready :", self.export_ready()

        )

        print()

    # --------------------------------------------------
    # Load Estimated Report Table
    # --------------------------------------------------
    
    def load_estimated_table(
        self,
        table
    ):
        """
        Load Estimated Report.

        L1 = Ladder
        L2-L10 = Samples

        Ladder column is ignored.
        """

        self.clear()

        if table is None:
            return

        if len(table) < 2:
            return

        header = table[0]

        # Ignore Ladder column

        self.total_lanes = max(
            0,
            len(header) - 1
        )

        for row in table[1:]:

            if len(row) == 0:
                continue

            # Skip first column (L1)

            for column in range(1, len(row)):

                cell = row[column]

                if cell is None:
                    continue

                text = str(cell).strip()

                if text == "":
                    continue

                lines = text.splitlines()

                if len(lines) < 2:
                    continue

                try:

                    band_id = int(
                        lines[0].replace(".", "")
                    )

                    bp = float(
                        lines[1]
                        .replace("bp", "")
                        .strip()
                    )

                except:

                    continue

                self.bands.append(

                    {

                        "id": band_id,

                        # L2 -> Sample1
                        # L3 -> Sample2

                        "lane": column +1,

                        "bp": bp,

                        "x": 0.0,

                        "y": 0.0

                    }

                )

        self.bands.sort(

            key=lambda x: (

                x["bp"],
                x["lane"]

            )

        )



    ##===========================================
    ## Build From Estimated Report  
    ##===========================================

    def build_from_estimated_report(self):

        if len(self.bands) == 0:
            return

        converted = []

        for band in self.bands:

            converted.append(

                {

                    "id": band["id"],

                    "lane": band["lane"],

                    "bp": band["bp"],

                    "x": 0.0,

                    "y": 0.0

                }

            )

        self.load_bands(converted)

        self.build_clusters()

        self.build_bp_rows()

        self.build_matrix()
