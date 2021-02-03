from pdf_preflight.issue import Issue
from .base_rule import Rule


class DocumentId(Rule):
    """
    Check that the file has a document ID
    """
    name = "DocumentId"

    @classmethod
    def check(cls, pdf):
        issues = []

        if "/ID" not in pdf.trailer.keys() or pdf.trailer["/ID"] is None:
            issues.append(Issue(
                page="Metadata",
                rule=cls.name,
                desc=f"Document ID missing."
            ))

        if len(issues) != 0:
            return issues
