# API de Usuários

API CRUD para gerenciamento de usuários com FastAPI e MongoDB.

## Funcionalidades

- Criar usuário (POST /users)
- Listar todos os usuários (GET /users)
- Buscar usuário por ID (GET /users/{id})
- Atualizar usuário (PUT /users/{id})
- Deletar usuário (DELETE /users/{id})

## Como executar

```bash
docker-compose up --build
```

A API estará disponível em: http://localhost:8000

Documentação automática: http://localhost:8000/docs

## Estrutura do Usuário

```json
{
  "name": "João Silva",
  "email": "joao@email.com",
  "birthdate": "1990-01-15"
}
```