from pdf_preflight.issue import Issue
from .base_rule import Rule


class PrintBoxes(Rule):
    """
    For PDFX/1a, every page must have MediaBox, plus either ArtBox or TrimBox (TrimBox is preferred).
    """
    name = "PrintBoxes"

    @classmethod
    def check(cls, pdf):
        issues = []
        for i, page in enumerate(pdf.pages):
            page_number = i + 1

            media = getattr(page, "MediaBox", None)
            trim = getattr(page, "TrimBox", None)
            art = getattr(page, "ArtBox", None)

            if not media:
                issues.append(Issue(
                    page=page_number,
                    rule=cls.name,
                    desc="MediaBox is required but was not found."))
            elif not trim and not art:
                issues.append(Issue(
                    page=page_number,
                    rule=cls.name,
                    desc="ArtBox or TrimBox is required, but neither was found; TrimBox is preferred."))
            elif trim and art:
                issues.append(Issue(
                    page=page_number,
                    rule=cls.name,
                    desc="A page cannot have both ArtBox and TrimBox, but both were found; TrimBox is preferred"))

        if len(issues) != 0:
            return issues
