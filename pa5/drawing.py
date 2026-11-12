"""
CS 121: Drawing Treemaps
The ChiCanvas and ColorKey classes used for actually drawing the treemap
"""

#####################################
# DO NOT MODIFY THE CODE IN THIS FILE
#####################################

import tempfile
import textwrap
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.transforms import Bbox, TransformedBbox
import numpy as np

mpl.rcParams["toolbar"] = "None"

# DO NOT REMOVE THESE LINES OF CODE
# pylint: disable-msg= invalid-name, missing-class-docstring
# pylint: disable-msg= too-many-arguments, protected-access, bare-except
# pylint: disable-msg= too-many-locals, no-self-use


class ChiCanvas:
    def __init__(self, xscale: int = 10, yscale: int = 10):
        """
        initialize a ChiCanvas
        """
        plt.close("all")

        # Get the renderer through a hack
        fig = plt.figure()
        fig.add_subplot(111)
        with tempfile.NamedTemporaryFile(suffix="png", delete=True) as tmp_file:
            fig.savefig(tmp_file)
            self._renderer = (
                plt.gca().figure.canvas.get_renderer()
            )  # get_renderer_cache()
        plt.close("all")

        self._figure, self._ax = plt.subplots(figsize=(xscale, yscale))
        # self._figure.canvas.set_window_title(title)
        self._figure.patch.set_facecolor("white")
        plt.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)
        self._ax.set_axis_off()

    def draw_rectangle(
        self,
        x0: float,
        y0: float,
        x1: float,
        y1: float,
        fill: str = "blue",
        outline: str = "black",
    ):
        """
        draw a rectangle in the canvas at the specified coordinates with the
        given style
        (x0, y0): coordinates of top left corner
        (x1, y1): coordinates of bottom right corner
        fill: color with which to fill rectangle
        outline: color for border of rectangle
        """
        rect = mpatches.Rectangle(
            (x0, y0),
            x1 - x0,
            y1 - y0,
            facecolor=fill,
            linewidth=1,
            linestyle="solid",
            edgecolor=outline,
        )
        self._ax.add_patch(rect)

    def __draw_text_with_rotation(
        self,
        x0: float,
        y0: float,
        w: float,
        h: float,
        txt: str,
        offset_x=0,
        offset_y=0,
        rotation=0,
        fg: str = "black",
        debug: bool = False,
    ):
        """
        draw text txt horizontally at specified (x0, y0) coordinates
        max width w, color fg
        """

        # offset_x = -w/2.0+0.01
        # offset_y = 0
        # rotation = 0

        if debug:
            self.draw_rectangle(
                x0 - w / 2.0,
                y0 - h / 2,
                x0 + w / 2.0,
                y0 + h / 2.0,
                fill="none",
                outline="red",
            )
        clip_rect = mpatches.Rectangle(
            xy=(x0 - w / 2.0, y0 - h / 2.0),
            width=w,
            height=0.1,
            transform=self._ax.transData,
        )
        textobj = plt.text(
            x0 + offset_x,
            y0 + offset_y,
            txt,
            color=fg,
            ha="left",
            va="center",
            clip_path=clip_rect,
            clip_on=True,
            rotation=rotation,
        )
        # Let's store the clipping box in the object, so that we can use it
        # when clipping text
        textobj.set_clip_box(
            TransformedBbox(
                bbox=Bbox(((x0 - w / 2.0, y0 - h / 2.0), (x0 + w / 2.0, y0 + h / 2.0))),
                transform=self._ax.transData,
            )
        )
        textobj.set_rotation_mode("anchor")

    def draw_text(self, x0, y0, w, txt, fg="black", debug=False):
        """
        draw text txt horizontally at specified (x0, y0) coordinates
        max width w, color fg
        """
        # -w/2.0 + 0.02
        self.__draw_text_with_rotation(
            x0,
            y0,
            w,
            0.03,
            txt,
            offset_x=-w / 2.0 + 0.075,
            fg=fg,
            rotation=0,
            debug=debug,
        )

    def draw_text_vertical(self, x0, y0, h, txt, fg="black", debug=False):
        """
        draw text txt vertically at specified (x0, y0) coordinates
        max height h, color fg
        """
        self.__draw_text_with_rotation(
            x0,
            y0,
            0.03,
            h,
            txt,
            offset_y=h / 2.0 - 0.02,
            fg=fg,
            rotation=90,
            debug=debug,
        )

    def show(self):
        """
        display the canvas on screen
        """
        # Draw only the unit box and flip the y axis
        plt.xlim((0, 1))
        plt.ylim((1, 0))

        self._figure.canvas.mpl_connect("draw_event", ChiCanvas._on_draw)

        plt.show()

    def savefig(self, filename):
        """
        save the canvas as an image file at filename)
        """
        # Draw only the unit box and flip the y axis
        plt.xlim((0, 1))
        plt.ylim((1, 0))

        ChiCanvas._on_draw(fig=self._figure, renderer=self._renderer)

        self._figure.savefig(filename)

    def close(self):
        """
        clean up a canvas
        """
        plt.close()

    # Auxiliary functions

    @classmethod
    def _auto_ellipsis_text(cls, textobj, renderer):
        """
        abbreviate text with ellipsis if necessary
        """
        try:
            clip = textobj._clip
        except AttributeError:
            return

        x0, _ = textobj.get_transform().transform(textobj.get_position())
        textobj.set_rotation_mode("anchor")
        rotation = textobj.get_rotation()
        assert rotation == 0
        buf = abs(x0 - clip.x0)
        new_width = abs(clip.x0 - clip.x1) - 2 * buf
        new_height = abs(clip.y1 - clip.y0)
        fontsize = textobj.get_size()
        pixels_per_char = 0.5 * renderer.points_to_pixels(fontsize)
        v_pixels_per_char = renderer.points_to_pixels(fontsize)
        try:
            txt = textobj._old_text
        except Exception:
            txt = textobj.get_text()
            textobj._old_text = txt
        wrap_width = new_width // pixels_per_char
        wrap_height = new_height // v_pixels_per_char
        clip_char = max(0, int(wrap_width * 0.9))
        max_lines = max(0, int(wrap_height * 0.8))
        if clip_char * max_lines < 4:
            wrapped_text = ""
        else:
            original_lines = txt.split("\n")
            lines = []
            for original in original_lines:
                lines.extend(textwrap.wrap(original, width=clip_char))
            wrapped_text = "\n".join(lines[:max_lines])
        textobj.set_text(wrapped_text)

    @classmethod
    def _on_draw(cls, event=None, fig=None, renderer=None):
        """
        Automatically put ellipsis after overflowing text
        """
        if event is not None:
            fig = event.canvas.figure
            renderer = event.renderer

        for ax in fig.axes:
            for artist in ax.get_children():
                if isinstance(artist, mpl.text.Text):
                    cls._auto_ellipsis_text(artist, renderer)

        if event is not None:
            func_handles = fig.canvas.callbacks.callbacks[event.name]
            fig.canvas.callbacks.callbacks[event.name] = {}
            fig.canvas.draw()
            fig.canvas.callbacks.callbacks[event.name] = func_handles


