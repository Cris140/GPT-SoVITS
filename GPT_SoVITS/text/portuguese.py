import re
from phonemizer import phonemize
from phonemizer.punctuation import Punctuation
from phonemizer.backend import EspeakBackend
from phonemizer.separator import Separator, default_separator

from text import symbols

# Regular expression matching Portuguese characters without punctuation marks:
_portuguese_characters = re.compile(
    r"[A-Za-zÁÉÍÓÚáéíóúÂÊÔâêôÃÕãõÇç]"
)

# Regular expression matching non-Portuguese characters or punctuation marks:
_portuguese_marks = re.compile(
    r"[^A-Za-zÁÉÍÓÚáéíóúÂÊÔâêôÃÕãõÇç]"
)

# List of (symbol, Portuguese) pairs for marks:
_symbols_to_portuguese = [(re.compile("%s" % x[0]), x[1]) for x in [("percent", "por cento")]]

# Convert list into string 
def listToString(text):  
    str1 = ""      
    for ele in text: 
        str1 += ele  
    return str1 

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
    if ph in rep_map.keys():
        ph = rep_map[ph]
    if ph in symbols:
        return ph
    if ph not in symbols:
        ph = "UNK"
    return ph


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
    text = lowercase(text)
    text = collapse_whitespace(text)
    text = [text]
    text = backendptbr.phonemize(text)
    text = listToString(text)
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
