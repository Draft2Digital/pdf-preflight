from decimal import Decimal

import pikepdf

from pdf_preflight.issue import Issue
from .base_rule import Rule


class NoRgb(Rule):
    """
    Check the target PDF doesn't use RGB colorspace since some print workflows forbid it
    """
    name = "NoRgb"

    @classmethod
    def check(cls, pdf):
        issues = []

        for i, page in enumerate(pdf.pages):
            page_number = i + 1

            if (cls._has_rgb_in_page_resources(page) or
                    cls._has_rgb_in_xobjects(page) or
                    cls._has_rgb_in_content_stream(page)):
                issues.append(Issue(
                    page=page_number,
                    rule=cls.name,
                    desc="Found RGB colorspace; RGB colors are prohibited."
                ))

        if len(issues) != 0:
            return issues

    @classmethod
    def _has_rgb_in_page_resources(cls, page):
        p = dict(page)
        if "/Resources" in p:
            r = dict(p["/Resources"])
            if "/ColorSpace" in r:
                cs = dict(r["/ColorSpace"])
                for k in cs.keys():
                    if k.startswith("/CS"):
                        if cs[k] == "/DeviceRGB" or "/DeviceRGB" in list(cs[k]):
                            return True

    @classmethod
    def _has_rgb_in_xobjects(cls, page):
        p = dict(page)
        if "/Resources" in p:
            r = dict(p["/Resources"])
            # colorspace defined on the object using it
            if "/XObject" in r:
                xo = dict(r["/XObject"])
                for k in xo.keys():
                    v = dict(xo[k])
                    if "/ColorSpace" in v:
                        if v["/ColorSpace"] == "/DeviceRGB":
                            return True
    @classmethod
    def _has_rgb_in_content_stream(cls, page):
        for operands, operator in pikepdf.parse_content_stream(page):
            if str(operator) == "RG" or str(operator) == "rg":
                return True
