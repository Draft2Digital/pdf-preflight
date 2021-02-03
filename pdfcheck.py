import argparse
import sys

from pdf_preflight.profiles import Pdfx1a2003

issues, exceptions = Pdfx1a2003.run_preflight_checks(sys.argv[1])
if issues or exceptions:
    print(Pdfx1a2003.get_preflight_check_text(issues, exceptions))
else:
    print("Passed preflight")
