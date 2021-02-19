from decimal import Decimal

import pikepdf

from pdf_preflight.issue import Issue
from .base_rule import Rule


class NoIndexedCmyk(Rule):
    """
    We don't currently have the ability to check the ink density of indexed cmyk colorspaces,
    so if we find one in a document that we intend to run the MaxInkDensity rule against,
    we have to reject the document.
    """
    name = "NoIndexedCmyk"

    @classmethod
    def check(cls, pdf):
        issues = []

        for i, page in enumerate(pdf.pages):
            page_number = i + 1

            p = dict(page)
            if "/Resources" in p:
                r = dict(p["/Resources"])
                # indexed cmyk colorspaces are defined in the page resources
                if "/ColorSpace" in r:
                    cs = dict(r["/ColorSpace"])
                    for k in cs.keys():
                        if k.startswith("/CS"):
                            try:
                                li = list(cs[k])
                            except:
                                # indexed CMYK colorspaces have a structure that can be cast to a list,
                                # so any colorspace that can't be cast to a list isn't what we're looking for
                                continue
                            else:
                                if "/Indexed" in list(cs[k]) and "/DeviceCMYK" in li:
                                    issues.append(Issue(
                                        page=page_number,
                                        rule=cls.name,
                                        desc=f"Indexed CMYK colorspaces are prohibited but one or more were found."
                                    ))

        if len(issues) != 0:
            return issues
