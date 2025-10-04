from pydantic import BaseModel, Field
from datetime import datetime
from app.models.estoque import TipoMovimento

# criacao
class EstoqueMovimentoCreate(BaseModel):
    produto_id: int
    tipo: TipoMovimento
    quantidade: int = Field(gt=0, description="A quantidade deve ser maior que zero")
    motivo: str | None = None

# saida (resposta da API)
class EstoqueMovimentoOut(BaseModel):
    id: int
    produto_id: int
    tipo: TipoMovimento
    quantidade: int
    motivo: str | None
    criado_em: datetime

    class Config:
        from_attributes = True

# consulta de saldo
class SaldoOut(BaseModel):
    produto_id: int
    saldo: int

# resumo de estoque
class ResumoEstoqueOut(BaseModel):
    produto_id: int
    nome: str
    saldo: int
    estoque_minimo: int
    abaixo_minimo: bool

# operacoes compostas
class VendaDevolucaoPayload(BaseModel):
    produto_id: int
    quantidade: int = Field(gt=0)

class AjustePayload(BaseModel):
    produto_id: int
    quantidade: int = Field(gt=0)
    tipo: TipoMovimento
    motivo: str