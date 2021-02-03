import itertools
import traceback

import pikepdf

from pdf_preflight.issue import Issue


class Profile:
    rules = []

    @classmethod
    def get_preflight_check_text(cls, issues, exceptions):
        if issues or exceptions:
            exception_text = f"PDF failed Preflight checks with the following Issues & exceptions:\n"

            if issues:
                exception_text += "ISSUES:\n"
                combined_issues = cls._combine_similar_issues(issues)
                for i in combined_issues:
                    if i.page == "Metadata":
                        exception_text += f"Rule '{i.rule}' found an error in document metadata: {i.desc}\n"
                    else:
                        exception_text += f"Rule '{i.rule}' found an error on page {i.page}: {i.desc}\n"

            if exceptions:
                exception_text += "EXCEPTIONS:\n"
                for e in exceptions:
                    exception_text += e + "\n"
            return exception_text

    @classmethod
    def check_preflight(cls, file):
        issues, exceptions = cls.run_preflight_checks(file)
        if issues or exceptions:
            exception_text = cls.get_preflight_check_text(issues, exceptions)
            raise Exception(exception_text)

    @classmethod
    def run_preflight_checks(cls, file):
        issues = []
        exceptions = []
        with pikepdf.open(file) as pdf:
            for row in cls.rules:
                rule = row[0]
                args = row[1:]
                i, e = cls._run_rule(rule, pdf, *args)
                issues += i
                exceptions += e
        return issues, exceptions

    @classmethod
    def _run_rule(cls, rule, pdf, *args):
        issues = []
        exceptions = []
        try:
            result = rule.check(pdf, *args)
            if result:
                issues += result
        except Exception:
            exception_string = traceback.format_exc()
            exceptions.append(exception_string)
        return issues, exceptions

    @classmethod
    def _combine_similar_issues(cls, issues):
        combined_issues = []
        key = lambda i: (i.rule, i.desc)
        for k, g in itertools.groupby(sorted(issues, key=key), key=key):
            g = list(g)
            first = g[0]
            last = g[len(g) - 1]

            if first.page == "Metadata" or first.page == last.page:
                pages = first.page
            else:
                pages = str(first.page) + "-" + str(last.page)

            issue = Issue(
                rule=first.rule,
                page=pages,
                desc=first.desc
            )
            combined_issues.append(issue)
        return combined_issues
