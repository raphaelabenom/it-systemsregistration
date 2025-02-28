from app import app, db  # Certifique-se de importar o app e db do arquivo principal
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

# Criar ou resetar o usuário admin
with app.app_context():
    from app import User  # Importar o modelo User do seu aplicativo

    # Procurar pelo usuário admin
    user = User.query.filter_by(username='admin').first()

    # Deletar o usuário, caso exista
    if user:
        print("Deletando usuário admin existente...")
        db.session.delete(user)
        db.session.commit()
        print("Usuário admin deletado com sucesso.")

    # Criar um novo usuário admin
    print("Criando novo usuário admin...")
    hashed_password = bcrypt.generate_password_hash('admin').decode('utf-8')
    new_user = User(username='admin', password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    print("Novo usuário admin criado com sucesso.")
