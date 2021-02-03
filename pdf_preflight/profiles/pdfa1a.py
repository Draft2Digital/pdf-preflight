from .base_profile import Profile

from pdf_preflight import rules


class Pdfa1a(Profile):
    rules = [
        [rules.CompressionAlgorithms, ["/CCITTFaxDecode", "/DCTDecode", "/FlateDecode", "/RunLengthDecode"]],
        [rules.OnlyEmbeddedFonts],
    ]
