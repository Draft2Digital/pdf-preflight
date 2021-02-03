from .base_profile import Profile

from pdf_preflight import rules


class Pdfx1a2003(Profile):
    rules = [
        [rules.BoxNesting],
        [rules.CompressionAlgorithms, ["/ASCII85Decode", "/CCITTFaxDecode", "/DCTDecode", "/FlateDecode", "/RunLengthDecode"]],
        [rules.DocumentId],
        [rules.InfoHasKeys, ["/Title", "/CreationDate", "/ModDate"]],
        [rules.InfoSpecifiesTrapping],
        [rules.MatchInfoEntries, {"/GTS_PDFXVersion": "^PDF/X.*"}],
        [rules.MaxVersion, "1.4"],
        [rules.NoFilespecs],
        [rules.NoRgb],
        [rules.NoTransparency],
        [rules.OnlyEmbeddedFonts],
        [rules.OutputIntentForPdfx],
        [rules.PdfxOutputIntentHasKeys],
        [rules.PrintBoxes],
        [rules.RootHasKeys, ["/OutputIntents"]],
    ]
