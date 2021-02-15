from pdf_preflight.issue import Issue
from .base_rule import Rule


class PdfxOutputIntentHasKeys(Rule):
    """
    All PDFX files MUST have a GTS_PDFX OutputIntent with certain keys.
    """
    name = "PdfxOutputIntentHasKeys"

    @classmethod
    def check(cls, pdf, entries=None):
        issues = []
        if not entries:
            entries = []

        root = pdf.Root
        if "/OutputIntents" in root.keys():
            intents = [intent for intent in pdf.Root.OutputIntents if intent["/S"] == "/GTS_PDFX"]
            for intent in intents:
                for key in entries:
                    if key not in intent.keys():
                        issues.append(Issue(
                            page="Metadata",
                            rule=cls.name,
                            desc=f"GTS_PDFX OutputIntent missing required key '{key}'."
                        ))
        else:
            issues.append(Issue(
                page="Metadata",
                rule=cls.name,
                desc=f"GTS_PDFX OutputIntent not found, assumed to be missing all required keys '{entries}'."
            ))

        if len(issues) != 0:
            return issues

    @classmethod
    def fix(cls, pdf, entries=None):
        # for each key that is missing (including /OutputIntents itself),
        #   find out the requirements for it and its appropriate value,
        #   generate them,
        #   and add them to the PDF
        # in this test, we are not bothered by the possibility of there being multiple OutputIntents,
        #   we simply add any missing keys to all of them and let the Other Rule do the freaking out if necessary
        super().fix(pdf)
