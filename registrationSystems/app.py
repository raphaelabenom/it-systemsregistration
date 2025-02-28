from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
)
import os
from waitress import serve

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sistemas.db"
app.config["SECRET_KEY"] = "supersecretkey"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


# Modelos
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


class System(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    pasta = db.Column(db.String(150), nullable=False)
    node = db.Column(db.String(150), nullable=False)
    python = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    endereco_web = db.Column(db.String(150), nullable=True)
    porta_web = db.Column(db.String(10), nullable=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("list_sistemas"))
        else:
            flash("Credenciais inválidas", "danger")
    return render_template("login.html", hide_nav=True)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def list_sistemas():
    sistemas = System.query.all()
    return render_template("list.html", sistemas=sistemas)


@app.route("/create", methods=["GET", "POST"])
@login_required
def create_sistema():
    if request.method == "POST":
        nome = request.form["nome"]
        pasta = request.form["pasta"]
        node = request.form["node"]
        python = request.form["python"]
        descricao = request.form["descricao"]
        endereco_web = request.form["endereco_web"]
        porta_web = request.form["porta_web"]

        novo_sistema = System(
            nome=nome,
            pasta=pasta,
            node=node,
            python=python,
            descricao=descricao,
            endereco_web=endereco_web,
            porta_web=porta_web,
        )
        db.session.add(novo_sistema)
        db.session.commit()
        flash("Sistema criado com sucesso!", "success")
        return redirect(url_for("list_sistemas"))
    return render_template("create.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_sistema(id):
    sistema = System.query.get_or_404(id)

    if request.method == "POST":
        sistema.nome = request.form["nome"]
        sistema.pasta = request.form["pasta"]
        sistema.node = request.form["node"]
        sistema.python = request.form["python"]
        sistema.descricao = request.form["descricao"]
        sistema.endereco_web = request.form["endereco_web"]
        sistema.porta_web = request.form["porta_web"]

        db.session.commit()
        flash("Sistema atualizado com sucesso!", "success")
        return redirect(url_for("list_sistemas"))

    return render_template("edit.html", sistema=sistema)


@app.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_sistema(id):
    sistema = System.query.get_or_404(id)
    db.session.delete(sistema)
    db.session.commit()

    # Busca lista atualizada de sistemas
    sistemas = System.query.all()

    # Renderiza apenas o partial com a lista atualizada
    return render_template(
        "sistemas_lista_partial.html",
        sistemas=sistemas,
        message="Sistema excluído com sucesso!",
    )


if __name__ == "__main__":
    if not os.path.exists("sistemas.db"):
        with app.app_context():
            db.create_all()
            if not User.query.filter_by(username="admin").first():
                hashed_password = bcrypt.generate_password_hash("admin").decode("utf-8")
                admin_user = User(username="admin", password=hashed_password)
                db.session.add(admin_user)
                db.session.commit()
    app.run(debug=True)
    serve(app, host="0.0.0.0", port=8080)
