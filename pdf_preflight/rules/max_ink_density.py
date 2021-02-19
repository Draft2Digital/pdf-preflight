import pikepdf

from decimal import Decimal

from pdf_preflight.issue import Issue
from .base_rule import Rule


class MaxInkDensity(Rule):
    """
    Most CMYK printers will have a stated upper tolerance for ink density. If
    the total percentage of the 4 components (C, M, Y and K) is over that
    tolerance then the result can be unpredictable and often ugly.

    Detect CMYK ink densities over a certain threshold.
    """
    name = "MaxInkDensity"

    @classmethod
    def check(cls, pdf, threshold=None):
        issues = []

        if threshold is None:
            raise Exception("Rule 'MaxInkDensity' requires threshold argument but none was provided.")

        for i, page in enumerate(pdf.pages):
            page_number = i + 1

            bad_resources = cls._check_page_resources(page, threshold)
            bad_images = cls._check_page_images(page, threshold)
            bad_stream = cls._check_content_stream(page, threshold)

            if threshold and (bad_resources or bad_images or bad_stream):
                issues.append(Issue(
                    page=page_number,
                    rule=cls.name,
                    desc=f"CMYK ink density too high; must not exceed {threshold}%"
                ))

        if len(issues) != 0:
            return issues

    @classmethod
    def _check_page_resources(cls, page, threshold):
        p = dict(page)
        if "/Resources" in p:
            r = dict(p["/Resources"])
            if "/ColorSpace" in r:
                cs = dict(r["/ColorSpace"])
                for k in cs.keys():
                    if k.startswith("/CS"):
                        try:
                            li = list(cs[k])
                        except:
                            # If the colorspace can't be cast to a list, it's either the pdf-name "/DeviceCMYK"
                            # or something we don't care about. Neither case is cause to raise an exception.
                            li = []
                        else:
                            # ignore indexed colorspaces; they're prohibited, but the NoIndexedCmyk rule catches them
                            if cs[k] == "/DeviceCMYK" or ("/DeviceCMYK" in li and "/Indexed" not in li):
                                # search the content stream for a reference to the colorspace we just found
                                found_colorspace = False
                                for operands, operator in pikepdf.parse_content_stream(page):
                                    if str(operator) in ["cs", "CS"] and k in operands:
                                        found_colorspace = True
                                    elif found_colorspace and str(operator) in ["scn", "SCN"]:
                                        density = Decimal("0")
                                        for op in operands:
                                            density += Decimal(op)
                                        if (density * Decimal("100")) > Decimal(threshold):
                                            return True

    @classmethod
    def _check_page_images(cls, page, threshold):
        images = page.images
        for k in images.keys():
            img = pikepdf.PdfImage(images[k])
            cur_img = img.as_pil_image()
            if str(cur_img.mode) != "CMYK":
                cur_img.convert("CMYK")
            # get the list of pixels as 4-tuples
            pixels = list(cur_img.getdata())
            for pixel in pixels:
                density = Decimal("0")
                for val in pixel:
                    # each pixel is a tuple of four ints, each in the range 0..255
                    # we need to squish each int into the range 0..1 to make the calculation work
                    density += Decimal(val) / Decimal("255")
                if (density * Decimal("100")) > Decimal(threshold):
                    return True

    @classmethod
    def _check_content_stream(cls, page, threshold):
        for operands, operator in pikepdf.parse_content_stream(page):
            if str(operator) == "K" or str(operator) == "k":
                density = Decimal("0")
                for op in operands:
                    density += Decimal(op)
                if (density * Decimal("100")) > Decimal(threshold):
                    return True
