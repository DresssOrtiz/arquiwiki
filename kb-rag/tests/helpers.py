"""Dobles de prueba: embedder determinista, almacén en memoria y LLM falso."""

import hashlib
import math

from app.chunker import Chunk
from app.llm import Answer
from app.store import Hit

DIM = 32


def _bag_of_words(text: str) -> list[float]:
    vec = [0.0] * DIM
    for word in text.lower().split():
        h = int(hashlib.md5(word.strip(".,:;¿?¡!()[]#>*-").encode()).hexdigest(), 16)
        vec[h % DIM] += 1.0
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / norm for x in vec]


class FakeEmbedder:
    dim = DIM

    def embed(self, texts):
        return [_bag_of_words(t) for t in texts]

    def count_tokens(self, text):
        return len(text.split())


class MemoryStore:
    def __init__(self):
        self.docs: dict[str, dict] = {}
        self.logs: list[tuple[str, dict]] = []

    def document_hashes(self):
        return {p: d["sha256"] for p, d in self.docs.items()}

    def replace_document(self, path, sha256, chunks: list[Chunk], vectors):
        self.docs[path] = {"sha256": sha256, "chunks": list(zip(chunks, vectors, strict=True))}

    def delete_document(self, path):
        self.docs.pop(path, None)

    def search(self, vector, k):
        rows = [
            Hit(path, c.heading, c.text, c.tokens, sum(a * b for a, b in zip(vector, v, strict=True)))
            for path, d in self.docs.items()
            for c, v in d["chunks"]
        ]
        return sorted(rows, key=lambda h: h.score, reverse=True)[:k]

    def stats(self):
        chunks = [c for d in self.docs.values() for c, _ in d["chunks"]]
        return {
            "documents": len(self.docs),
            "chunks": len(chunks),
            "indexed_tokens": sum(c.tokens for c in chunks),
        }

    def log(self, kind, data):
        self.logs.append((kind, data))


class FakeLLM:
    def __init__(self):
        self.calls = []

    def answer(self, question, hits):
        self.calls.append((question, hits))
        return Answer(text=f"respuesta [{hits[0].path}]", input_tokens=123, output_tokens=45, model="fake-model")
