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
                for f in fonts:
                    font = fonts[f]
                    if not cls._is_embedded(font):
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
        if font.get("/Subtype") == "/Type3":
            return True
        elif font.get("/FontDescriptor"):
            descriptor = font["/FontDescriptor"]
            if descriptor and ("/FontFile" in descriptor or "/FontFile2" in descriptor or "/FontFile3" in descriptor):
                return True
        elif font.get("/Subtype") == "/Type0":
            descendants = font["/DescendantFonts"]
            for d in descendants:
                return cls._is_embedded(d)
        else:
            return False
