from pdf_preflight.issue import Issue
from .base_rule import Rule


class MaxVersion(Rule):
    """
    Check that the PDF version of the file under review is not more recent than desired
    """
    name = "MaxVersion"

    @classmethod
    def check(cls, pdf, max_version=None):
        issues = []

        if max_version and float(pdf.pdf_version) > float(max_version):
            issues.append(Issue(
                page="Metadata",
                rule=cls.name,
                desc=f"PDF version should be {max_version} or lower."
            ))
        elif max_version is None:
            raise Exception("Rule 'MaxVersion' requires max_version argument but none was provided.")

        if len(issues) != 0:
            return issues
