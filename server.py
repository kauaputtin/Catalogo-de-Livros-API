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
        "title": "Poder e Manipulacao",
        "author": "Jacob Petry",
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
class RestHTTPRequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, status, data=None, headers=None):
        body = b""

        if data is not None:
            body = json.dumps(data, indent=2).encode("utf-8")

        self.send_response(status)

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )

        if headers:
            for name, value in headers.items():
                self.send_header(name, value)

        if status != 204:
            self.send_header("Content-Length", str(len(body)))

        self.end_headers()

        if body:
            self.wfile.write(body)

    def _get_path(self):
        return urlsplit(self.path).path

    def _read_json(self):
        content_length = self.headers.get("Content-Length")

        if content_length is None:
            self._send_json(
                411, {"erro": "Content-Length eh obrigatorio."}
            )
            return None
        try:
            length = int(content_length)
            data = self.rfile.read(length)
            json_data = json.loads(data)
        except (ValueError, json.JSONDecodeError):
            self._send_json(
                400, {"erro": "JSON invalido."}
            )
            return None
        if not isinstance(json_data, dict):
            self._send_json(
                400, {"erro": "JSON deve ser um objeto."}
            )
            return None
        return json_data

    def _validate_book(self, book):
        required_fields = ("title", "author", "year", "available")

        for field in required_fields:
            if field not in book:
                self._send_json(
                    400, {"erro": f"Campo '{field}' eh obrigatorio."}
                )
                return False

        if not isinstance(book["title"], str):
            self._send_json(400, {"erro": "Campo 'title' deve ser uma string."})
            return False

        if not isinstance(book["author"], str):
            self._send_json(400, {"erro": "Campo 'author' deve ser uma string."})
            return False

        if not isinstance(book["year"], int):
            self._send_json(400, {"erro": "Campo 'year' deve ser um inteiro."})
            return False

        if not isinstance(book["available"], bool):
            self._send_json(400, {"erro": "Campo 'available' deve ser um booleano."})
            return False

        return True
    
    def do_GET(self):
        path = self._get_path()

        if path == "/api/books":
            self._send_json(200, BOOKS)
            return

        if path.startswith("/api/books/"):
            book_id_text = path.split("/")[-1]

            try:
                book_id = int(book_id_text)
            except ValueError:
                self._send_json(400, {"erro": "ID do livro invalido."})
                return

            book = next(
                (book for book in BOOKS if book["id"] == book_id),
            None)

            if book is None:
                self._send_json(404, {"erro": "Livro nao encontrado."})
                return
            self._send_json(200, book)
            return
        
        self._send_json(404, {"erro": "Rota nao encontrada."})

    def do_POST(self):
        path = self._get_path()

        if path != "/api/books":
            self._send_json(404, {"erro": "Rota nao encontrada."})
            return

        new_book = self._read_json()
        if new_book is None:
            return

        if not self._validate_book(new_book):
            return
        
        next_id = max((book["id"] for book in BOOKS), default=0) + 1
        new_book["id"] = next_id
        BOOKS.append(new_book)

        self._send_json(
            201, new_book, headers={"Location": f"/api/books/{next_id}"
            }
        )

    def do_PUT(self):
        path = self._get_path()

        if not path.startswith("/api/books/"):
            self._send_json(404, {"erro": "Rota nao encontrada."})
            return

        book_id_text = path.split("/")[-1]

        try:
            book_id = int(book_id_text)
        except ValueError:
            self._send_json(400, {"erro": "ID do livro invalido."})
            return

        book = next(
            (book for book in BOOKS if book["id"] == book_id),
            None
        )

        if book is None:
            self._send_json(404, {"erro": "Livro nao encontrado."})
            return

        updated_book = self._read_json()
        if updated_book is None:
            return

        if not self._validate_book(updated_book):
            return

        book["title"] = updated_book["title"]
        book["author"] = updated_book["author"]
        book["year"] = updated_book["year"]
        book["available"] = updated_book["available"]

        self._send_json(200, book)

    def do_DELETE(self):
        path = self._get_path()

        if not path.startswith("/api/books/"):
            self._send_json(404, {"erro": "Rota nao encontrada"})
            return

        book_id_text = path.split("/")[-1]

        try:
            book_id = int(book_id_text)
        except ValueError:
            self._send_json(400, {"erro": "ID do livro invalido."})
            return

        for index, book in enumerate(BOOKS):
            if book["id"] == book_id:
                BOOKS.pop(index)
                self._send_json(204)
                return

        self._send_json(404, {"erro": "Livro nao encontrado."})

def run(
    server_class = HTTPServer,
    handler_class = RestHTTPRequestHandler,
    port = 3001):

    server_address = ("127.0.0.1", port)
    httpd = server_class(server_address, handler_class)

    print(f"Servidor rodando em http://127.0.0.1:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
 run()

