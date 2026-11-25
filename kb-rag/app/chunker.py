"""Fragmentación de markdown por encabezados.

Cada fragmento lleva la ruta de encabezados como prefijo ("Clase 2 > Pasos"),
lo que le da contexto al embedding. Los párrafos se agrupan hasta `max_tokens`;
un párrafo más largo se parte por ventanas de palabras con solapamiento corto.
"""

import re
from collections.abc import Callable
from dataclasses import dataclass

CountTokens = Callable[[str], int]

_HEADING = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")


@dataclass(frozen=True)
class Chunk:
    ord: int
    heading: str
    text: str
    tokens: int


def _sections(markdown: str) -> list[tuple[str, str]]:
    """Devuelve (ruta_de_encabezados, cuerpo) por cada sección con contenido."""
    stack: list[tuple[int, str]] = []
    sections: list[tuple[str, list[str]]] = [("", [])]
    in_code = False
    for line in markdown.splitlines():
        if line.lstrip().startswith("```"):
            in_code = not in_code
        m = None if in_code else _HEADING.match(line)
        if m:
            level, title = len(m.group(1)), m.group(2)
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, title))
            sections.append((" > ".join(t for _, t in stack), []))
        else:
            sections[-1][1].append(line)
    return [(h, "\n".join(body).strip()) for h, body in sections if "\n".join(body).strip()]


def _split_long(paragraph: str, max_tokens: int, count: CountTokens, overlap_words: int) -> list[str]:
    words = paragraph.split()
    pieces: list[str] = []
    start = 0
    while start < len(words):
        end = len(words)
        # Se reduce la ventana hasta que quepa; mínimo una palabra.
        while end - start > 1 and count(" ".join(words[start:end])) > max_tokens:
            end = start + max(1, (end - start) * 3 // 4)
        pieces.append(" ".join(words[start:end]))
        if end >= len(words):
            break
        start = max(start + 1, end - overlap_words)
    return pieces


def chunk_markdown(
    markdown: str,
    count_tokens: CountTokens,
    max_tokens: int = 200,
    overlap_words: int = 20,
) -> list[Chunk]:
    chunks: list[Chunk] = []

    def emit(heading: str, text: str) -> None:
        full = f"{heading}\n\n{text}" if heading else text
        chunks.append(Chunk(len(chunks), heading, full, count_tokens(full)))

    for heading, body in _sections(markdown):
        budget = max(1, max_tokens - count_tokens(heading))
        buffer: list[str] = []
        for paragraph in re.split(r"\n\s*\n", body):
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            if count_tokens(paragraph) > budget:
                if buffer:
                    emit(heading, "\n\n".join(buffer))
                    buffer = []
                for piece in _split_long(paragraph, budget, count_tokens, overlap_words):
                    emit(heading, piece)
                continue
            candidate = "\n\n".join([*buffer, paragraph])
            if buffer and count_tokens(candidate) > budget:
                emit(heading, "\n\n".join(buffer))
                buffer = [paragraph]
            else:
                buffer.append(paragraph)
        if buffer:
            emit(heading, "\n\n".join(buffer))
    return chunks
