from sqlalchemy.orm import Session
from app.models.produto import Produto
from app.models.estoque import EstoqueMovimento, TipoMovimento
from app.schemas.estoque import EstoqueMovimentoCreate
from fastapi import HTTPException, status

# calcular o saldo de um produto
def get_saldo_produto(db: Session, produto_id: int) -> int:
    movimentos = db.query(EstoqueMovimento).filter(EstoqueMovimento.produto_id == produto_id).all()
    saldo = 0
    for m in movimentos:
        if m.tipo == TipoMovimento.ENTRADA:
            saldo += m.quantidade
        else:
            saldo -= m.quantidade
    return saldo

# criar um movimento
def create_movimento(db: Session, payload: EstoqueMovimentoCreate) -> EstoqueMovimento:
    # 1. Valida se o produto existe
    produto = db.get(Produto, payload.produto_id)
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )

    # 2. Regra de negócio: Bloqueio de Saldo Negativo
    ALLOW_NEGATIVE_STOCK = False 
    if payload.tipo == TipoMovimento.SAIDA and not ALLOW_NEGATIVE_STOCK:
        saldo_atual = get_saldo_produto(db, payload.produto_id)
        if saldo_atual < payload.quantidade:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Saldo insuficiente. Saldo atual: {saldo_atual}"
            )

    # 3. Cria o movimento no banco
    db_movimento = EstoqueMovimento(**payload.model_dump())
    db.add(db_movimento)
    db.commit()
    db.refresh(db_movimento)
    return db_movimento