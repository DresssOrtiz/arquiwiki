"""El conteo de tokens no debe saturarse en la ventana del modelo.

Regresión: el tokenizador de fastembed trunca y rellena a max_length (128 en MiniLM) y
`count_tokens` lo usaba tal cual, así que ningún fragmento parecía superar 128 tokens.
"""

from tokenizers import Tokenizer, models, pre_tokenizers

from app.chunker import chunk_markdown
from app.embedder import make_counter, window_of

WINDOW = 8


def model_like_tokenizer() -> Tokenizer:
    """Tokenizador sintético con el mismo comportamiento: trunca y rellena a WINDOW."""
    vocab = {"[PAD]": 0, "[UNK]": 1, **{f"w{i}": i + 2 for i in range(500)}}
    tok = Tokenizer(models.WordLevel(vocab, unk_token="[UNK]"))
    tok.pre_tokenizer = pre_tokenizers.Whitespace()
    tok.enable_truncation(max_length=WINDOW)
    tok.enable_padding(length=WINDOW, pad_id=0, pad_token="[PAD]")
    return tok


def words(n: int) -> str:
    return " ".join(f"w{i}" for i in range(n))


def test_el_tokenizador_del_modelo_se_satura_y_la_copia_no():
    model = model_like_tokenizer()
    assert len(model.encode(words(50)).ids) == WINDOW  # el problema original
    assert make_counter(model).encode(words(50)).ids.__len__() == 50


def test_el_contador_no_altera_el_tokenizador_original():
    model = model_like_tokenizer()
    make_counter(model)
    assert model.truncation["max_length"] == WINDOW
    assert len(model.encode(words(50)).ids) == WINDOW


def test_ventana_del_modelo():
    assert window_of(model_like_tokenizer()) == WINDOW
    sin_truncar = model_like_tokenizer()
    sin_truncar.no_truncation()
    assert window_of(sin_truncar) == 512


def test_con_el_contador_correcto_ningun_fragmento_excede_la_ventana():
    counter = make_counter(model_like_tokenizer())
    count = lambda t: len(counter.encode(t).ids)  # noqa: E731
    doc = "# Titulo\n\n" + "\n\n".join(words(30) for _ in range(5))
    chunks = chunk_markdown(doc, count, max_tokens=WINDOW)
    assert len(chunks) > 5
    assert all(c.tokens <= WINDOW for c in chunks)
    # el texto completo queda cubierto: nada se descarta al embeber
    assert sum(c.tokens for c in chunks) >= 5 * 30
