from decimal import Decimal

from pdf_preflight.issue import Issue
from .base_rule import Rule


class NoFilespecs(Rule):
    """
    Check the target PDF doesn't use Filespecs to refer to external files.
    """
    name = "NoFilespecs"

    @classmethod
    def check(cls, pdf):
        issues = []

        if cls._has_filespecs(pdf):
            issues.append(Issue(
                page="Metadata",
                rule=cls.name,
                desc="Found one or more filespecs; use of filespecs to reference external files is prohibited."
            ))

        if len(issues) != 0:
            return issues

    @classmethod
    def _has_filespecs(cls, pdf):
        for obj in pdf.objects:
            if (not isinstance(obj, str) and
                    not isinstance(obj, int) and
                    not isinstance(obj, Decimal) and
                    not isinstance(obj, list)):
                if "/Type" in obj.keys() and obj["/Type"] == "/Filespec":
                    return True
