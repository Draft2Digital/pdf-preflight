from .base_profile import Profile

from pdf_preflight import rules


class Pdfx1a(Profile):
    rules = [
        [rules.BoxNesting],
        [rules.CompressionAlgorithms, ["/ASCII85Decode", "/CCITTFaxDecode", "/DCTDecode", "/FlateDecode", "/RunLengthDecode"]],
        [rules.DocumentId],
        [rules.InfoHasKeys, ["/Title", "/CreationDate", "/ModDate"]],
        [rules.InfoSpecifiesTrapping],
        [rules.MatchInfoEntries, {"/GTS_PDFXVersion": "^PDF/X.*", "/GTS_PDFXConformance": "^PDF/X-1a.*"}],
        [rules.MaxVersion, "1.3"],
        [rules.NoFilespecs],
        [rules.NoRgb],
        [rules.NoTransparency],
        [rules.OnlyEmbeddedFonts],
        [rules.OutputIntentForPdfx],
        [rules.PdfxOutputIntentHasKeys],
        [rules.PrintBoxes],
        [rules.RootHasKeys, ["/OutputIntents"]],
    ]
