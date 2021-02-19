import os
import unittest
import pikepdf

import pdf_preflight.rules as rules
import pdf_preflight.profiles as profiles

pdf_folder = os.path.join(os.path.dirname(__file__), "pdfs")


class TestPdfPreflight(unittest.TestCase):

    def test_profile__pdfa1a(self):
        filename = os.path.join(pdf_folder, "pdfa-1a.pdf")
        self.assertEqual(None, profiles.Pdfa1a.check_preflight(filename))

        filename = os.path.join(pdf_folder, "standard_14_font.pdf")
        with self.assertRaisesRegex(Exception, "^PDF failed Preflight checks.*") as cm:
            profiles.Pdfa1a.check_preflight(filename)
        expected_exception = ("PDF failed Preflight checks with the following Issues & exceptions:\n"
                              "ISSUES:\n"
                              "Rule 'OnlyEmbeddedFonts' found an error on page 1: "
                              "All fonts must be embedded; found non-embedded font.\n")
        self.assertTrue(str(cm.exception).startswith(expected_exception))

    def test_profile__pdfx1a(self):
        filename = os.path.join(pdf_folder, "pdfx-1a.pdf")
        self.assertEqual(None, profiles.Pdfx1a.check_preflight(filename))

        filename = os.path.join(pdf_folder, "fails_pdfx.pdf")
        with self.assertRaisesRegex(Exception, "^PDF failed Preflight checks.*") as cm:
            profiles.Pdfx1a.check_preflight(filename)
        expected_exception = ("PDF failed Preflight checks with the following Issues & exceptions:\n"
                              "ISSUES:\n"
                              "Rule 'InfoHasKeys' found an error in document metadata: "
                              "Info dict missing required key '/ModDate'\n"
                              "Rule 'InfoHasKeys' found an error in document metadata: "
                              "Info dict missing required key '/Title'\n"
                              "Rule 'InfoSpecifiesTrapping' found an error in document metadata: "
                              "Info dict missing required key '/Trapped'.\n"
                              "Rule 'MatchInfoEntries' found an error in document metadata: "
                              "Info dict missing required key '/GTS_PDFXConformance'\n"
                              "Rule 'MatchInfoEntries' found an error in document metadata: "
                              "Info dict missing required key '/GTS_PDFXVersion'\n"
                              "Rule 'MaxVersion' found an error in document metadata: "
                              "PDF version should be 1.3 or lower.\n"
                              "Rule 'NoRgb' found an error on page 1-100: "
                              "Found RGB colorspace; RGB objects are prohibited.\n"
                              "Rule 'NoTransparency' found an error on page 1-100: "
                              "Found object with transparency; transparent objects are prohibited.\n"
                              "Rule 'OutputIntentForPdfx' found an error in document metadata: "
                              "OutputIntent with subtype '/GTS_PDFX' is required but was not found.\n"
                              "Rule 'PdfxOutputIntentHasKeys' found an error in document metadata: "
                              "GTS_PDFX OutputIntent not found, assumed to be missing all required keys "
                              "'['/OutputConditionIdentifier', '/Info']'.\n"
                              "Rule 'PrintBoxes' found an error on page 1-100: "
                              "ArtBox or TrimBox is required, but neither was found; TrimBox is preferred.\n"
                              "Rule 'RootHasKeys' found an error in document metadata: "
                              "Root dict missing required key '/OutputIntents'\n")
        self.assertTrue(str(cm.exception).startswith(expected_exception))

    def test_profile__pdfx1a2003(self):
        filename = os.path.join(pdf_folder, "pdfx-1a-2003.pdf")
        self.assertEqual(None, profiles.Pdfx1a2003.check_preflight(filename))

        filename = os.path.join(pdf_folder, "fails_pdfx.pdf")
        with self.assertRaisesRegex(Exception, "^PDF failed Preflight checks.*") as cm:
            profiles.Pdfx1a2003.check_preflight(filename)
        expected_exception = ("PDF failed Preflight checks with the following Issues & exceptions:\n"
                              "ISSUES:\n"
                              "Rule 'InfoHasKeys' found an error in document metadata: "
                              "Info dict missing required key '/ModDate'\n"
                              "Rule 'InfoHasKeys' found an error in document metadata: "
                              "Info dict missing required key '/Title'\n"
                              "Rule 'InfoSpecifiesTrapping' found an error in document metadata: "
                              "Info dict missing required key '/Trapped'.\n"
                              "Rule 'MatchInfoEntries' found an error in document metadata: "
                              "Info dict missing required key '/GTS_PDFXVersion'\n"
                              "Rule 'MaxVersion' found an error in document metadata: "
                              "PDF version should be 1.4 or lower.\n"
                              "Rule 'NoRgb' found an error on page 1-100: "
                              "Found RGB colorspace; RGB objects are prohibited.\n"
                              "Rule 'NoTransparency' found an error on page 1-100: "
                              "Found object with transparency; transparent objects are prohibited.\n"
                              "Rule 'OutputIntentForPdfx' found an error in document metadata: "
                              "OutputIntent with subtype '/GTS_PDFX' is required but was not found.\n"
                              "Rule 'PdfxOutputIntentHasKeys' found an error in document metadata: "
                              "GTS_PDFX OutputIntent not found, assumed to be missing all required keys "
                              "'['/OutputConditionIdentifier', '/Info']'.\n"
                              "Rule 'PrintBoxes' found an error on page 1-100: "
                              "ArtBox or TrimBox is required, but neither was found; TrimBox is preferred.\n"
                              "Rule 'RootHasKeys' found an error in document metadata: "
                              "Root dict missing required key '/OutputIntents'\n")
        self.assertTrue(str(cm.exception).startswith(expected_exception))

    ######################################################################

    def test_rule__box_nesting(self):
        filename = os.path.join(pdf_folder, "72ppi.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.BoxNesting.check(pdf)
            self.assertEqual(None, issues)

        filename = os.path.join(pdf_folder, "bleedbox_larger_than_mediabox.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.BoxNesting.check(pdf)
            issue = issues[0]
            self.assertEqual(1, issue.page)
            self.assertEqual("BoxNesting", issue.rule)
            self.assertEqual("BleedBox must be smaller than MediaBox", issue.desc)

    def test_rule__compression_algorithms(self):
        filename = os.path.join(pdf_folder, "jbig2.pdf")
        with pikepdf.open(filename) as pdf:
            allowed_algorithms = ["/FlateDecode", "/JBIG2Decode"]
            issues = rules.CompressionAlgorithms.check(pdf, allowed_algorithms)
            self.assertEqual(None, issues)

        filename = os.path.join(pdf_folder, "jbig2.pdf")
        with pikepdf.open(filename) as pdf:
            allowed_algorithms = ["/FlateDecode"]
            issues = rules.CompressionAlgorithms.check(pdf, allowed_algorithms)
            issue = issues[0]
            self.assertEqual("Metadata", issue.page)
            self.assertEqual("CompressionAlgorithms", issue.rule)
            self.assertEqual("File uses unwanted compression algorithm: '/JBIG2Decode'", issue.desc)

    def test_rule__document_id(self):
        filename = os.path.join(pdf_folder, "pdfx-1a-subsetting.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.DocumentId.check(pdf)
            self.assertEqual(None, issues)

        filename = os.path.join(pdf_folder, "no_document_id.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.DocumentId.check(pdf)
            issue = issues[0]
            self.assertEqual("Metadata", issue.page)
            self.assertEqual("DocumentId", issue.rule)
            self.assertEqual("Document ID missing.", issue.desc)

    def test_rule__info_has_keys(self):
        filename = os.path.join(pdf_folder, "72ppi.pdf")
        with pikepdf.open(filename) as pdf:
            entries = ["/Creator", "/Producer"]
            issues = rules.InfoHasKeys.check(pdf, entries)
            self.assertEqual(None, issues)

        filename = os.path.join(pdf_folder, "72ppi.pdf")
        with pikepdf.open(filename) as pdf:
            entries = ["/GTS_PDFXVersion"]
            issues = rules.InfoHasKeys.check(pdf, entries)
            issue = issues[0]
            self.assertEqual("Metadata", issue.page)
            self.assertEqual("InfoHasKeys", issue.rule)
            self.assertEqual("Info dict missing required key '/GTS_PDFXVersion'", issue.desc)

    def test_rule__info_specifies_trapping(self):
        filename = os.path.join(pdf_folder, "trapped_false.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.InfoSpecifiesTrapping.check(pdf)
            self.assertEqual(None, issues)

        filename = os.path.join(pdf_folder, "trapped_true.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.InfoSpecifiesTrapping.check(pdf)
            self.assertEqual(None, issues)

        filename = os.path.join(pdf_folder, "trapped_broken.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.InfoSpecifiesTrapping.check(pdf)
            issue = issues[0]
            self.assertEqual("Metadata", issue.page)
            self.assertEqual("InfoSpecifiesTrapping", issue.rule)
            self.assertEqual("Value of Info entry '/Trapped' must be True or False.", issue.desc)

        filename = os.path.join(pdf_folder, "72ppi.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.InfoSpecifiesTrapping.check(pdf)
            issue = issues[0]
            self.assertEqual("Metadata", issue.page)
            self.assertEqual("InfoSpecifiesTrapping", issue.rule)
            self.assertEqual("Info dict missing required key '/Trapped'.", issue.desc)

    def test_rule__match_info_entries(self):
        filename = os.path.join(pdf_folder, "72ppi.pdf")
        with pikepdf.open(filename) as pdf:
            entries = {"/Creator": r"Prawn"}
            issues = rules.MatchInfoEntries.check(pdf, entries)
            self.assertEqual(None, issues)

        filename = os.path.join(pdf_folder, "72ppi.pdf")
        with pikepdf.open(filename) as pdf:
            entries = {"/GTS_PDFXVersion": "^PDF/X.*"}
            issues = rules.MatchInfoEntries.check(pdf, entries)
            issue = issues[0]
            self.assertEqual("Metadata", issue.page)
            self.assertEqual("MatchInfoEntries", issue.rule)
            self.assertEqual("Info dict missing required key '/GTS_PDFXVersion'", issue.desc)

        filename = os.path.join(pdf_folder, "72ppi.pdf")
        with pikepdf.open(filename) as pdf:
            entries = {"/Creator": r"Shrimp"}
            issues = rules.MatchInfoEntries.check(pdf, entries)
            issue = issues[0]
            self.assertEqual("Metadata", issue.page)
            self.assertEqual("MatchInfoEntries", issue.rule)
            self.assertEqual("Value of Info entry '/Creator' doesn't match regex 'Shrimp'", issue.desc)

    def test_rule__max_ink_density(self):
        # no cmyk colors specified
        filename = os.path.join(pdf_folder, "rgb-hexagon.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.MaxInkDensity.check(pdf, 100)
            self.assertEqual(None, issues)

        # cmyk ink density in file is at or below threshold
        filename = os.path.join(pdf_folder, "cmyk.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.MaxInkDensity.check(pdf, 400)
            self.assertEqual(None, issues)

        # cmyk ink density in file is above threshold
        filename = os.path.join(pdf_folder, "cmyk.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.MaxInkDensity.check(pdf, 240)
            issue = issues[0]
            self.assertEqual(5, issue.page)
            self.assertEqual("MaxInkDensity", issue.rule)
            self.assertEqual("CMYK ink density too high; must not exceed 240%", issue.desc)

    def test_rule__max_version(self):
        filename = os.path.join(pdf_folder, "version_1_3.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.MaxVersion.check(pdf, "1.3")
            self.assertEqual(None, issues)

        filename = os.path.join(pdf_folder, "version_1_3.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.MaxVersion.check(pdf, "1.4")
            self.assertEqual(None, issues)

        filename = os.path.join(pdf_folder, "version_1_4.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.MaxVersion.check(pdf, "1.4")
            self.assertEqual(None, issues)

        filename = os.path.join(pdf_folder, "version_1_4.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.MaxVersion.check(pdf, "1.3")
            issue = issues[0]
            self.assertEqual("Metadata", issue.page)
            self.assertEqual("MaxVersion", issue.rule)
            self.assertEqual("PDF version should be 1.3 or lower.", issue.desc)

    def test_rule__min_ppi(self):
        filename = os.path.join(pdf_folder, "300ppi.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.MinPpi.check(pdf, 300)
            self.assertEqual(None, issues)

        filename = os.path.join(pdf_folder, "72ppi.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.MinPpi.check(pdf, 300)
            issue = issues[0]
            self.assertEqual(1, issue.page)
            self.assertEqual("MinPpi", issue.rule)
            self.assertEqual("Found low-resolution image; images must be at least 300 ppi.", issue.desc)

    def test_rule__no_filespecs(self):
        filename = os.path.join(pdf_folder, "rgb.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.NoFilespecs.check(pdf)
            self.assertEqual(None, issues)

        filename = os.path.join(pdf_folder, "filespec_to_external_file.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.NoFilespecs.check(pdf)
            issue = issues[0]
            self.assertEqual("Metadata", issue.page)
            self.assertEqual("NoFilespecs", issue.rule)
            self.assertEqual("Found one or more filespecs; use of filespecs to reference external files is prohibited.",
                             issue.desc)

    def test_rule__no_indexed_cmyk(self):
        # pass a file with both indexed and non-indexed colorspaces that are not CMYK
        filename = os.path.join(pdf_folder, "rgb.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.NoIndexedCmyk.check(pdf)
            self.assertEqual(None, issues)

        # fail a file with indexed CMYK, ignoring its non-indexed CMYK colorspaces
        filename = os.path.join(pdf_folder, "cmyk.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.NoIndexedCmyk.check(pdf)
            issue = issues[0]
            self.assertEqual(7, issue.page)
            self.assertEqual("NoIndexedCmyk", issue.rule)
            self.assertEqual("Indexed CMYK colorspaces are prohibited but one or more were found.",
                             issue.desc)

    def test_rule__no_rgb(self):
        filename = os.path.join(pdf_folder, "gray.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.NoRgb.check(pdf)
            self.assertEqual(None, issues)

        filename = os.path.join(pdf_folder, "rgb.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.NoRgb.check(pdf)
            issue = issues[0]
            self.assertEqual(1, issue.page)
            self.assertEqual("NoRgb", issue.rule)
            self.assertEqual("Found RGB colorspace; RGB objects are prohibited.",
                             issue.desc)

    def test_rule__no_transparency(self):
        filename = os.path.join(pdf_folder, "gray.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.NoTransparency.check(pdf)
            self.assertEqual(None, issues)

        filename = os.path.join(pdf_folder, "transparency.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.NoTransparency.check(pdf)
            issue = issues[0]
            self.assertEqual(1, issue.page)
            self.assertEqual("NoTransparency", issue.rule)
            self.assertEqual("Found object with transparency; transparent objects are prohibited.",
                             issue.desc)

    def test_rule__only_embedded_fonts(self):
        # pass a file with embedded fonts that don't have subsets
        filename = os.path.join(pdf_folder, "pdfx-1a-no-subsetting.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.OnlyEmbeddedFonts.check(pdf)
            self.assertEqual(None, issues)

        # pass a file with embedded fonts that do have subsets
        filename = os.path.join(pdf_folder, "pdfx-1a-subsetting.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.OnlyEmbeddedFonts.check(pdf)
            self.assertEqual(None, issues)

        # fail a file with a standard font that's not embedded
        filename = os.path.join(pdf_folder, "standard_14_font.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.OnlyEmbeddedFonts.check(pdf)
            issue = issues[0]
            self.assertEqual(1, issue.page)
            self.assertEqual("OnlyEmbeddedFonts", issue.rule)
            self.assertEqual("All fonts must be embedded; found non-embedded font.", issue.desc)

    def test_rule__output_intent_for_pdfx(self):
        filename = os.path.join(pdf_folder, "pdfx-1a-subsetting.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.OutputIntentForPdfx.check(pdf)
            self.assertEqual(None, issues)

        filename = os.path.join(pdf_folder, "two_outputintents.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.OutputIntentForPdfx.check(pdf)
            issue = issues[0]
            self.assertEqual("Metadata", issue.page)
            self.assertEqual("OutputIntentForPdfx", issue.rule)
            self.assertEqual("Exactly one OutputIntent with subtype '/GTS_PDFX' is required; found multiple.",
                             issue.desc)

        filename = os.path.join(pdf_folder, "version_1_4.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.OutputIntentForPdfx.check(pdf)
            issue = issues[0]
            self.assertEqual("Metadata", issue.page)
            self.assertEqual("OutputIntentForPdfx", issue.rule)
            self.assertEqual("OutputIntent with subtype '/GTS_PDFX' is required but was not found.", issue.desc)

    def test_rule__pdfx_output_intent_has_keys(self):
        filename = os.path.join(pdf_folder, "pdfx-1a-subsetting.pdf")
        with pikepdf.open(filename) as pdf:
            entries = ["/OutputConditionIdentifier", "/Info"]
            issues = rules.PdfxOutputIntentHasKeys.check(pdf, entries)
            self.assertEqual(None, issues)

        filename = os.path.join(pdf_folder, "pdfx-1a-subsetting.pdf")
        with pikepdf.open(filename) as pdf:
            entries = ["/Cheese"]
            issues = rules.PdfxOutputIntentHasKeys.check(pdf, entries)
            issue = issues[0]
            self.assertEqual("Metadata", issue.page)
            self.assertEqual("PdfxOutputIntentHasKeys", issue.rule)
            self.assertEqual("GTS_PDFX OutputIntent missing required key '/Cheese'.",
                             issue.desc)

        filename = os.path.join(pdf_folder, "version_1_4.pdf")
        with pikepdf.open(filename) as pdf:
            entries = ["/Info"]
            issues = rules.PdfxOutputIntentHasKeys.check(pdf, entries)
            issue = issues[0]
            self.assertEqual("Metadata", issue.page)
            self.assertEqual("PdfxOutputIntentHasKeys", issue.rule)
            self.assertEqual("GTS_PDFX OutputIntent not found, assumed to be missing all required keys '['/Info']'.",
                             issue.desc)

    def test_rule__print_boxes(self):
        filename = os.path.join(pdf_folder, "pdfx-1a-subsetting.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.PrintBoxes.check(pdf)
            self.assertEqual(None, issues)

        filename = os.path.join(pdf_folder, "inherited_page_attributes.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.PrintBoxes.check(pdf)
            self.assertEqual(None, issues)

        filename = os.path.join(pdf_folder, "artbox_and_trimbox.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.PrintBoxes.check(pdf,)
            issue = issues[0]
            self.assertEqual(1, issue.page)
            self.assertEqual("PrintBoxes", issue.rule)
            self.assertEqual("A page cannot have both ArtBox and TrimBox, but both were found; TrimBox is preferred",
                             issue.desc)

        filename = os.path.join(pdf_folder, "no_artbox_or_trimbox.pdf")
        with pikepdf.open(filename) as pdf:
            issues = rules.PrintBoxes.check(pdf,)
            issue = issues[0]
            self.assertEqual(1, issue.page)
            self.assertEqual("PrintBoxes", issue.rule)
            self.assertEqual("ArtBox or TrimBox is required, but neither was found; TrimBox is preferred.", issue.desc)

    def test_rule__root_has_keys(self):
        filename = os.path.join(pdf_folder, "72ppi.pdf")
        with pikepdf.open(filename) as pdf:
            entries = ["/Type"]
            issues = rules.RootHasKeys.check(pdf, entries)
            self.assertEqual(None, issues)

        filename = os.path.join(pdf_folder, "72ppi.pdf")
        with pikepdf.open(filename) as pdf:
            entries = ["/OutputIntents"]
            issues = rules.RootHasKeys.check(pdf, entries)
            issue = issues[0]
            self.assertEqual("Metadata", issue.page)
            self.assertEqual("RootHasKeys", issue.rule)
            self.assertEqual("Root dict missing required key '/OutputIntents'", issue.desc)