class ColorKey:
    NCOLORS = 512
    # Creates a color wheel of nice pastel colors
    COLORS = mpl.colors.hsv_to_rgb(
        np.vstack(
            [
                np.linspace(0, 1, NCOLORS),  # Hue
                0.4 * np.ones(NCOLORS),  # Saturation
                1.0 * np.ones(NCOLORS),  # Value
            ]
        ).T[np.newaxis]
    )[0]

    def __init__(self, codes):
        """
        construct a ColorKey with given codes

        Inputs:
            codes: (set of strings) set of keys to use for color map
        """
        self.color_map = {}
        incr = self.NCOLORS // len(codes)
        index = 0
        for code in sorted(codes):
            self.color_map[code] = ColorKey.COLORS[index]
            index = (index + incr) % self.NCOLORS

    def get_color(self, code):
        """
        get color for the specified code
        """
        return self.color_map.get(code, "gray")

    def get_color_by_index(self, i):
        """
        get color i spaces into list
        """
        return self.color_map.keys()[i]

    def draw_color_key(self, canvas, x0, y0, w, h, code_to_label=None):
        """
        draw color key in canvas from topleft corner (x0, y0) to
        bottomright corner (x0+w, y0+h).

        Inputs:
            canvas: ChiCanvas object
            x0, y0, x1, y1: floats with coordinates for points (x0, y0)
                and (x1, y1)

            code_to_label: (optional) maps codes to strings that will
               be used to identify the colors.
        """

        if not code_to_label:
            code_to_label = {}

        hincr = h / (len(self.color_map) * 1.0)
        x1 = x0 + w
        y = y0
        for code, color in sorted(self.color_map.items()):
            canvas.draw_rectangle(x0, y, x1, y + hincr, fill=color)
            canvas.draw_text(
                x0 + w / 2,
                y + hincr / 2,
                w * 0.95,
                h * 0.95,
                code_to_label.get(code, code),
            )
            y = y + hincr


def draw_rectangles(rectangles, color_codes, output_filename=None):
    """
    Draw rectangles on a canvas.  Either shows the resulting
    canvas (when output_filename is None) or saves it to a file.

    Args:
        rectangles (List[Rectangle]): the rectangles to draw
        color_codes (Set(str)): a set of possible codes
        output_filename (str): name of file in which to save the image.
            If None, displays the image instead. (Default: None)

    Returns (None): no return value
    """
    x_scale_factor = 12
    y_scale_factor = 10

    # Create the canvas to draw on
    c = ChiCanvas(x_scale_factor, y_scale_factor)

    # create the color key
    ck = ColorKey(color_codes)

    # draw the rectangles
    for rect in rectangles:
        rect.draw(c, ck)

    # save or show the result.
    if output_filename:
        print("saving...", output_filename)
        c.savefig(output_filename)
    else:
        c.show()
