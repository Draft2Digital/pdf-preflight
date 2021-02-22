from decimal import Decimal

import pikepdf

from pdf_preflight.issue import Issue
from .base_rule import Rule


class NoDevicen(Rule):
    """
    Check the target PDF doesn't use DeviceN colorspace (spot colors) since some print workflows forbid it
    """
    name = "NoDevicen"

    @classmethod
    def check(cls, pdf):
        issues = []

        for i, page in enumerate(pdf.pages):
            page_number = i + 1

            if cls._has_devicen_in_page_resources(page) or cls._has_devicen_in_xobjects(page):
                issues.append(Issue(
                    page=page_number,
                    rule=cls.name,
                    desc="Found DeviceN colorspace (spot color); DeviceN colors are prohibited."
                ))

        if len(issues) != 0:
            return issues

    @classmethod
    def _has_devicen_in_page_resources(cls, page):
        p = dict(page)
        if "/Resources" in p:
            r = dict(p["/Resources"])
            # colorspace defined in the page resources
            if "/ColorSpace" in r:
                cs = dict(r["/ColorSpace"])
                for k in cs.keys():
                    if k.startswith("/CS"):
                        try:
                            li = list(cs[k])
                        except:
                            # DeviceN colorspaces come in list form, if something isn't a list we skip it
                            pass
                        else:
                            if "/DeviceN" in li:
                                return True
                            elif li[0] == "/Indexed":
                                try:
                                    sublist = list(li[1])
                                except:
                                    # DeviceN colorspaces come in list form, if something isn't a list we skip it
                                    pass
                                else:
                                    if"/DeviceN" in sublist:
                                        return True

    @classmethod
    def _has_devicen_in_xobjects(cls, page):
        p = dict(page)
        if "/Resources" in p:
            r = dict(p["/Resources"])
            # colorspace defined on the object using it
            if "/XObject" in r:
                xo = dict(r["/XObject"])
                for k in xo.keys():
                    v = dict(xo[k])
                    if "/ColorSpace" in v:
                        cs = v["/ColorSpace"]
                        try:
                            li = list(cs)
                        except:
                            # DeviceN colorspaces come in list form, if something isn't a list we skip it
                            pass
                        else:
                            if "/DeviceN" in li:
                                return True
