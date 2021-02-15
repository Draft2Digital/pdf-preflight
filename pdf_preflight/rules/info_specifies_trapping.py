import pikepdf

from pdf_preflight.issue import Issue
from .base_rule import Rule


class InfoSpecifiesTrapping(Rule):
    """
    Every PDF has an optional 'Info' dictionary.
    Check that the dictionary has a 'Trapped' entry that is set to either True or False.
    """
    name = "InfoSpecifiesTrapping"

    @classmethod
    def check(cls, pdf):
        issues = []

        info = pdf.docinfo
        if "/Trapped" not in info.keys():
            issues.append(Issue(
                page="Metadata",
                rule=cls.name,
                desc="Info dict missing required key '/Trapped'."
            ))
        elif info["/Trapped"] != "/True" and info["/Trapped"] != "/False":
            issues.append(Issue(
                page="Metadata",
                rule=cls.name,
                desc="Value of Info entry '/Trapped' must be True or False."
            ))

        if len(issues) != 0:
            return issues

    @classmethod
    def fix(cls, pdf):
        info = pdf.docinfo
        if "/Trapped" not in info or (info["/Trapped"] != "/True" and info["/Trapped"] != "/False"):
            info["/Trapped"] = "/False"
