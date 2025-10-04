from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.deps import get_db
from app.schemas.produto import ProdutoCreate, ProdutoOut
from app.schemas.estoque import ResumoEstoqueOut
from app.repositories import produto as repo
from app.repositories import estoque as repo_estoque

rotas = APIRouter(prefix="/v1/produtos", tags=["Produtos"]) 

@rotas.post("/", response_model=ProdutoOut, status_code=status.HTTP_201_CREATED)
def create(payload: ProdutoCreate, db: Session = Depends(get_db)):
    """Cria um novo produto."""
    return repo.create(db, payload)

@rotas.get("/", response_model=List[ProdutoOut])
def list_all(db: Session = Depends(get_db)):
    """Lista todos os produtos."""
    return repo.get_all(db)

@rotas.get("/{produto_id}", response_model=ProdutoOut)
def get_by_id(produto_id: int, db: Session = Depends(get_db)):
    """Obtém um produto pelo seu ID."""
    objeto = repo.get(db, produto_id)
    if not objeto:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Produto não encontrado")
    return objeto

@rotas.get("/abaixo-minimo/", response_model=List[ResumoEstoqueOut])
def listar_produtos_abaixo_minimo(db: Session = Depends(get_db)):
    """Lista produtos com estoque abaixo do mínimo definido."""
    produtos = repo.get_all(db)
    produtos_criticos = []
    for p in produtos:
        if p.ativo:
            saldo = repo_estoque.get_saldo_produto(db, p.id)
            if saldo < p.estoque_minimo:
                produtos_criticos.append(ResumoEstoqueOut(
                    produto_id=p.id,
                    nome=p.nome,
                    saldo=saldo,
                    estoque_minimo=p.estoque_minimo,
                    abaixo_minimo=True
                ))
    return produtos_criticos