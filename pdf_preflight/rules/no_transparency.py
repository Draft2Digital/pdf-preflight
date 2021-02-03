from decimal import Decimal

from pdf_preflight.issue import Issue
from .base_rule import Rule


class NoTransparency(Rule):
    """
    Check the target PDF doesn't use transparent objects since some print workflows forbid it
    """
    name = "NoTransparency"

    @classmethod
    def check(cls, pdf):
        issues = []

        for i, page in enumerate(pdf.pages):
            page_number = i + 1

            if cls._has_transparency(page):
                issues.append(Issue(
                    page=page_number,
                    rule=cls.name,
                    desc="Found object with transparency; transparent objects are prohibited."
                ))

        if len(issues) != 0:
            return issues

    @classmethod
    def _has_transparency(cls, page):
        if cls._has_transparent_group(page):
            return True
        else:
            p = dict(page)
            for key in p:
                if not isinstance(p[key], str) and not isinstance(p[key], int) and not isinstance(p[key], Decimal):
                    val = dict(p[key])
                    if "/Kids" in val:
                        kids = list(val["/Kids"])
                        for kid in kids:
                            if cls._has_transparent_group(kid):
                                return True
            return False

    @classmethod
    def _has_transparent_group(cls, obj):
        p = dict(obj)
        if "/Group" in p:  # Can objects other than Groups have transparency?
            g = p["/Group"]
            if g.get("/S") == "/Transparency":
                return True
