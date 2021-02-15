import re

from pdf_preflight.issue import Issue
from .base_rule import Rule


class MatchInfoEntries(Rule):
    """
    Every PDF has an optional 'Info' dictionary.
    Check that the target file has certain keys and that their values match a given regex.
    """
    name = "MatchInfoEntries"

    @classmethod
    def check(cls, pdf, entries=None):
        issues = []
        if not entries:
            entries = {}

        info = pdf.docinfo
        for k, v in entries.items():
            if k not in info:
                issues.append(Issue(
                    page="Metadata",
                    rule=cls.name,
                    desc=f"Info dict missing required key '{k}'"
                ))
            elif not re.fullmatch(v, str(info[k])):
                issues.append(Issue(
                    page="Metadata",
                    rule=cls.name,
                    desc=f"Value of Info entry '{k}' doesn't match regex '{v}'"
                ))

        if len(issues) != 0:
            return issues

    @classmethod
    def fix(cls, pdf, entries=None):
        # for each key or key-value that is missing,
        #   find out the requirements for the key and its appropriate value,
        #   generate whatever part of them is missing,
        #   and add that to the PDF
        super().fix(pdf)
