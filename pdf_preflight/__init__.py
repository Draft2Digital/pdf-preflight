import os
import re
import subprocess
from collections import defaultdict

from d2dutils import os_utils

RUBY_PREFLIGHT_MAIN_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'ruby-preflight', 'lib', 'main.rb'
)


def run_pdf_preflight_checks_from_file(file_obj):
    with os_utils.temporary_file() as pdf_file:
        pdf_file.write(file_obj.read())
        pdf_file.seek(0)
        results, stderr = run_pdf_preflight_checks_from_filename(pdf_file.name)
    file_obj.seek(0)
    return results, stderr


def run_pdf_preflight_checks_from_filename(filename):
    cmd = ['ruby', RUBY_PREFLIGHT_MAIN_PATH, filename]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')

    issues = stdout[2:-1].replace('\n', '').split(', #')
    if issues == ['']:
        return {}, stderr

    results = defaultdict(list)
    for issue in issues:
        rule, attributes = parse_issue(issue)
        results[rule].append(attributes)

    return results, stderr


def parse_issue(issue):
    description = re.search('@description=\"([^"]+)\"', issue).group(1)
    rule = re.search('@rule=:"Preflight::Rules::([a-zA-Z]+)"', issue).group(1)
    if '@attributes={}' in issue:
        attributes = {}
    else:
        attributes_str = re.search('@attributes={([^}]+)}', issue).group(1)
        attributes = {}
        for attr in attributes_str.split(', '):
            key, value = attr.split('=>')
            attributes[key.replace(':', '')] = value.replace(':', '')

    return f'{rule}: {description}', attributes
