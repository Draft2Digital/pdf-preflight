from pdf_preflight.issue import Issue
from .base_rule import Rule


class OnlyEmbeddedFonts(Rule):
    """
    Check that the target PDF only uses embedded fonts.
    """
    name = "OnlyEmbeddedFonts"

    @classmethod
    def check(cls, pdf):
        issues = []
        for i, page in enumerate(pdf.pages):
            page_number = i + 1

            fonts = cls._get_fonts_for_page(page)
            if fonts:
                for key in fonts:
                    if not cls._is_embedded(fonts[key]):
                        issues.append(Issue(
                            page=page_number,
                            rule=cls.name,
                            desc="All fonts must be embedded; found non-embedded font."))

        if len(issues) != 0:
            return issues

    @classmethod
    def _get_fonts_for_page(cls, page):
        p = dict(page)
        if "/Resources" in p:
            r = dict(p["/Resources"])
            if "/Font" in r:
                f = dict(r["/Font"])
                return f

    @classmethod
    def _is_embedded(cls, font):
        if font["/Subtype"] == "Type3":
            return True
        elif "/FontDescriptor" in font.keys():
            descriptor = dict(font["/FontDescriptor"])
            if ("/FontFile" in descriptor.keys() or
                    "/FontFile2" in descriptor.keys() or
                    "/FontFile3" in descriptor.keys()):
                return True
        elif font["/Subtype"] == "Type0":
            descendants = dict(font["/DescendantFonts"])
            for key in descendants:
                return cls._is_embedded(descendants[key])
        else:
            return False
