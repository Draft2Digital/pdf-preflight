from pdf_preflight.issue import Issue
from .base_rule import Rule


class BoxNesting(Rule):
    """
    For any page, MediaBox must be the biggest box, followed by the BleedBox, followed by the TrimBox or ArtBox.
    Boxes may be omitted, but if they're provided they must be correctly nested.
    """
    name = "BoxNesting"

    @classmethod
    def check(cls, pdf):
        issues = []
        for i, page in enumerate(pdf.pages):
            page_number = i + 1

            media = getattr(page, 'MediaBox', None)
            bleed = getattr(page, 'BleedBox', None)
            trim = getattr(page, 'TrimBox', None)
            art = getattr(page, 'ArtBox', None)

            if media and bleed and (bleed[2] > media[2] or bleed[3] > media[3]):
                issues.append(Issue(page=page_number, rule=cls.name, desc='BleedBox must be smaller than MediaBox'))
            elif trim and bleed and (trim[2] > bleed[2] or trim[3] > bleed[3]):
                issues.append(Issue(page=page_number, rule=cls.name, desc='TrimBox must be smaller than BleedBox'))
            elif art and bleed and (art[2] > bleed[2] or art[3] > bleed[3]):
                issues.append(Issue(page=page_number, rule=cls.name, desc='ArtBox must be smaller than BleedBox'))
            elif trim and media and (trim[2] > media[2] or trim[3] > media[3]):
                issues.append(Issue(page=page_number, rule=cls.name, desc='TrimBox must be smaller than MediaBox'))
            elif art and media and (art[2] > media[2] or art[3] > media[3]):
                issues.append(Issue(page=page_number, rule=cls.name, desc='ArtBox must be smaller than MediaBox'))

        if len(issues) != 0:
            return issues
