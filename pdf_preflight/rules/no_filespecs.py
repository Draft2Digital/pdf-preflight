import pikepdf

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
            if obj is not None and isinstance(obj, pikepdf.objects.Object):
                obj = dict(obj)
                if obj.get("/Type") == "/Filespec":
                    return True
