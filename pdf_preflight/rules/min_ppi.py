from math import hypot
from decimal import Decimal, ROUND_DOWN

import pikepdf

from pdf_preflight.issue import Issue
from pdf_preflight.measurement_conversions import pt2in
from .base_rule import Rule


class MinPpi(Rule):
    """
    Check that the file contains no images with a points-per-inch below the provided threshold.
    """
    name = "MinPpi"

    @classmethod
    def check(cls, pdf, threshold=0):
        issues = []

        for i, page in enumerate(pdf.pages):
            page_number = i + 1

            images = cls._get_all_images_on_page(page)
            image_matrices = cls._get_all_image_matrices_on_page(page)
            for index in range(len(images)):
                if cls._image_has_low_ppi(images[index], image_matrices[index], threshold):
                    issues.append(Issue(
                        page=page_number,
                        rule=cls.name,
                        desc=f"Found low-resolution image; images must be at least {threshold} ppi."
                    ))

        if len(issues) != 0:
            return issues

    @classmethod
    def _get_all_images_on_page(cls, page):
        images = []
        p = dict(page)
        if "/Resources" in p:
            r = dict(p["/Resources"])
            if "/XObject" in r:
                xo = dict(r["/XObject"])
                for k in xo.keys():
                    v = dict(xo[k])
                    if "/Subtype" in v and v["/Subtype"] == "/Image" and "/Height" in v and "/Width" in v:
                        images.append(v)
        return images

    @classmethod
    def _get_all_image_matrices_on_page(cls, page):
        image_matrices = []
        for operands, operator in pikepdf.parse_content_stream(page):
            if str(operator) == "cm":
                m = pikepdf.PdfMatrix(operands)
                image_matrices.append(m)
        return image_matrices

    @classmethod
    def _image_has_low_ppi(cls, image, matrix, threshold):
        sample_height = image["/Height"]
        sample_width = image["/Width"]
        display_width, display_height = cls._get_display_dimensions_in_inches(matrix)

        vertical_ppi = Decimal(sample_height / display_height)
        horizontal_ppi = Decimal(sample_width / display_width)

        return horizontal_ppi < threshold or vertical_ppi < threshold

    @classmethod
    def _get_display_dimensions_in_inches(cls, matrix):
        bottom_left = cls._calc_corner(matrix, 0, 0)
        top_left = cls._calc_corner(matrix, 0, 1)
        bottom_right = cls._calc_corner(matrix, 1, 0)

        display_width = pt2in(hypot(bottom_left[0] - bottom_right[0], bottom_left[1] - bottom_right[1]))
        display_height = pt2in(hypot(bottom_left[0] - top_left[0], bottom_left[1] - top_left[1]))

        return display_width, display_height

    @classmethod
    def _calc_corner(cls, matrix, x, y):
        corner_x = (matrix.a * x) + (matrix.c * y) + matrix.e
        corner_y = (matrix.b * x) + (matrix.d * y) + matrix.f
        return corner_x, corner_y
