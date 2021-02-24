from decimal import Decimal

import pikepdf

from pdf_preflight.issue import Issue
from .base_rule import Rule


class NoIccColors(Rule):
    """
    Check the target PDF doesn't use ICCBased colorspaces, since some print workflows forbid it
    """
    name = "NoIccColors"

    @classmethod
    def check(cls, pdf):
        issues = []

        for i, page in enumerate(pdf.pages):
            page_number = i + 1

            if cls._has_icc_in_page_resources(page) or cls._has_icc_in_xobjects(page):
                issues.append(Issue(
                    page=page_number,
                    rule=cls.name,
                    desc="Found ICCBased colorspace; ICC profiles are prohibited."
                ))

        if len(issues) != 0:
            return issues

    @classmethod
    def _has_icc_in_page_resources(cls, page):
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
                            # ignore anything that can't become a list
                            pass
                        else:
                            if "/ICCBased" in li:
                                return True

                            try:
                                sublist = list(li[1])
                            except:
                                # ignore any cases where the second element isn't a list
                                pass
                            else:
                                if li[0] == "/Indexed" and "/ICCBased" in sublist:
                                    return True

    @classmethod
    def _has_icc_in_xobjects(cls, page):
        p = dict(page)
        if "/Resources" in p:
            r = dict(p["/Resources"])
            if "/XObject" in r:
                xo = dict(r["/XObject"])
                for k in xo.keys():
                    v = dict(xo[k])
                    if "/ColorSpace" in v:
                        cs = v["/ColorSpace"]
                        try:
                            li = list(cs)
                        except:
                            # ignore any cases where it isn't a list
                            pass
                        else:
                            if "/ICCBased" in li:
                                return True
