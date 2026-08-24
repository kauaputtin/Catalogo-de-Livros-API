from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit
import json

HOST = "127.0.0.1"
PORTA = 8000

#lista armazenamento dos livros da api
#[] lista
#{} dicionario
BOOKS = [
    {
        "id": 1,
        "title": "Poder e Manipulação",
        "author": "Jacob Pétry",
        "year": 2016,
        "available": True,
    },
    {
        "id": 2,
            "title": "Dom Casmurro",
            "author": "Machado de Assim",
            "year": 1899,
            "available": True,
    }
]

#O BaseHTTPRequestHandler recebe a requisição HTTP e 
#chama automaticamente um método Python correspondente.
#exp:GET /api/books chama do_GET()

#Uma API não se torna RESTful simplesmente porque possui operações de criação,
#leitura, atualização e remoção de dados.
#CRUD descreve operações comuns sobre dados. REST descreve um estilo
#arquitetônico baseado em restrições sobre a interação entre componentes.
#Uma aplicação pode implementar operações CRUD utilizando HTTP sem
#necessariamente atender a todas as restrições de REST.
class BookAPIHandler(BaseHTTPRequestHandler):
    def _send_json(self, status, data=None, headers=None):
        body = b""

        if data is not Nome:
            body = json.dumps(
                data,
                ensure_ascii=False
            ).encode("utf-8")

        self.send_response(status)

        if data is not None:
            self.send_header(
                "Content-Type",
                "application/json; charset=utf-8"
            )
            self.send_header(
                "Content-Length",
                str(len(body))
            )

        if headers:
            for name, value in headers.items():
                self.send_header(nome, valor)
        self.end_headers()

        if body:
            self.wfile.write(body)
