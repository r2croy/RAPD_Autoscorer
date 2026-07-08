"""
config.py

Global configuration for RAPD Auto Scorer
"""

# ==========================================================
# Application
# ==========================================================

APP_NAME = "RAPD Auto Scorer"

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 850

BACKGROUND_COLOR = "#1E1E1E"

# ==========================================================
# Viewer
# ==========================================================

INITIAL_ZOOM = 1.0

ZOOM_STEP = 1.10

MIN_ZOOM = 0.20

MAX_ZOOM = 8.00

# ==========================================================
# Band Marker
# ==========================================================

BAND_COLOR = "red"

BAND_RADIUS = 5

TEXT_COLOR = "white"

TEXT_OFFSET_X = 12

TEXT_OFFSET_Y = -12

FONT = ("Arial", 10, "bold")

# ==========================================================
# Canvas
# ==========================================================

CANVAS_BACKGROUND = "black"

# ==========================================================
# Supported Image Formats
# ==========================================================

SUPPORTED_IMAGE_TYPES = [
    ("Image Files", "*.png *.jpg *.jpeg *.tif *.tiff *.bmp")
]
