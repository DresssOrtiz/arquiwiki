from typing import Protocol


class Embedder(Protocol):
    dim: int

    def embed(self, texts: list[str]) -> list[list[float]]: ...

    def count_tokens(self, text: str) -> int: ...


class FastEmbedder:
    """Embeddings locales con fastembed (ONNX). No consume tokens de ningún LLM."""

    def __init__(self, model_name: str):
        from fastembed import TextEmbedding

        self._model = TextEmbedding(model_name=model_name)
        self._tokenizer = self._model.model.tokenizer
        self.dim = len(self.embed(["dimensión"])[0])

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [vector.tolist() for vector in self._model.embed(texts)]

    def count_tokens(self, text: str) -> int:
        return len(self._tokenizer.encode(text).ids)
