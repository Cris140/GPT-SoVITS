import re
from phonemizer import phonemize
from phonemizer.punctuation import Punctuation
from phonemizer.backend import EspeakBackend

from text import symbols

# Regular expression matching Portuguese characters without punctuation marks:
_portuguese_characters = re.compile(
    r"[A-Za-zÁÉÍÓÚáéíóúÂÊÔâêôÃÕãõÇç]+"
)

# Regular expression matching non-Portuguese characters or punctuation marks:
_portuguese_marks = re.compile(
    r"[^A-Za-zÁÉÍÓÚáéíóúÂÊÔâêôÃÕãõÇç]"
)

# List of (symbol, Portuguese) pairs for marks:
_symbols_to_portuguese = [(re.compile("%s" % x[0]), x[1]) for x in [("percent", "por cento")]]


def listToString(text):  
    return ''.join(text)


def post_replace_ph(ph):
    rep_map = {
        ":": ",",
        ";": ",",
        ",": ",",
        ".": ".",
        "!": "!",
        "?": "?",
        "\n": ".",
        "·": ",",
        "...": "…",
    }
    ph = rep_map.get(ph, ph)  # Substitui se estiver no rep_map
    return ph if ph in symbols else "UNK"  # Verifica se está em symbols ou retorna "UNK"


def symbols_to_portuguese(text):
    for regex, replacement in _symbols_to_portuguese:
        text = re.sub(regex, replacement, text)
    return text


def preprocess_port(text, backend):
    """Preprocessing for Portuguese."""
    text = symbols_to_portuguese(text)
    sentences = re.split(_portuguese_marks, text)
    marks = re.findall(_portuguese_marks, text)
    text = []
    for i, sentence in enumerate(sentences):
        if re.match(_portuguese_characters, sentence):
            phonemes = backend.phonemize(sentence)
            text += list(phonemes)

        if i < len(marks):
            if marks[i] == " ":
                continue
            text += [marks[i].replace(" ", "")]
    return text


def text_normalize(text):
    text = text.lower()  # Converte para minúsculas
    text = re.sub(r'\s+', ' ', text).strip()  # Remove espaços extras
    return text


def g2p(norm_text, backend):
    phones = preprocess_port(norm_text, backend)
    phones = [post_replace_ph(i) for i in phones]
    return phones


if __name__ == "__main__":
    # Initialize the EspeakBackend for Portuguese (Brazil)
    backendptbr = EspeakBackend(
        'pt-br',
        preserve_punctuation=True,
        punctuation_marks=Punctuation.default_marks(),
        with_stress=True,
    )
    
    phones = g2p("Olá, tudo bem? Este é um exemplo em português!", backendptbr)
    print(phones)
