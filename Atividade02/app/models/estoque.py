from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey, Enum as SQLAlchemyEnum)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
from app.models.produto import Produto
import enum

class TipoMovimento(enum.Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"

class EstoqueMovimento(Base):
    __tablename__ = 'estoque_movimentos'
    
    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey('produtos.id'), nullable=False)
    tipo = Column(SQLAlchemyEnum(TipoMovimento), nullable=False)
    quantidade = Column(Integer, nullable=False)
    motivo = Column(String, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    produto = relationship("Produto")