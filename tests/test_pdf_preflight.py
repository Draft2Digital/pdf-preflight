import io
import json
import os
import unittest
import pdf_preflight

data_folder = os.path.join(os.path.dirname(__file__), 'data')


class TestPdfPreflight(unittest.TestCase):

    @staticmethod
    def load(filename):
        with open(os.path.join(data_folder, filename), mode='rb') as f:
            return f.read()

    def test_run_pdf_preflight_checks_from_file(self):
        # passing file obj
        file_obj = io.BytesIO(self.load('passes-9781393996651.pdf'))
        issues, stderr = pdf_preflight.run_pdf_preflight_checks_from_file(file_obj)
        self.assertEqual('', stderr)
        self.assertEqual({}, issues)

        # failing file obj
        file_obj = io.BytesIO(self.load('9780973568875.pdf'))
        issues, stderr = pdf_preflight.run_pdf_preflight_checks_from_file(file_obj)
        self.assertEqual('', stderr)
        expected = json.loads(self.load('9780973568875-results.json'))
        self.assertEqual(expected, issues)

    def test_run_pdf_preflight_checks_from_filename__interior_passes(self):
        interior = os.path.join(data_folder, 'passes-9781393996651.pdf')
        issues, stderr = pdf_preflight.run_pdf_preflight_checks_from_filename(interior)
        self.assertEqual('', stderr)
        self.assertEqual({}, issues)

    def test_run_pdf_preflight_checks_from_filename__cover_passes(self):
        cover = os.path.join(data_folder, 'cover-passes-9781393996651.pdf')
        issues, stderr = pdf_preflight.run_pdf_preflight_checks_from_filename(cover)
        self.assertEqual('', stderr)
        self.assertEqual({}, issues)

    def test_run_pdf_preflight_checks_from_filename__interior_issues(self):
        interior_with_issues = os.path.join(data_folder, '9780973568875.pdf')
        issues, stderr = pdf_preflight.run_pdf_preflight_checks_from_filename(interior_with_issues)
        self.assertEqual('', stderr)
        expected = json.loads(self.load('9780973568875-results.json'))
        self.assertEqual(expected, issues)

    def test_run_pdf_preflight_checks_from_filename__cover_issues(self):
        cover_with_issues = os.path.join(data_folder, '9781989351291-cover.pdf')
        issues, stderr = pdf_preflight.run_pdf_preflight_checks_from_filename(cover_with_issues)
        self.assertEqual('', stderr)
        expected = json.loads(self.load('9781989351291-results.json'))
        self.assertEqual(expected, issues)

    def test_parse_issue(self):
        issue = '<Preflight::Issue:0x00000000028f85e8 @description="every page must have either an ArtBox or a TrimBox", @rule=:"Preflight::Rules::PrintBoxes", @attributes={:page=>352}>'
        expected_rule = 'PrintBoxes: every page must have either an ArtBox or a TrimBox'
        expected_attrs = {'page': '352'}
        rule, attrs = pdf_preflight.parse_issue(issue)
        self.assertEqual(expected_rule, rule)
        self.assertEqual(expected_attrs, attrs)

        issue = '<Preflight::Issue:0x00000000028d7208 @description="Info dict missing required key", @rule=:"Preflight::Rules::MatchInfoEntries", @attributes={:key=>:GTS_PDFXVersion}>'
        expected_rule = 'MatchInfoEntries: Info dict missing required key'
        expected_attrs = {'key': 'GTS_PDFXVersion'}
        rule, attrs = pdf_preflight.parse_issue(issue)
        self.assertEqual(expected_rule, rule)
        self.assertEqual(expected_attrs, attrs)

        issue = '<Preflight::Issue:0x00000000028d6a88 @description="Root dict missing required key OutputIntents", @rule=:"Preflight::Rules::RootHasKeys", @attributes={:key=>:OutputIntents}>'
        expected_rule = 'RootHasKeys: Root dict missing required key OutputIntents'
        expected_attrs = {'key': 'OutputIntents'}
        rule, attrs = pdf_preflight.parse_issue(issue)
        self.assertEqual(expected_rule, rule)
        self.assertEqual(expected_attrs, attrs)

        issue = '<Preflight::Issue:0x00000000028d62e0 @description="Info dict missing required key", @rule=:"Preflight::Rules::InfoHasKeys", @attributes={:key=>:Title}>'
        expected_rule = 'InfoHasKeys: Info dict missing required key'
        expected_attrs = {'key': 'Title'}
        rule, attrs = pdf_preflight.parse_issue(issue)
        self.assertEqual(expected_rule, rule)
        self.assertEqual(expected_attrs, attrs)

        issue = '<Preflight::Issue:0x00000000028d5d18 @description="Info dict does not specify Trapped", @rule=:"Preflight::Rules::InfoSpecifiesTrapping", @attributes={}>'
        expected_rule = 'InfoSpecifiesTrapping: Info dict does not specify Trapped'
        expected_attrs = {}
        rule, attrs = pdf_preflight.parse_issue(issue)
        self.assertEqual(expected_rule, rule)
        self.assertEqual(expected_attrs, attrs)

        issue = '<Preflight::Issue:0x0000000002598f38 @description="PDF version should be 1.4 or lower", @rule=:"Preflight::Rules::MaxVersion", @attributes={:max_version=>1.4, :current_version=>1.7}>'
        expected_rule = 'MaxVersion: PDF version should be 1.4 or lower'
        expected_attrs = {'max_version': '1.4', 'current_version': '1.7'}
        rule, attrs = pdf_preflight.parse_issue(issue)
        self.assertEqual(expected_rule, rule)
        self.assertEqual(expected_attrs, attrs)

        issue = '<Preflight::Issue:0x0000000002598380 @description="There must be exactly 1 OutputIntent with a subtype of GTS_PDFX", @rule=:"Preflight::Rules::OutputIntentForPdfx", @attributes={}>]'
        expected_rule = 'OutputIntentForPdfx: There must be exactly 1 OutputIntent with a subtype of GTS_PDFX'
        expected_attrs = {}
        rule, attrs = pdf_preflight.parse_issue(issue)
        self.assertEqual(expected_rule, rule)
        self.assertEqual(expected_attrs, attrs)

        issue = '<Preflight::Issue:0x00000000013ec050 @description="PDF version should be 1.4 or lower", @rule=:"Preflight::Rules::MaxVersion", @attributes={:max_version=>1.4, :current_version=>1.7}>'
        expected_rule = 'MaxVersion: PDF version should be 1.4 or lower'
        expected_attrs = {'max_version': '1.4', 'current_version': '1.7'}
        rule, attrs = pdf_preflight.parse_issue(issue)
        self.assertEqual(expected_rule, rule)
        self.assertEqual(expected_attrs, attrs)
