# API REST - Catálogo de Livros

Projeto desenvolvido em Python usando apenas a biblioteca padrão, principalmente `http.server`.

A API permite:

* listar livros;
* buscar livro por ID;
* cadastrar livro;
* atualizar livro;
* remover livro.

## Rotas

```text
GET    /api/books
GET    /api/books/{id}
POST   /api/books
PUT    /api/books/{id}
DELETE /api/books/{id}
```

## Executar

```bash
python server.py
```

Servidor:

```text
http://127.0.0.1:3001
```

## Teste com curl

Exemplo:

```bash
curl.exe -i http://127.0.0.1:3001/api/books
```

Os dados ficam armazenados em memória, então são perdidos quando o servidor é encerrado.

Projeto feito para praticar métodos HTTP, códigos de status, JSON, recursos e princípios de REST.

