# Projeto de Gestão de Estoques - API FastAPI

Foram implementadas funcionalidades para registrar movimentações, controlar saldos, gerenciar estoque mínimo e oferecer operações de negócio como vendas e devoluções.

## Decisão sobre Saldo Negativo

Conforme as boas práticas de gestão de estoque, a regra de negócio implementada na API **bloqueia qualquer movimento de saída que possa resultar em um saldo negativo**. A variável de controle `ALLOW_NEGATIVE_STOCK` no repositório de estoque está configurada como `False` para garantir a integridade dos dados de estoque.

## Como Executar a Aplicação

1.  **Instale as dependências:**
    Certifique-se de ter `fastapi`, `uvicorn`, `sqlalchemy`, `pydantic` e `pydantic-settings` instalados.
    ```bash
    pip install fastapi "uvicorn[standard]" sqlalchemy pydantic
    ```

2.  **Execute o servidor:**
    A partir da raiz do projeto, execute o seguinte comando:
    ```bash
    uvicorn app.main:app --reload
    ```

3.  **Acesse a Documentação Interativa:**
    A API estará disponível em `http://127.0.0.1:8000`. A documentação do Swagger UI pode ser acessada em `http://127.0.0.1:8000/docs`.

## Exemplos de Chamadas (cURL)

Substitua `{produto_id}` pelo ID do produto desejado.

### 1. Registrar uma Venda (SAIDA)
```bash
curl -X 'POST' \
  '[http://127.0.0.1:8000/v1/estoque/venda](http://127.0.0.1:8000/v1/estoque/venda)' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "produto_id": 1,
  "quantidade": 5
}'
```

### 2. Registrar uma Devolução (ENTRADA)
```bash
curl -X 'POST' \
  '[http://127.0.0.1:8000/v1/estoque/devolucao](http://127.0.0.1:8000/v1/estoque/devolucao)' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "produto_id": 1,
  "quantidade": 2
}'
```
