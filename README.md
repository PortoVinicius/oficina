## ✅ ESTRUTURA FINAL
```bash
oficina/
│
├── app.py                  ← arquivo principal Flask
├── requirements.txt        ← dependências do projeto
├── helpers.py              ← funções auxiliares (igual ao CS50)
├── schema.sql              ← arquivo de criação do banco
│
├── instance/
│   └── database.db         ← banco SQLite (gerado depois)
│
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── app.js
│   └── img/
│       └── logo.png
│
├── templates/
│   ├── layout.html         ← igual ao layout.html do CS50
│   ├── index.html
│   ├── servicos.html
│   ├── solicitar.html
│   └── sucesso.html
│
├── models/
│   ├── __init__.py
│   └── servico.py          ← classe Serviço (futuro)
│
└── README.md
```
# Oficina (Flask + SQLite + Docker)

## Local (venv)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# criar DB (opcional: o app faz isso automaticamente)
sqlite3 instance/database.db < schema.sql

```bash
CREATE TABLE IF NOT EXISTS servicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    descricao TEXT
);

CREATE TABLE IF NOT EXISTS solicitacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT NOT NULL,
    servico_id INTEGER NOT NULL,
    detalhes TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(servico_id) REFERENCES servicos(id)
);
```

python app.py
# abrir http://localhost:5000

## Docker
docker-compose up --build
# abrir http://localhost:5000

# para parar:
docker compose down
# oficina
