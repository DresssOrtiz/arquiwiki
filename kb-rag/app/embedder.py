from typing import Protocol


class Embedder(Protocol):
    dim: int
    max_seq_len: int  # tokens que el modelo realmente procesa por texto (el resto se descarta)

    def embed(self, texts: list[str]) -> list[list[float]]: ...

    def count_tokens(self, text: str) -> int: ...


def make_counter(model_tokenizer):
    """Copia del tokenizador del modelo sin truncamiento ni relleno, solo para contar.

    El original trunca (y rellena) a max_length; contar con él satura el conteo en ese valor.
    """
    from tokenizers import Tokenizer

    counter = Tokenizer.from_str(model_tokenizer.to_str())
    counter.no_truncation()
    counter.no_padding()
    return counter


def window_of(model_tokenizer) -> int:
    """Tokens por texto que el modelo realmente procesa."""
    truncation = model_tokenizer.truncation
    return int(truncation["max_length"]) if truncation else 512


class FastEmbedder:
    """Embeddings locales con fastembed (ONNX). No consume tokens de ningún LLM."""

    def __init__(self, model_name: str):
        from fastembed import TextEmbedding

        self._model = TextEmbedding(model_name=model_name)
        model_tokenizer = self._model.model.tokenizer
        self._counter = make_counter(model_tokenizer)
        self.max_seq_len = window_of(model_tokenizer)
        self.dim = len(self.embed(["dimensión"])[0])

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [vector.tolist() for vector in self._model.embed(texts)]

    def count_tokens(self, text: str) -> int:
        return len(self._counter.encode(text).ids)
