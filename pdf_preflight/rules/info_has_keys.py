from pdf_preflight.issue import Issue
from .base_rule import Rule


class InfoHasKeys(Rule):
    """
    Every PDF has an optional 'Info' dictionary.
    Check that the target file has certain keys.
    """
    name = "InfoHasKeys"

    @classmethod
    def check(cls, pdf, entries=None):
        issues = []
        if not entries:
            entries = []

        info = pdf.docinfo
        for k in entries:
            if k not in info:
                issues.append(Issue(
                    page="Metadata",
                    rule=cls.name,
                    desc=f"Info dict missing required key '{k}'"
                ))

        if len(issues) != 0:
            return issues

    @classmethod
    def fix(cls, pdf):
        # for each key that is missing,
        #   find out the requirements for it and its appropriate value,
        #   generate them,
        #   and add them to the PDF
        super().fix(pdf)
