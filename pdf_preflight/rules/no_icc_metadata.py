from decimal import Decimal

import pikepdf

from pdf_preflight.issue import Issue
from .base_rule import Rule


class NoIccMetadata(Rule):
    """
    Check the target PDF doesn't use ICC profiles in its OutputIntents
    """
    name = "NoIccMetadata"

    @classmethod
    def check(cls, pdf):
        issues = []

        for page in pdf.pages:
            if cls._has_icc_in_root(pdf):
                issues.append(Issue(
                    page="Metadata",
                    rule=cls.name,
                    desc="Found ICC profile in document OutputIntents; ICC profiles are prohibited."
                ))

        if len(issues) != 0:
            return issues

    @classmethod
    def _has_icc_in_root(cls, pdf):
        root = pdf.Root
        if "/OutputIntents" in root.keys():
            intents = list(root.OutputIntents)
            for intent in intents:
                i = dict(intent)
                if "/RegistryName" in i and i["/RegistryName"] == "http://www.color.org":
                    # http://www.color.org is where the ICC maintains its list of registered profiles.
                    # PDF/X requires profiles from that list to be referenced by that URL.
                    # We are assuming here that if we see that RegistryName, there is an ICC profile being used,
                    # and if we don't see it then there isn't one.
                    # That could be a big assumption, but if this rule is used only in situations that already
                    # expect PDF/X compliance, it should be ok.
                    return True
