from pdf_preflight.issue import Issue
from .base_rule import Rule


class RootHasKeys(Rule):
    """
    Every PDF has a 'Root' dictionary.
    Check that the target file has certain keys.
    """
    name = "RootHasKeys"

    @classmethod
    def check(cls, pdf, entries=None):
        issues = []
        if not entries:
            entries = []

        root = pdf.Root
        for k in entries:
            if k not in root:
                issues.append(Issue(
                    page="Metadata",
                    rule=cls.name,
                    desc=f"Root dict missing required key '{k}'"
                ))

        if len(issues) != 0:
            return issues

    @classmethod
    def fix(cls, pdf, entries=None):
        # for each key that is missing,
        #   find out the requirements for it and its appropriate value,
        #   generate them,
        #   and add them to the PDF
        super().fix(pdf)
