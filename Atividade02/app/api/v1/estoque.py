from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.deps import get_db
from app.schemas.estoque import (EstoqueMovimentoCreate, EstoqueMovimentoOut, SaldoOut, VendaDevolucaoPayload, AjustePayload, ResumoEstoqueOut)
from app.repositories import estoque as repo_estoque
from app.repositories import produto as repo_produto
from app.models.produto import Produto

# router
rotas = APIRouter(prefix="/v1/estoque", tags=["Estoque"])

# criar movimento 
@rotas.post("/movimentos", response_model=EstoqueMovimentoOut, status_code=status.HTTP_201_CREATED)
def create_movimento(payload: EstoqueMovimentoCreate, db: Session = Depends(get_db)):
    return repo_estoque.create_movimento(db, payload)

# consultar saldo 
@rotas.get("/saldo/{produto_id}", response_model=SaldoOut)
def get_saldo(produto_id: int, db: Session = Depends(get_db)):
    produto = db.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    saldo = repo_estoque.get_saldo_produto(db, produto_id)
    return SaldoOut(produto_id=produto_id, saldo=saldo)

# venda 
@rotas.post("/venda", response_model=EstoqueMovimentoOut, status_code=status.HTTP_201_CREATED)
def registrar_venda(payload: VendaDevolucaoPayload, db: Session = Depends(get_db)):
    movimento_data = EstoqueMovimentoCreate(
        produto_id=payload.produto_id,
        tipo="SAIDA",
        quantidade=payload.quantidade,
        motivo="venda"
    )
    return repo_estoque.create_movimento(db, movimento_data)

# devolução 
@rotas.post("/devolucao", response_model=EstoqueMovimentoOut, status_code=status.HTTP_201_CREATED)
def registrar_devolucao(payload: VendaDevolucaoPayload, db: Session = Depends(get_db)):
    movimento_data = EstoqueMovimentoCreate(
        produto_id=payload.produto_id,
        tipo="ENTRADA",
        quantidade=payload.quantidade,
        motivo="devolucao"
    )
    return repo_estoque.create_movimento(db, movimento_data)

# ajuste 
@rotas.post("/ajuste", response_model=EstoqueMovimentoOut, status_code=status.HTTP_201_CREATED)
def registrar_ajuste(payload: AjustePayload, db: Session = Depends(get_db)):
    movimento_data = EstoqueMovimentoCreate(
        produto_id=payload.produto_id,
        tipo=payload.tipo,
        quantidade=payload.quantidade,
        motivo=payload.motivo
    )
    return repo_estoque.create_movimento(db, movimento_data)

# extrato 
@rotas.get("/extrato/{produto_id}", response_model=List[EstoqueMovimentoOut])
def get_extrato_produto(produto_id: int, limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    movimentos = db.query(repo_estoque.EstoqueMovimento)\
                   .filter(repo_estoque.EstoqueMovimento.produto_id == produto_id)\
                   .order_by(repo_estoque.EstoqueMovimento.criado_em.desc())\
                   .offset(offset)\
                   .limit(limit)\
                   .all()
    return movimentos

# resumo 
@rotas.get("/resumo", response_model=List[ResumoEstoqueOut])
def get_resumo_estoque(db: Session = Depends(get_db)):
    produtos_ativos = db.query(Produto).filter(Produto.ativo == True).all()
    resumo_final = []
    for p in produtos_ativos:
        saldo = repo_estoque.get_saldo_produto(db, p.id)
        resumo_final.append(ResumoEstoqueOut(
            produto_id=p.id,
            nome=p.nome,
            saldo=saldo,
            estoque_minimo=p.estoque_minimo,
            abaixo_minimo=(saldo < p.estoque_minimo)
        ))
    return resumo_final