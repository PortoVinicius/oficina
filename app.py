import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy

# Config
app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
db_path = os.path.join(app.instance_path or '.', 'database.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Servico(db.Model):
    __tablename__ = 'servicos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Servico {self.nome}>"

class Solicitacao(db.Model):
    __tablename__ = 'solicitacoes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(50), nullable=False)
    servico_id = db.Column(db.Integer, db.ForeignKey('servicos.id'), nullable=False)
    detalhes = db.Column(db.Text, nullable=True)
    criado_em = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    servico = db.relationship("Servico", backref="solicitacoes")

    def __repr__(self):
        return f"<Solicitacao {self.id} - {self.nome}>"

# Inicializa DB + seed
def init_db():
    with app.app_context():
        db.create_all()
        # seed somente se tabela servicos vazia
        if Servico.query.first() is None:
            seed = [
                Servico(nome="Revisão básica 10.000 km ou 6 meses", preco=100.0,
                        descricao="Troca de óleo, filtro de óleo, filtro de ar, filtro de combustível"),
                Servico(nome="Inspeções e ajustes", preco=100.0,
                        descricao="Pastilhas, Discos de freio"),
                Servico(nome="Diagnóstico eletrônico: preço variável de acordo com a complexidade.", preco=200.0,
                        descricao="Diagnóstico em sistemas de injeção eletrônica"),
                Servico(nome="Diagnóstico de suspensão automotiva", preco=250.0,
                        descricao="Realize uma inspeção visual para identificar vazamentos nos amortecedores e verificar danos nas molas, buchas e braços.")
            ]
            db.session.bulk_save_objects(seed)
            db.session.commit()

# Rotas
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/servicos")
def servicos():
    lista = Servico.query.all()
    return render_template("servicos.html", servicos=lista)

@app.route("/solicitar", methods=["GET", "POST"])
def solicitar():
    if request.method == "POST":
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        servico_id = request.form.get("servico")
        detalhes = request.form.get("detalhes")

        # validações simples
        if not nome or not telefone or not servico_id:
            flash("Por favor preencha todos os campos obrigatórios.", "danger")
            return redirect(url_for("solicitar"))

        try:
            servico_id = int(servico_id)
        except ValueError:
            flash("Serviço inválido.", "danger")
            return redirect(url_for("solicitar"))

        solicit = Solicitacao(
            nome=nome.strip(),
            telefone=telefone.strip(),
            servico_id=servico_id,
            detalhes=detalhes.strip() if detalhes else None
        )
        db.session.add(solicit)
        db.session.commit()

        flash("Pedido enviado com sucesso!", "success")
        return redirect(url_for(
            "sucesso",
            nome=nome,
            telefone=telefone,
            servico=servico_id
)       )


    servicos_disponiveis = Servico.query.all()
    return render_template("solicitar.html", servicos=servicos_disponiveis)

@app.route("/sucesso")
def sucesso():
    nome = request.args.get("nome", "")
    telefone = request.args.get("telefone", "")
    servico = request.args.get("servico", "")

    return render_template(
        "sucesso.html",
        nome=nome,
        telefone=telefone,
        servico=servico
    )


@app.route("/painel")
def painel():
    # lista de solicitações (ordenadas por data)
    pedidos = Solicitacao.query.order_by(Solicitacao.criado_em.desc()).all()
    return render_template("painel.html", pedidos=pedidos)

# inicialização do DB quando o app iniciar
init_db()


# Rota para servir o service worker na raiz
@app.route("/service-worker.js")
def service_worker():
    return send_from_directory("static", "service-worker.js")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
