import re
import unicodedata


def normalize_unicode(text):
    """
    Basic Unicode normalization.

    Does not perform external lookup or translation.
    """
    if text is None:
        return ""

    if not isinstance(text, str):
        text = str(text)

    text = unicodedata.normalize("NFKC", text)

    return text


def normalize_text(text):
    """
    Conservative general-purpose text normalization.

    - Unicode normalization
    - lowercase/casefold
    - & -> and
    - punctuation -> spaces
    - whitespace normalization
    """

    text = normalize_unicode(text)

    if not text:
        return ""

    text = text.casefold()

    # Treat ampersand as a word rather than deleting it
    text = text.replace("&", " and ")

    # Replace punctuation/symbols with spaces
    text = re.sub(r"[^\w\s]", " ", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize_name(text):
    text = normalize_text(text)
    return expand_abbreviations(text, NAME_ABBREVIATIONS)


def normalize_address(text):
    text = normalize_text(text)
    return expand_abbreviations(text, ADDRESS_ABBREVIATIONS)

NAME_ABBREVIATIONS = {
    "pvt": "private",
    "ltd": "limited",
    "corp": "corporation",
    "inc": "incorporated",
    "co": "company",
}

ADDRESS_ABBREVIATIONS = {
    "rd": "road",
    "st": "street",
    "ave": "avenue",
    "blvd": "boulevard",
    "dr": "drive",
    "ln": "lane",
    "hwy": "highway",
    "pkwy": "parkway",
    "ct": "court",
    "pl": "place",
    "trl": "trail",
    "cir": "circle",
    "ter": "terrace",
    "ste": "suite",
    "apt": "apartment",
}

def expand_abbreviations(text, mapping):
    """
    Expand whole-word abbreviations only.
    """

    if not text:
        return ""

    tokens = text.split()

    tokens = [
        mapping.get(token, token)
        for token in tokens
    ]

    return " ".join(tokens)