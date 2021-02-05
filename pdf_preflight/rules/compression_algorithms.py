from decimal import Decimal

import pikepdf

from pdf_preflight.issue import Issue
from pdf_preflight.rules.base_rule import Rule


class CompressionAlgorithms(Rule):
    """
    Check that a file doesn't use unwanted compression algorithms.
    """
    name = "CompressionAlgorithms"

    @classmethod
    def check(cls, pdf, allowed_algorithms=None):
        issues = []
        if not allowed_algorithms:
            allowed_algorithms = []

        banned_algorithms = cls._find_banned_algorithms(pdf, allowed_algorithms)
        for algorithm in banned_algorithms:
            issues.append(Issue(
                page="Metadata",
                rule=cls.name,
                desc=f"File uses unwanted compression algorithm: '{algorithm}'"
            ))

        if len(issues) != 0:
            return issues

    @classmethod
    def _find_banned_algorithms(cls, pdf, allowed_algorithms):
        banned_algorithms = []

        all_algorithms = []
        for obj in pdf.objects:
            if obj is not None and isinstance(obj, pikepdf.objects.Object):
                obj = dict(obj)
                if "/Filter" in obj:
                    result = obj["/Filter"]
                    if isinstance(result, pikepdf.Name):  # we only found one
                        all_algorithms.append(str(result))
                    else:
                        all_algorithms += [str(x) for x in result]

        for algorithm in all_algorithms:
            if (algorithm not in allowed_algorithms and
                    algorithm not in banned_algorithms):  # don't allow duplicate list entries
                banned_algorithms.append(algorithm)

        return banned_algorithms
