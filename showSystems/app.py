from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    # Database URI
    "sqlite:///PATH_TO_YOUR_DATABASE.db"
)

db = SQLAlchemy(app)

class System(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    pasta = db.Column(db.String(150), nullable=False)
    node = db.Column(db.String(150), nullable=False)
    python = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    endereco_web = db.Column(db.String(150), nullable=True)
    porta_web = db.Column(db.String(10), nullable=True)


@app.route("/")
def index():
    sistemas = System.query.all()
    return render_template("index.html", sistemas=sistemas)


@app.route("/access_address/<int:id>")
def access_address(id):
    sistema = System.query.get_or_404(id)
    url = f"http://{sistema.endereco_web}:{sistema.porta_web}"
    return redirect(url)


if __name__ == "__main__":
    app.run(debug=True, port=5003)
