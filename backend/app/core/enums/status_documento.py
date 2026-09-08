from enum import Enum


class StatusDocumento(str, Enum):
    PROCESSANDO = "processando"
    PROCESSADO = "processado"
    ERRO = "erro"