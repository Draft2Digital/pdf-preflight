from pdf_preflight.issue import Issue
from .base_rule import Rule


class OutputIntentForPdfx(Rule):
    """
    Check the target PDF contains an output intent suitable for PDFX.
    """
    name = "OutputIntentForPdfx"

    @classmethod
    def check(cls, pdf):
        issues = []

        root = pdf.Root
        if "/OutputIntents" not in root.keys():
            issues.append(Issue(
                page="Metadata",
                rule=cls.name,
                desc=f"OutputIntent with subtype '/GTS_PDFX' is required but was not found."
            ))
        else:
            intents = [oi for oi in root.OutputIntents if oi["/S"] == "/GTS_PDFX"]
            if len(intents) != 1:
                issues.append(Issue(
                    page="Metadata",
                    rule=cls.name,
                    desc=f"Exactly one OutputIntent with subtype '/GTS_PDFX' is required; found multiple."
                ))

        if len(issues) != 0:
            return issues
