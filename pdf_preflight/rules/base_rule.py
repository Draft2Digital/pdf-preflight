from pdf_preflight.issue import Issue


class Rule:
    name = "Base Rule Class"

    @classmethod
    def check(cls, pdf):
        issues = []

        issues.append(Issue(
            page=0,
            rule=cls.name,
            desc=("Every subclass of Rule must define its own 'check()' method,"
                  "which should return a list of Issues (or None if no issues were found)")
        ))

        if len(issues) != 0:
            return issues
