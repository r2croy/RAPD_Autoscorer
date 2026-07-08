"""
viewer.py

Interactive Image Viewer
RAPD Auto Scorer

Module-4

Features
--------
✓ Smooth Zoom
✓ Smooth Pan
✓ Image Centering
✓ Band Overlay
✓ Lane Overlay
✓ Coordinate Conversion

Author : Ridoy Roy
Platform : Ubuntu
"""

import tkinter as tk

from PIL import Image
from PIL import ImageTk

from .config import (
    CANVAS_BACKGROUND,
    INITIAL_ZOOM,
    ZOOM_STEP,
    MIN_ZOOM,
    MAX_ZOOM
)


class ImageViewer:

    """
    Interactive image viewer.

    Responsibilities
    ----------------
    • Display image
    • Zoom
    • Pan
    • Coordinate conversion
    • Draw bands
    • Draw lanes
    """

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self, parent):

        self.parent = parent

        # --------------------------------------------------
        # Canvas
        # --------------------------------------------------

        self.canvas = tk.Canvas(
            parent,
            bg=CANVAS_BACKGROUND,
            highlightthickness=0,
            cursor="crosshair"
        )

        self.canvas.pack(
            fill=tk.BOTH,
            expand=True
        )

        # --------------------------------------------------
        # Image
        # --------------------------------------------------

        self.original_image = None

        self.display_image = None

        self.tk_image = None

        self.image_id = None

        # --------------------------------------------------
        # Zoom
        # --------------------------------------------------

        self.zoom = INITIAL_ZOOM

        # --------------------------------------------------
        # Pan
        # --------------------------------------------------

        self.offset_x = 0

        self.offset_y = 0

        self.start_x = 0

        self.start_y = 0

        self.is_dragging = False

        # --------------------------------------------------
        # Canvas Size
        # --------------------------------------------------

        self.canvas_width = 1

        self.canvas_height = 1

        # --------------------------------------------------
        # Overlay Cache
        # --------------------------------------------------

        self.current_bands = []

        self.current_lanes = []

        self.band_items = []

        self.lane_items = []

        # --------------------------------------------------
        # Bind Events
        # --------------------------------------------------

        self.bind_events()
    # ======================================================
    # Bind Events
    # ======================================================

    def bind_events(self):

        # Window Resize

        self.canvas.bind(

            "<Configure>",

            self.on_resize

        )

        # Windows Mouse Wheel

        self.canvas.bind(

            "<MouseWheel>",

            self.on_mousewheel

        )

        # Linux Scroll Up

        self.canvas.bind(

            "<Button-4>",

            self.on_linux_scroll_up

        )

        # Linux Scroll Down

        self.canvas.bind(

            "<Button-5>",

            self.on_linux_scroll_down

        )

        # Start Drag

        self.canvas.bind(

            "<ButtonPress-2>",

            self.start_pan

        )

        # Drag Image

        self.canvas.bind(

            "<B2-Motion>",

            self.pan_image

        )

        # Stop Drag

        self.canvas.bind(

            "<ButtonRelease-2>",

            self.stop_pan

        )

    # ======================================================
    # Load Image
    # ======================================================

    def load_image(self, image_array):
        """
        Load image into the viewer.
        """

        self.original_image = Image.fromarray(image_array)

        # Reset viewer
        self.zoom = INITIAL_ZOOM

        self.offset_x = 0
        self.offset_y = 0

        self.render_image()

    # ======================================================
    # Window Resize
    # ======================================================

    def on_resize(self, event):

        self.canvas_width = event.width
        self.canvas_height = event.height

        self.render_image()

    # ======================================================
    # Render Image
    # ======================================================

    def render_image(self):

        if self.original_image is None:
            return

        # ---------------------------------------------
        # Resize according to zoom
        # ---------------------------------------------

        width = max(
            1,
            int(self.original_image.width * self.zoom)
        )

        height = max(
            1,
            int(self.original_image.height * self.zoom)
        )

        self.display_image = self.original_image.resize(
            (width, height),
            Image.Resampling.LANCZOS
        )

        self.tk_image = ImageTk.PhotoImage(
            self.display_image
        )

        # ---------------------------------------------
        # Clear old image
        # ---------------------------------------------

        self.canvas.delete("image")

        # ---------------------------------------------
        # Image Center
        # ---------------------------------------------

        center_x = (
            self.canvas_width / 2
        ) + self.offset_x

        center_y = (
            self.canvas_height / 2
        ) + self.offset_y

        self.image_id = self.canvas.create_image(

            center_x,

            center_y,

            image=self.tk_image,

            anchor="center",

            tags="image"

        )

        # ---------------------------------------------
        # Redraw overlays
        # ---------------------------------------------

        self.redraw_overlays()

    # ======================================================
    # Fit Image To Window
    # ======================================================

    def fit_to_window(self):

        if self.original_image is None:
            return

        img_w = self.original_image.width
        img_h = self.original_image.height

        if img_w == 0 or img_h == 0:
            return

        scale_x = self.canvas_width / img_w
        scale_y = self.canvas_height / img_h

        self.zoom = min(
            scale_x,
            scale_y
        )

        if self.zoom > 1.0:
            self.zoom = 1.0

        if self.zoom < MIN_ZOOM:
            self.zoom = MIN_ZOOM

        self.offset_x = 0
        self.offset_y = 0

        self.render_image()

    # ======================================================
    # Center Image
    # ======================================================

    def center_image(self):

        self.offset_x = 0
        self.offset_y = 0

        self.render_image()

    # ======================================================
    # Mouse Wheel Zoom (Windows)
    # ======================================================

    def on_mousewheel(self, event):

        if event.delta > 0:
            self.apply_zoom(ZOOM_STEP)
        else:
            self.apply_zoom(1 / ZOOM_STEP)

    # ======================================================
    # Linux Scroll Up
    # ======================================================

    def on_linux_scroll_up(self, event):

        self.apply_zoom(ZOOM_STEP)

    # ======================================================
    # Linux Scroll Down
    # ======================================================

    def on_linux_scroll_down(self, event):

        self.apply_zoom(1 / ZOOM_STEP)

    # ======================================================
    # Apply Zoom
    # ======================================================

    def apply_zoom(self, factor):

        if self.original_image is None:
            return

        new_zoom = self.zoom * factor

        if new_zoom < MIN_ZOOM:
            new_zoom = MIN_ZOOM

        if new_zoom > MAX_ZOOM:
            new_zoom = MAX_ZOOM

        if abs(new_zoom - self.zoom) < 1e-6:
            return

        self.zoom = new_zoom

        self.render_image()

    # ======================================================
    # Start Pan
    # ======================================================

    def start_pan(self, event):

        self.start_x = event.x
        self.start_y = event.y

        self.is_dragging = True

    # ======================================================
    # Pan Image
    # ======================================================

    def pan_image(self, event):

        if not self.is_dragging:
            return

        dx = event.x - self.start_x
        dy = event.y - self.start_y

        self.offset_x += dx
        self.offset_y += dy

        self.start_x = event.x
        self.start_y = event.y

        self.render_image()

    # ======================================================
    # Stop Pan
    # ======================================================

    def stop_pan(self, event):

        self.is_dragging = False

    # ======================================================
    # Canvas -> Image Coordinate
    # ======================================================

    def canvas_to_image(self, canvas_x, canvas_y):

        if self.original_image is None:
            return None

        center_x = (
            self.canvas_width / 2
        ) + self.offset_x

        center_y = (
            self.canvas_height / 2
        ) + self.offset_y

        image_x = (
            (canvas_x - center_x) / self.zoom
        ) + (
            self.original_image.width / 2
        )

        image_y = (
            (canvas_y - center_y) / self.zoom
        ) + (
            self.original_image.height / 2
        )

        if (
            image_x < 0
            or image_y < 0
            or image_x > self.original_image.width
            or image_y > self.original_image.height
        ):
            return None

        return (image_x, image_y)

    # ======================================================
    # Image -> Canvas Coordinate
    # ======================================================

    def image_to_canvas(self, image_x, image_y):

        if self.original_image is None:
            return None

        canvas_x = (
            (image_x - self.original_image.width / 2)
            * self.zoom
        )

        canvas_y = (
            (image_y - self.original_image.height / 2)
            * self.zoom
        )

        canvas_x += (
            self.canvas_width / 2
        ) + self.offset_x

        canvas_y += (
            self.canvas_height / 2
        ) + self.offset_y

        return (canvas_x, canvas_y)
    
    # ==========================================================
    # Draw One Band
    # ==========================================================

    def draw_band(self, band):

        if self.original_image is None:
            return

        canvas_pos = self.image_to_canvas(
            band["x"],
            band["y"]
        )

        if canvas_pos is None:
            return

        x, y = canvas_pos

        r = 2

        circle = self.canvas.create_oval(
            x - r,
            y - r,
            x + r,
            y + r,
            fill="red",
            outline="red",
            width=2,
            tags="band"
        )

        text = self.canvas.create_text(
            x + 12,
            y - 12,
            text=str(band["id"]),
            fill="white",
            font=("Arial", 10, "bold"),
            tags="band"
        )

        self.band_items.append(circle)
        self.band_items.append(text)

    # ==========================================================
    # Draw One Lane
    # ==========================================================

    def draw_lane(self, lane):

        if self.original_image is None:
            return

        top = self.image_to_canvas(
            lane["x"],
            0
        )

        bottom = self.image_to_canvas(
            lane["x"],
            self.original_image.height
        )

        if top is None or bottom is None:
            return

        x1, y1 = top
        x2, y2 = bottom

        # Ladder lane = Green
        if lane["id"] == 1:

            color = "#00ff00"

        else:

            color = "#00aaff"

        line = self.canvas.create_line(

            x1,
            y1,
            x2,
            y2,

            fill=color,

            width=2,

            dash=(5, 3),

            tags="lane"

        )

        label = self.canvas.create_text(

            x1,

            y1 - 15,

            text=f"L{lane['id']}",

            fill=color,

            font=("Arial", 10, "bold"),

            tags="lane"

        )

        self.lane_items.append(line)
        self.lane_items.append(label)

    # ==========================================================
    # Redraw All Overlays
    # ==========================================================

    def redraw_overlays(self):

        self.canvas.delete("band")
        self.canvas.delete("lane")

        self.band_items.clear()
        self.lane_items.clear()

        # Draw lanes first

        for lane in self.current_lanes:

            self.draw_lane(lane)

        # Draw bands on top

        for band in self.current_bands:

            self.draw_band(band)

    # ==========================================================
    # Update Band List
    # ==========================================================

    def redraw_band_list(self, bands):

        self.current_bands = list(bands)

        self.redraw_overlays()

    # ==========================================================
    # Update Lane List
    # ==========================================================

    def redraw_lane_list(self, lanes):

        self.current_lanes = list(lanes)

        self.redraw_overlays()

    # ==========================================================
    # Clear Overlay
    # ==========================================================

    def clear_overlay(self):

        self.canvas.delete("band")
        self.canvas.delete("lane")

        self.band_items.clear()
        self.lane_items.clear()

        self.current_bands.clear()
        self.current_lanes.clear()

    # ==========================================================
    # Reset Viewer
    # ==========================================================

    def reset_view(self):

        if self.original_image is None:
            return

        self.zoom = INITIAL_ZOOM

        self.offset_x = 0
        self.offset_y = 0

        self.render_image()

    # ==========================================================
    # Refresh Viewer
    # ==========================================================

    def refresh(self):

        if self.original_image is None:
            return

        self.render_image()

    # ==========================================================
    # Clear Viewer
    # ==========================================================

    def clear(self):

        self.original_image = None
        self.display_image = None
        self.tk_image = None

        self.zoom = INITIAL_ZOOM

        self.offset_x = 0
        self.offset_y = 0

        self.current_bands.clear()
        self.current_lanes.clear()

        self.band_items.clear()
        self.lane_items.clear()

        self.canvas.delete("all")

    # ==========================================================
    # Focus Canvas
    # ==========================================================

    def focus(self):

        self.canvas.focus_set()

    # ==========================================================
    # Get Canvas
    # ==========================================================

    def get_canvas(self):

        return self.canvas

    # ==========================================================
    # Image Loaded ?
    # ==========================================================

    def has_image(self):

        return self.original_image is not None

    # ==========================================================
    # Image Width
    # ==========================================================

    def image_width(self):

        if self.original_image is None:
            return 0

        return self.original_image.width

    # ==========================================================
    # Image Height
    # ==========================================================

    def image_height(self):

        if self.original_image is None:
            return 0

        return self.original_image.height

    # ==========================================================
    # Image Size
    # ==========================================================

    def image_size(self):

        if self.original_image is None:
            return (0, 0)

        return (
            self.original_image.width,
            self.original_image.height
        )

    # ==========================================================
    # Current Zoom
    # ==========================================================

    def get_zoom(self):

        return self.zoom

    # ==========================================================
    # Current Offset
    # ==========================================================

    def get_offset(self):

        return (
            self.offset_x,
            self.offset_y
        )
