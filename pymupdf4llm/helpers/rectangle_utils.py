from typing import TypeAlias

from .._pymupdf import pymupdf

RectOrTuple: TypeAlias = tuple[float, float, float, float] | pymupdf.Rect


def is_inside(rect1: RectOrTuple, rect2: RectOrTuple):
    """
    Determines if rect1 is completely inside rect2.

    :param rect1: Tuple of coordinates (x0, y0, x1, y1) representing the first rectangle
    :param rect2: Tuple of coordinates (x0, y0, x1, y1) representing the second rectangle
    :return: True if rect1 is completely inside rect2, False otherwise
    """
    x0_1, y0_1, x1_1, y1_1 = rect1
    x0_2, y0_2, x1_2, y1_2 = rect2

    return x0_2 <= x0_1 <= x1_1 <= x1_2 and y0_2 <= y0_1 <= y1_1 <= y1_2


def is_in_rects(rect: RectOrTuple, rect_list: list[RectOrTuple]):
    """
    Check if rect is contained in a rect of the list.
    Return the index + 1 of the container rect.
    """
    for i, r in enumerate(rect_list, start=1):
        if is_inside(rect, r):
            return i
    return 0


def intersects_rects(rect: RectOrTuple, rect_list: list[RectOrTuple]):
    """
    Check if rect intersects with any rect of the list.
    Return the index + 1 of the first intersecting rect.
    """
    for i, r in enumerate(rect_list, start=1):
        if do_intersects(rect, r):
            return i
    return 0


def do_intersects(rect1: RectOrTuple, rect2: RectOrTuple):
    """
    Determines if two rectangles intersect.

    :param rect1: Tuple of coordinates (x0, y0, x1, y1) representing the first rectangle
    :param rect2: Tuple of coordinates (x0, y0, x1, y1) representing the second rectangle
    :return: True if the rectangles intersect, False otherwise
    """
    x0_1, y0_1, x1_1, y1_1 = rect1
    x0_2, y0_2, x1_2, y1_2 = rect2

    # Check if one rectangle is to the left of the other
    if x1_1 <= x0_2 or x1_2 <= x0_1:
        return False

    # Check if one rectangle is above the other
    if y1_1 <= y0_2 or y1_2 <= y0_1:
        return False

    return True


def intersects_over_x(rect1: pymupdf.Rect, rect2: pymupdf.Rect):
    """
    Check if rect1 and rect2 intersect over x-axis.
    Actual meaning: one under the other.
    Return True if they intersect over x-axis.

        rect1: x0--------------x1
        rect2:          x0---------------x1
         or
        rect1:          x0---------------x1
        rect2: x0--------------x1
         or
        rect1: x0--------------x1
        rect2: x0--------------x1
         or
        rect1:          x0---------------x1
        rect2:             x0----------x1

         but
        rect1: x0--------------x1
        rect2:                   x0----------x1
    """

    return not (rect1.x1 < rect2.x0 or rect2.x1 < rect1.x0)


def intersects_over_y(rect1: pymupdf.Rect, rect2: pymupdf.Rect):
    """
    Check if rect1 and rect2 intersect over y-axis.
    Actual meaning: one beside the other.
    Return True if they intersect over y-axis.

        react1:           rect2
          y0
          |
          |
          |                y0
         y1                 |
                            |
                            |
                            |
                            y1
    """

    return not (rect1.y1 < rect2.y0 or rect2.y1 < rect1.y0)


def any_rect_between_over_y(
    rect1: pymupdf.Rect, rect2: pymupdf.Rect, rect_list: list[pymupdf.Rect]
):
    """
    Check if any rect of the list is between rect1 and rect2.
    Return the index + 1 of the first rect between rect1 and rect2.
    """

    for i, r in enumerate(rect_list, start=1):
        # check if r actually under some rect
        if intersects_over_x(rect1, r) or intersects_over_x(rect2, r):
            if rect1.y0 < r.y0 < rect2.y0:
                return i
    return 0


def any_rect_between_over_x(
    rect1: pymupdf.Rect, rect2: pymupdf.Rect, rect_list: list[pymupdf.Rect]
):
    """
    Check if any rect of the list is between rect1 and rect2.
    Return the index + 1 of the first rect between rect1 and rect2.
    """

    for i, r in enumerate(rect_list, start=1):
        # check if r actually under some rect
        if intersects_over_y(rect1, r) or intersects_over_y(rect2, r):
            if rect1.x0 < r.x0 < rect2.x0:
                return i
    return 0
