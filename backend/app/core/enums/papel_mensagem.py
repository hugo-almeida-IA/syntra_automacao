from enum import Enum


class PapelMensagem(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"