from dataclasses import dataclass
from typing import Protocol

from app.store import Hit

SYSTEM_PROMPT = (
    "Eres un asistente de un curso de Arquitectura de Software. Responde en español usando "
    "únicamente los fragmentos de contexto. Después de cada afirmación cita la fuente entre "
    "corchetes con su ruta, por ejemplo [raw/clase-02-atam.md]. Si los fragmentos no contienen "
    "la respuesta, dilo claramente en lugar de inventarla."
)


@dataclass(frozen=True)
class Answer:
    text: str
    input_tokens: int
    output_tokens: int
    model: str


class LLM(Protocol):
    def answer(self, question: str, hits: list[Hit]) -> Answer: ...


def build_user_message(question: str, hits: list[Hit]) -> str:
    context = "\n\n".join(f"[{h.path}] ({h.heading or 'sin título'})\n{h.text}" for h in hits)
    return f"Contexto:\n\n{context}\n\nPregunta: {question}"


class AnthropicLLM:
    def __init__(self, api_key: str, model: str, max_tokens: int):
        import anthropic

        self._client = anthropic.Anthropic(api_key=api_key)
        self._model = model
        self._max_tokens = max_tokens

    def answer(self, question: str, hits: list[Hit]) -> Answer:
        response = self._client.messages.create(
            model=self._model,
            max_tokens=self._max_tokens,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": build_user_message(question, hits)}],
        )
        text = "".join(b.text for b in response.content if b.type == "text")
        return Answer(
            text=text,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            model=self._model,
        )
